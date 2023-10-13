from fastapi import FastAPI, Depends
from sqlmodel import Session, select, SQLModel
from sqlmodel_init.database_and_session import engine , Task, get_session

# sqlmodel_databaseからインポートしたモデルからテーブルを生成
SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.post("/Todo/", response_model=Task)
def index_create(title, session: Session = Depends(get_session())):
    pass
