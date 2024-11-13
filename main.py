import logging
from fastapi import FastAPI,Depends,status, HTTPException
import sqlalchemy.orm as _orm
from typing import Union,List
import fastapi.security as _security
from typing import Optional

from services import  create_database, get_db, get_current_user,get_user_by_email,create_token,create_task,create_user_,create_user_Task,authenticate_user,get_user_task,updateTask,deleteTask
# import schemas as _schema
from schemas import UserCreate,Task,TaskCreate,User
# import models as _model
# from .schemas import *
# from .models import User


app = FastAPI()

@app.on_event("startup")
async def startup():
    # This will run only once when the app starts
    create_database()
    logging.info("Database initialized successfully.")

@app.get('/')
def read_root():
    return {"Hello":"World"}

@app.post('/api/user')
async def create_user(user:UserCreate, db:_orm.Session = Depends(get_db)):

    user_db = get_user_by_email(user.email,db)

    if user_db:
        raise HTTPException(status_code=400,detail="Email already Exits")
    
    # user = _service.create_user_(user,db)
    user = create_user_(user,db)
    return create_token(user)

@app.post("/api/token") 
def generate_token(
    form_data:_security.OAuth2PasswordRequestForm = Depends(),db:_orm.Session = Depends(get_db)
):
    print("Received form data:")
    # print(f"Username: {form_data.username}")
    # print(f"Password: {form_data.password}")

    user = authenticate_user(email=form_data.username,password=form_data.password, db=db)

    print("Authenticated user:")
    print(user)

    if not user:
        print("User authentication failed")
        raise HTTPException(status_code=400,detail="Invalid Credentials")
    
    return create_token(user=user)


@app.get("/api/user/me", response_model=User)
def get_user(user:User = Depends(get_current_user)):
    return user



@app.post('/api/user/tasks', response_model=Task)
def create_task(task:TaskCreate,user:User =Depends(get_current_user), db:_orm.Session = Depends(get_db)):
    return create_task(user=user,db=db,task=task)

@app.post("/users/user/{user_id}/tasks", response_model=Task)
def create_user_task(user_id:int,task:TaskCreate,user:User = Depends(get_current_user),db:_orm.Session =Depends(get_db)):
    return create_user_Task(db=db,user_id=user_id,task=task)


@app.get("/api/tasks",response_model=List[Task])
async def get_user_tasks(user:User = Depends(get_current_user), db:_orm.Session = Depends(get_db)):
    return get_user_task(user=user,db=db)

@app.put("/api/task/{task_id}", response_model=Task)
async def update_task(
        task_id: int,
        is_completed: Optional[bool] = None,
        task_title: Optional[str] = None,
        user:User = Depends(get_current_user), 
        db:_orm.Session = Depends(get_db)):
    return updateTask(task_id=task_id, user=user,db=db,is_completed=is_completed, task_title=task_title)          

@app.delete("/api/task/{task_id}",response_model=Task)
async def delete_task(
    task_id:int,
    user:User = Depends(get_current_user),
    db: _orm.Session = Depends(get_db)):

    return deleteTask(user=user,db=db,task_id=task_id)


