from pathlib import Path

from flask.helpers import get_root_path
from werkzeug.datastructures import FileStorage


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


def upload_image(client, image_path):
    """画像をアップロードする"""
    image = Path(get_root_path("tests"), image_path)

    test_file = (
        FileStorage(
            stream=open(image, "rb"),
            filename=Path(image_path).name,
            content_type="multipart/form-data",
        )
    )

    data = dict(
        image=test_file,
    )
    return client.post("/upload", data=data, follow_redirects=True)


def test_upload_signup_post_validate(client):
    signup(client, "admin", "flaskbook@example.com", "password")
    rv = upload_image(client, "detector/testdata/test_invalid_file.txt")
    assert "サポートされていない画像形式です。" in rv.data.decode()