import hashlib


def get_gravatar_url(email, size=100):
    # メールアドレスを小文字にしてMD5でハッシュ化
    email_hash = hashlib.md5(email.lower().encode("utf-8")).hexdigest()

    # GravatarのURLを作成
    return f"https://www.gravatar.com/avatar/{email_hash}?s={size}"


# 例：gravatarのURLを生成
email = "sw.miki.0728@gmail.com"  # Gravatarに登録されたメールアドレス
avatar_url = get_gravatar_url(email)
