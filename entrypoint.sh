#!/bin/bash

# MySQLの接続を確認
until mysql -h db -u root -p'Bullshit03Sasano19' -e 'SELECT 1'; do
  echo "Waiting for MySQL..."
  sleep 2
done

# マイグレーションを実行
python manage.py migrate
# サーバーを起動
python manage.py runserver 0.0.0.0:8000
