from api import db_class as db
import binascii
import nfc
import time
import datetime
import csv

PATH = "./log/log.csv"

class nfcclass(object):
    def __init__(self):
        self.db = db.dbclass() #DBオブジェクトの作成
        self.idm = None;
        return

    def startup(self,targets):
        print ("ICカードをタッチしてください…")
        return targets

    def connected(self,tag):
        #IDmのみ変数に入れる
        self.idm = binascii.hexlify(tag.idm).decode()
        res = self.db.checkIc(self.idm)
        #ICカードが登録されていないときの処理
        if res is None:
            print("このICカードは登録されていません。")
            return True
        dt_now = datetime.datetime.now()
        dt_now = dt_now.strftime("%Y-%m-%d %H:%M:%S")
        #checked_atから確認
        if res["checked_at"] is None:
            self.db.loginUser(res["id"],dt_now)
            res = self.db.getUser(res["id"])
            print("\n{} {}が入室しました。\n".format(res[0]["checked_at"],res[0]["username"]))
            self.writeLog(res[0]["username"],res[0]["checked_at"],"入室")
        else:
            self.db.logoutUser(res["id"])
            print("\n{} {}が退出しました。\n".format(dt_now,res["username"]))
            self.writeLog(res["username"],dt_now,"退出")
        return True

    def getIdmConnected(self,tag):
        print("読み取りました。ICカードを離してください。")
        #IDmのみ変数に入れる
        self.idm = binascii.hexlify(tag.idm).decode()
        return True
    
    def released(self,tag):
        time.sleep(3)
        print ("ICカードをタッチしてください…")
        return

    #大事な情報は初期化
    def resetIdm(self):
        self.idm = None
        return

    def writeLog(self,username,checked_at,status):
        fa = open(PATH, "a",encoding="ms932",errors="",newline='') # ms932にエンコードしないと使えない。
        write_file = csv.writer(fa, delimiter=",",quotechar='"',skipinitialspace=True)
        write_file.writerow([status,username,checked_at])
        fa.close()
        return

    #読み取り処理のメインプログラム
    def main_read_ic(self):
        clf = nfc.ContactlessFrontend('usb')
        if not clf:
            print("接続されていません。終了します。")
            exit()
        try:
            # while True:
            clf.connect(rdwr={
                    'on-startup': self.startup,
                    'on-connect': self.connected,
                    'on-release': self.released,
                })
            self.resetIdm
        finally:
            clf.close()

    #idmのみ取得
    def read_ic(self):
        clf = nfc.ContactlessFrontend('usb')
        if not clf:
            print("接続されていません。終了します。")
            exit()
        try:
            clf.connect(rdwr={
                'on-startup': self.startup,
                'on-connect': self.getIdmConnected,
            })
            return self.idm
        finally:
            clf.close()