from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, create_engine, Session

DATABASE_URL = 'sqlite:///./sample.db'

# sqlをコマンドラインにechoする設定でdbを作成
engine = create_engine(DATABASE_URL, echo=True)



class Task(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    title:  str
    discription: Optional[str]
    state:Optional[int] = Field(default=0)
    limit_at: Optional[datetime]
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    __tablename__ = 'tasks'


def create_db_and_tables(): # モデルからテーブルを生成
    SQLModel.metadata.create_all(engine)



def get_session(): # セッション作成

    with Session(engine) as session:
        yield session

