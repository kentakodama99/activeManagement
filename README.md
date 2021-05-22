# activeManagement
出席管理ツール的な。目標：夏前までくらいに完成

### docker
***
.envファイルを作成し、環境変数を入れてください。
#### donker-compose 起動
```docker-compose up -d```
#### docker-compose 更新
```docker-compose up -d --build```
#### docker-compose MySQLにアクセス
```docker-compose exec db bash```
#### MySQL login
```mysql -u [username] -p```

### DBmigrate
***
必要パッケージ
```
pip install simple-db-migrate
pip install python-dotenv
pip install mysqlclient
```
./migrateにて以下のコマンドを実行<br/>
```db-migrate```
