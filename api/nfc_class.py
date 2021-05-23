from api import db_class as db
import binascii
import nfc

class nfcclass(object):
    def __init__(self):
        self.db = db.dbclass() #DBオブジェクトの作成
        self.idm = None;
        return

    def startup(self,targets):
        print ("ICカードをタッチしてください…")
        return targets

    def connected(self,tag):
        print("【 Touched 】")
        #IDmのみ変数に入れる
        self.idm = binascii.hexlify(tag.idm).decode()
        return True

    def getIdmConnected(self,tag):
        print("読み取りました。ICカードを離してください。")
        #IDmのみ変数に入れる
        self.idm = binascii.hexlify(tag.idm).decode()
        return True
    
    #大事な情報は初期化
    def released(self):
        print ("ICカードをタッチしてください…")
        return

    def resetIdm(self):
        self.idm = None
        return

    #読み取り処理のメインプログラム
    def main_read_ic(self):
        clf = nfc.ContactlessFrontend('usb')
        if not clf:
            print("接続されていません。終了します。")
            exit()
        try:
            while True:
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