from datetime import datetime, timedelta
from typing import Optional

from sqlmodel import Field, SQLModel, create_engine, Session
import pytz
DATABASE_URL = 'sqlite:///./sample.db'


# SQLModelで型定義とレコードの定義を同時に行う？

class TaskBase(SQLModel):
    # baseモデル　titleのみbaseモデルでも必須値　notionのように
    title:                   str
    description:    Optional[str] = None
    progress_state: Optional[int] = None
    limit_at:  Optional[datetime] = None





class Task(TaskBase, table=True):

    # 実際にテーブルとして追加するモデル
    id: Optional[int] = Field(default=None, primary_key=True)

    # インスタンス作成時に自動作成される時間のデータ
    created_at: datetime = Field(default_factory=lambda: datetime.now(pytz.timezone('Asia/Tokyo')), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(pytz.timezone('Asia/Tokyo')), nullable=False)
    __tablename__ = 'tasks'


class TaskCreate(TaskBase):

    pass


class TaskRead(TaskBase):
    pass


class TaskUpdate(SQLModel):

    title:          Optional[str] = None
    description:    Optional[str] = None
    progress_state: Optional[int] = None
    limit_at:       Optional[datetime] = Field(default_factory=lambda: datetime.now(pytz.timezone('Asia/Tokyo')), nullable=True)





# sqlをコマンドラインにechoする設定でdbを作成
connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)


def create_db_and_tables(): # モデルからテーブルを生成
    SQLModel.metadata.create_all(engine)

# sessionをDependsによって作成する関数
def get_session():
    with Session(engine) as session:
        yield session
