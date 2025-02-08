import os
import django

# Django の設定をロード
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# 作成するユーザー数 (開始を 1 にする)
start_index = 11
end_index = 20 

# ユーザーのリストを作成
users = []

for i in range(start_index, end_index + 1):  # user1 から user10 まで
    email = f'user{i}@example.com'

    # 既存のユーザーをチェック
    if not User.objects.filter(email=email).exists():
        user = User(name=f'user{i}', email=email, is_active=True, is_staff=True)
        user.set_password('password123')  # パスワードをハッシュ化
        user.save()
    else:
        print(f"User {email} already exists. Skipping.")

# 作成処理を実行
for user in users:
    user.save()

print(f"{len(users)} users have been created!")
