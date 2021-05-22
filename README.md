# activeManagement
出席管理ツール的な。目標：夏前までくらいに完成
### 目次
  
 - [環境](#環境)
 - [準備](#準備)
 - [docker](#docker)
 - [DBmigrate](#dbmigrate)
### 環境
---
| Title | Description | Vertion |
|----|----|----|
| 仮想環境 | Docker for Windows | 20.10.5 |
|  | conda | 4.10.1 |
| データベース | MySQL | 5.7 |
| アプリケーション言語| Python | 3.7 |
  
### 準備
---
.envファイルプロジェクトのルートディレクトリに作成し配置。以下を記述。
```
DB_HOST=接続ホスト
DB_NAME=データベース名
DB_PORT=ポート番号
DB_USER=ユーザー名
DB_PASS=パスワード
TZ=タイムゾーン
```
例
```
DB_HOST=localhost
DB_NAME=hoge
DB_PORT=3306
DB_USER=fuga
DB_PASS=piyo
TZ=Asia/Tokyo
```
### docker
---
コンテナ起動
  
```docker-compose up -d```
  
コンテナ停止
  
```docker-compose down```
  
コンテナ更新
  
```docker-compose up -d --build```
  
MySQLにアクセス
  
```docker-compose exec db bash```
  
MySQLにログイン
  
```mysql -u [username] -p```

### DBmigrate
---
必要パッケージ
```
pip install simple-db-migrate
pip install python-dotenv
pip install mysqlclient
```
./migrateにて以下のコマンドを実行
  
```db-migrate```
  
