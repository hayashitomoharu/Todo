from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os
# DBの環境変数を読み込む
load_dotenv()
DATABASE_URL = str(os.getenv('DATABASE_URL'))

# sqlをコマンドラインにechoする設定
connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)


def create_db_or_connect():  # モデルからテーブルを生成
    SQLModel.metadata.create_all(engine)


# sessionをDependsによって作成する関数
def get_session():
    with Session(engine) as session:
        yield session
