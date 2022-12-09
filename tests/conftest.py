import os
import shutil

import pytest
from apps.app import create_app, db
from apps.crud.models import User
from apps.detector.models import UserImage, UserImageTag


@pytest.fixture
def fixture_app():
    # セットアップ処理
    app = create_app("testing")

    # データベースを利用するための宣言をする
    app.app_context().push()

    # テスト用データベースのテーブルを作成する
    with app.app_context():
        db.create_all()

    # テスト用の画像アップロードディレクトリを作成する
    os.mkdir(app.config["UPLOAD_FOLDER"])

    # テストを実行する
    yield app

    # クリーンナップ処理
    User.query.delete()
    UserImage.query.delete()
    UserImageTag.query.delete()

    shutil.rmtree(app.config["UPLOAD_FOLDER"])
    db.session.commit()


# TODO こいつがよく分からない... 引数の fixture_app は 上で def した関数？->yes
@pytest.fixture
def client(fixture_app):
    return fixture_app.test_client()
