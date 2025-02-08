# Python 3.13 ベースの公式イメージを使用
FROM python:3.13-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なシステムパッケージをインストール
RUN apt-get update && \ 
    apt-get install -y \
    default-mysql-client \ 
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    libmariadb-dev-compat \
    libmariadb-dev && \
     # MySQLクライアントを追加
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    

# Python 仮想環境を作成
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV DJANGO_SETTINGS_MODULE=portfolio.portfolio.settings

# 依存パッケージをコピーしてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# デフォルトのポートを開放
EXPOSE 8000

# サーバーを起動
CMD []

RUN pip install pymysql

RUN pip install cryptography

RUN pip install --no-cache-dir Pillow
