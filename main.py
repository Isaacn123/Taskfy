from fastapi import FastAPI,Depends,status, HTTPException
import sqlalchemy.orm as _orm
from typing import Union,List
import fastapi.security as _security
from typing import Optional

import services as _service
import schemas as _schema
import models as _model


app = FastAPI()

@app.get('/')
def read_root():
    return {"Hello":"World"}

@app.post('/api/user')
async def create_user(user:_schema.UserCreate, db:_orm.Session = Depends(_service.get_db)):

    user_db = _service.get_user_by_email(user.email,db)

    if user_db:
        raise HTTPException(status_code=400,detail="Email already Exits")
    
    user = _service.create_user_(user,db)
    return _service.create_token(user)

@app.post("/api/token")
def generate_token(
    form_data:_security.OAuth2PasswordRequestForm = Depends(),db:_orm.Session = Depends(_service.get_db)
):
    print("Received form data:")
    # print(f"Username: {form_data.username}")
    # print(f"Password: {form_data.password}")

    user = _service.authenticate_user(email=form_data.username,password=form_data.password, db=db)

    print("Authenticated user:")
    print(user)

    if not user:
        print("User authentication failed")
        raise HTTPException(status_code=400,detail="Invalid Credentials")
    
    return _service.create_token(user=user)


@app.get("/api/user/me", response_model=_schema.User)
def get_user(user:_schema.User = Depends(_service.get_current_user)):
    return user



@app.post('/api/user/tasks', response_model=_schema.Task)
def create_task(task:_schema.TaskCreate,user:_schema.User =Depends(_service.get_current_user), db:_orm.Session = Depends(_service.get_db)):
    return _service.create_task(user=user,db=db,task=task)

@app.post("/users/user/{user_id}/tasks", response_model=_schema.Task)
def create_user_task(user_id:int,task:_schema.TaskCreate,user:_schema.User = Depends(_service.get_current_user),db:_orm.Session =Depends(_service.get_db)):
    return _service.create_user_Task(db=db,user_id=user_id,task=task)


@app.get("/api/tasks",response_model=List[_schema.Task])
async def get_user_tasks(user:_schema.User = Depends(_service.get_current_user), db:_orm.Session = Depends(_service.get_db)):
    return _service.get_user_task(user=user,db=db)

@app.put("/api/task/{task_id}", response_model=_schema.Task)
async def update_task(
        task_id: int,
        is_completed: Optional[bool] = None,
        task_title: Optional[str] = None,
        user:_schema.User = Depends(_service.get_current_user), 
        db:_orm.Session = Depends(_service.get_db)):
    return _service.updateTask(task_id=task_id, user=user,db=db,is_completed=is_completed, task_title=task_title)          

@app.delete("/api/task/{task_id}",response_model=_schema.Task)
async def delete_task(
    task_id:int,
    user:_schema.User = Depends(_service.get_current_user),
    db: _orm.Session = Depends(_service.get_db)):

    return _service.deleteTask(user=user,db=db,task_id=task_id)


