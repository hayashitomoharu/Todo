from sqlmodel import  SQLModel, create_engine, Session

DATABASE_URL = 'sqlite:///./sample.db'

# sqlをコマンドラインにechoする設定
connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)


def create_db_and_tables(): # モデルからテーブルを生成
    SQLModel.metadata.create_all(engine)

# sessionをDependsによって作成する関数
def get_session():
    with Session(engine) as session:
        yield session
