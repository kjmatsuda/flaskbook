def test_index(client):
    rv = client.get("/")
    assert "ログイン" in rv.data.decode()
    assert "画像新規登録" in rv.data.decode()


def signup(client, username, email, password):
    """サインアップする"""
    data = dict(username=username, email=email, password=password)
    return client.post("/auth/signup", data=data, follow_redirects=True)


def test_index_signup(client):
    """サインアップを実行する"""
    rv = signup(client, "admin", "flaskbook@example.com", "password")
    assert "admin" in rv.data.decode()

    rv = client.get("/")
    assert "ログアウト" in rv.data.decode()
    assert "画像新規登録" in rv.data.decode()


def test_upload_no_auth(client):
    rv = client.get("/upload", follow_redirects=True)
    # 画像アップロード画面にはアクセスできない
    assert "アップロード" not in rv.data.decode()
    # ログイン画面へリダイレクトされる
    assert "メールアドレス" in rv.data.decode()
    assert "パスワード" in rv.data.decode()


def test_upload_signup_get(client):
    signup(client, "admin", "flaskbook@example.com", "password")
    rv = client.get("/upload", follow_redirects=True)
    assert "アップロード" in rv.data.decode()
