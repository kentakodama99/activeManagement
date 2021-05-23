from api import db_class as db
from api import nfc_class as mynfc

#ユーザーチェック関数(y(OK)/n(ユーザーが異なる)/None(ユーザーなし))
def userCheck(db,ic_num = False):
    db.getAllUsersList()
    try:
        user_id = int(input('登録者のIDを入力してください（上記参考）>>'))
        user = db.getUser(user_id)
    #文字列などの例外処理はユーザーなし扱い。
    except:
        return None,None
    #ユーザーが存在したときは、ユーザー確認
    if  user :
        print("\n\n\n\n\n\n\n以下のユーザーでよろしいでしょうか？[y/n]")
        print("\n登録者名:{}".format(user[0]["username"]))
        for raw in user:
            if ic_num:
                print("({}) ICカード名:{}".format(user.index(raw),raw["ic_name"]))
            else:
                print("ICカード名:{}".format(raw["ic_name"]))
        print("\n")
        val = input('[y/n]>>')
    else:
        val = None
    return val,user

#IC取得andチェック関数
def getIdm():
    nfc = mynfc.nfcclass()
    try:
        while True:
            res = nfc.read_ic()
            if db.checkIc(res):
                print("このICカードはすでに登録されています。他のICカードでやり直しますか？[y/n]")
                val = input('[y/n]>>')
                nfc.resetIdm()
                if not val == str("y"):
                    print("終了します")
                    exit()
            else:
                nfc.resetIdm()
                return res
    except:
        nfc.resetIdm()
        print("エラーが発生しました。プログラムを終了します。")
        exit()

if __name__ == "__main__":
    db = db.dbclass() #DBオブジェクトの作成
    while True:
        print("操作したいメニューを追加してください。")
        print("0:データの取得、1:ICカードの登録、2:ICカードの更新、3:ICカードの削除、exit:終了")
        val = input('>>')

        #get
        if val == str(0):
            print("どちらを取得しますか？(0.ユーザーの取得 1.ICカードの取得)")
            val = input('>>')
            if val == str(0):
                db.getAllUsersList()
                db.closeDB()
            elif val == str(1):
                db.getAllList()
                db.closeDB()

        #create
        elif val == str(1):
            val,user = userCheck(db)
            #yならICカードの新規登録設定へ
            if val == str("y"):
                ic_id = getIdm()
                ic_name = input('ICカード名を入力してください。（例：通学用）>>')
                print("\n以下でICカードを新規登録します。よろしいでしょうか？[y/n]")
                print("\n登録者名:{}".format(user[0]["username"]))
                print("ICカード名:{}".format(ic_name))
                val = input('[y/n]>>')
                #yなら登録
                if val == str("y"):
                    db.createUser(ic_id,ic_name,user[0]["id"])
                    print("登録しました。")
                    db.closeDB()
                #nならスタートメニューに戻る
                elif val == str("n"):
                    print("キャンセルしました。スタートメニューに戻ります。\n")
            #nならスタートメニューに戻る
            elif val == str("n"):
                print("キャンセルしました。スタートメニューに戻ります。\n")
            #ユーザーが存在ないときは、ユーザーを新規登録する
            else:
                print("ユーザーが存在しません。新しく登録しますか？")
                val = input('[y/n]>>')
                #yなら登録
                if val == str("y"):
                    ic_id = getIdm()
                    username = input('ユーザー名を入力してください。（例：鈴木一郎）>>')
                    ic_name = input('ICカード名を入力してください。（例：通学用）>>')
                    print("\n以下でICカードを新規登録します。よろしいでしょうか？[y/n]")
                    print("\n登録者名:{}".format(username))
                    print("ICカード名:{}".format(ic_name))
                    val = input('[y/n]>>')
                    #yなら登録
                    if val == str("y"):
                        db.createUser(ic_id,ic_name,None,username)
                        print("登録しました。")
                        db.closeDB()
                    #nならスタートメニューに戻る
                    elif val == str("n"):
                        print("キャンセルしました。スタートメニューに戻ります。\n")
                #nならスタートメニューに戻る
                elif val == str("n"):
                    print("キャンセルしました。スタートメニューに戻ります。\n")

        #put
        elif val == str(2):
            val,user = userCheck(db,True)
            if val == str("y"):
                print("変更したいICカードの番号を入力してください。（上記参考）")
                ic_num = int(input('>>'))
                if user[ic_num]:
                    print("変更後ICカードをタッチしてください。")
                    update_ic_id = getIdm()
                    ic_name = input('ICカード名を入力してください。（例：通学用）>>')
                    print("\n以下のICカードを更新します。よろしいでしょうか？[y/n]")
                    print("\n登録者名:{}".format(user[0]["username"]))
                    print("ICカード名:{}".format(ic_name))
                    val = input('[y/n]>>')
                    #yなら登録
                    if val == str("y"):
                        db.update(user[ic_num]["ic_id"],update_ic_id,ic_name)
                        print("更新しました。")
                        db.closeDB()
                    #nならスタートメニューに戻る
                    elif val == str("n"):
                        print("キャンセルしました。スタートメニューに戻ります。\n")
                else:
                    print("IC番号が存在しません。スタートメニューに戻ります。\n")

        #delete
        elif val == str(3):
            val,user = userCheck(db,True)
            if val == str("y"):
                print("削除したいICカードの番号を入力してください。（上記参考）")
                ic_num = int(input('>>'))
                if user[ic_num]:
                    print("\n以下のICカードを削除します。よろしいでしょうか？[y/n]")
                    print("\n登録者名:{}".format(user[0]["username"]))
                    print("ICカード名:{}".format(user[ic_num]["ic_name"]))
                    val = input('[y/n]>>')
                    #yなら登録
                    if val == str("y"):
                        db.delete(user[ic_num]["ic_id"],user[0]["id"])
                        print("削除しました。")
                        db.closeDB()
                    #nならスタートメニューに戻る
                    elif val == str("n"):
                        print("キャンセルしました。スタートメニューに戻ります。\n")
                else:
                    print("IC番号が存在しません。スタートメニューに戻ります。\n")

        #exit
        elif val == str("exit"):
            db.closeDB()


        print("\nERROR:もう一度入力してください\n")
        #reset
        val = None
        user = None
        username = None
        ic_id = None
        update_ic_id = None
        ic_name = None
        ic_num = None