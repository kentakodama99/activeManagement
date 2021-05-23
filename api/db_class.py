import os
import pymysql.cursors
from dotenv import load_dotenv

class dbclass(object):
    def __init__(self):
        load_dotenv()
        # MySQLに接続する
        self.connection = pymysql.connect(
            host= os.getenv("DB_HOST"),
            port = int(os.getenv("DB_PORT")),
            user= os.getenv("DB_USER"),
            password = os.getenv("DB_PASS"),
            db = os.getenv("DB_NAME"),
            charset='utf8',
            cursorclass = pymysql.cursors.DictCursor)

    def getAll(self,table = "AllIc"): #table引数 table->table単体を取得。All->全てのIC情報の取得。
        with self.connection.cursor() as cursor:
            if table == "AllIc":
                sql = "SELECT * FROM users right join ic_users on users.id = ic_users.id "
                sql += "ORDER BY users.id ASC;"
            else:
                sql = "SELECT * FROM {} ".format(table)
                sql += "ORDER BY id ASC;"
            cursor.execute(sql) #SQLの実行
            self.connection.commit()
            res = cursor.fetchall()
        return res

    def getUser(self,user_id): #table引数 table->table単体を取得。All->全ての情報の取得。
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM users left join ic_users on users.id = ic_users.id WHERE users.id = %s;"
            cursor.execute(sql,(user_id))
            self.connection.commit()
            res = cursor.fetchall()
        return res

    def getAllList(self):
        res = self.getAll()
        print("\n--------------------------")
        for raw in res:
            print("[id:{}] 名前:{} ICカード名:{}".format(raw["id"],raw["username"],raw["ic_name"]))
        print("--------------------------\n")

    def getAllUsersList(self):
        res = self.getAll("users")
        print("\n--------------------------")
        for raw in res:
            print("[id:{}] 名前:{} checked_at:{}".format(raw["id"],raw["username"],raw["checked_at"]))
        print("--------------------------\n")

    def checkIc(self,ic_id): #table引数 table->table単体を取得。All->全ての情報の取得。
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM ic_users WHERE ic_id = %s;"
            cursor.execute(sql,(ic_id))
            self.connection.commit()
            res = cursor.fetchone()
        return res

    def createUser(self,ic_id,ic_name,id = None,username = None):
        with self.connection.cursor() as cursor:
            #ユーザー新規登録
            if not username is None:
                sql ="INSERT INTO users(username) value(%s); "
                cursor.execute(sql,(username)) #SQLの実行
                self.connection.commit()
                sql ="SELECT * FROM users ORDER BY id DESC;"
                cursor.execute(sql) #SQLの実行
                self.connection.commit()
                id = int(cursor.fetchone()["id"])
            #ICカード登録
            sql = "INSERT INTO ic_users(id,ic_id,ic_name) value(%s,%s,%s);"
            cursor.execute(sql,(id,ic_id,ic_name)) #SQLの実行
            self.connection.commit()
            return

    def update(self,ic_id,update_ic_id,ic_name):
        with self.connection.cursor() as cursor:
            #ICカード更新
            sql =  "UPDATE ic_users SET ic_id = %s,ic_name= %s WHERE ic_id = %s;"
            cursor.execute(sql,(update_ic_id,ic_name,ic_id)) #SQLの実行
            self.connection.commit()
            return
        
    def delete(self,ic_id,id):
        print(ic_id)
        print(id)
        with self.connection.cursor() as cursor:
            #ICカード更新
            sql =  "DELETE FROM ic_users WHERE ic_id = %s;"
            cursor.execute(sql,(ic_id)) #SQLの実行
            self.connection.commit()
            check = self.getUser(id)
            if check[0]["ic_id"] is None:
                print(check)
                sql =  "DELETE FROM users WHERE id = %s;"
                cursor.execute(sql,(id)) #SQLの実行
                self.connection.commit()
                print(">>>>登録ICがなくなったので、ユーザーを削除しました")
            return


    def closeDB(self):
        self.connection.close()
        input('Enterで終了します')
        exit()