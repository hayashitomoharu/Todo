from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Session, select
from models.model_and_session import *
from typing import List
# sqlmodel_databaseからインポートしたモデルからテーブルを生成


app = FastAPI()

# sqlomodelを作成？
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Taskモデルにレコードが存在するかチェックしてなければ指定したstatus_codeでエラーをraiseする関数
def get_task_or_exception(task_id: int, status_code, session: Session):
    task_by_id = session.get(Task, task_id)
    if not task_by_id:
        raise HTTPException(status_code=status_code, detail=f"Task with id : {task_id} not found")
    return task_by_id


@app.get("/todos/", response_model=List[Task])
def index(offset: int = 0, limit: int = Query(default=100, lte=100,),session:Session = Depends(get_session)):
    """
        全てのタスクを返す
        queryでoffsetとlimitを指定可能
    """
    # sqlmodelにTask型のテーブルを返してもらい、offsetとlimitを適用
    all_tasks = session.exec(select(Task).offset(offset).limit(limit)).all()

    return all_tasks


@app.get("/todos/{task_id}", response_model=Task)
def show(task_id: int, session:Session = Depends(get_session)):
    """指定したidのタスクを返す"""

    # DBから取得したいレコードをtask_by_idに取り出す
    task_by_id = get_task_or_exception(task_id=task_id,status_code=404, session=session)

    return task_by_id

@app.post("/todos/", response_model=Task)
def create(posted_task: TaskCreate, session:Session = Depends(get_session)):
    """新たにタスクを追加する"""

    # postされたデータをレコードとして追加する
    task_by_id = Task.from_orm(posted_task)
    session.add(task_by_id)
    session.commit()
    session.refresh(task_by_id)

    return task_by_id


@app.put("/todos/{task_id}", response_model=Task)
def update(task_id: int ,puted_task: TaskUpdate, session:Session = Depends(get_session)):
    """既存のtaskレコードを任意の内容で更新する"""

    # DBから更新したいレコードをtask_by_idに取り出す
    task_by_id = get_task_or_exception(task_id=task_id, status_code=404, session=session)

    # putで送られているデータからNoneを排除するが、nullやNoneがクライアントから明示的に送られている場合は辞書に加えて削除できる
    puted_task_data = puted_task.dict(exclude_unset= True)

    # Noneが排除されたdict型から、items()で取り出してtask_by_idに更新する
    for key, value in puted_task_data.items():
        setattr(task_by_id, key, value)

    # DBへの処理
    session.add(task_by_id)
    session.commit()
    session.refresh(task_by_id)

    return task_by_id


@app.delete("/todos/{task_id}")
def destroy(task_id: int, session:Session = Depends(get_session)):
    """特定のレコードを削除する"""
    # DBから削除したいレコードをtask_by_idに取り出す
    task_by_id = get_task_or_exception(task_id=task_id, status_code=404, session=session)

    session.delete(task_by_id)
    session.commit()

    return {"ok": True}
