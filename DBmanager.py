

if __name__ == "__main__":
    while True:
        print("操作したいメニューを追加してください。")
        print("1:登録ICカード一覧の取得、1:ICカードの登録、2:ICカードの更新、3:ICカードの削除、exit:終了")
        val = input('Enter choose menu>>')
        if val == str(1):
            print("get")
            exit()
        elif val == str(2):
            print("post")
            exit()
        elif val == str(3):
            print("put")
            exit()
        elif val == str(4):
            print("delete")
            exit()
        elif val == str("exit"):
            print("exit")
            exit()
        else:
            print("\nERROR:もう一度入力してください\n")