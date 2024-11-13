

import jwt as _jwt
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import sqlalchemy as _sql
import email_validator as _checkmail
import fastapi.security as _security
from fastapi import HTTPException, Depends
import dotenv as _env
from typing import Optional

# import database as _database
from .database import *
# import schemas as _schema
from .schemas import *
# import models as _model
from .models import *
import os as _os
import logging

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

_env.load_dotenv()
JWT_SECRETE =""  # _os.environ["JWT_SECRETE"]
# helper for checking if one is authendictated
oauth2schema = _security.OAuth2PasswordBearer("/api/token")

logging.basicConfig(level=logging.INFO)

def create_database():

    # return Base.metadata.create_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    logging.info("Database tables created or checked")

async def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()    


def create_user_(user:UserCreate, db:_orm.Session):

    try:
        valid = _checkmail.validate_email(user.email)
        email = valid.email
    except _checkmail.EmailNotValidError:
        raise HTTPException(status_code=400,detail="Please enter a valid email")
    
    user_obj = User(email=email,name=user.name,hashed_password=_hash.bcrypt.hash(user.password))

    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


def get_user_by_email(email:str,db:_orm.Session):
    return db.query(User).filter(User.email == email).first()

def create_token(user:User):
    # user_obj = _schema.User.model_validate(user)
    user_obj = user.to_dict()
    # token = _jwt.encode(user_obj.model_dump(),JWT_SECRETE)
    token = _jwt.encode(user_obj,JWT_SECRETE,algorithm="HS256")

    return dict(access_token=token,token_type="bearer")

# def generate_token():
def authenticate_user(email:str,password:str,db:_orm.Session):
    user = get_user_by_email(email=email,db=db)
    # print(f"User: {user.hashed_password}")
    # if not user:
    #     print(f"User: NO USER")
    #     return False
    # if not user.verify_password(password=password):
    #     print(user.verify_password(password=password))
    #     print(f"User: FAILED TO AUTHENTICATE")
    #     return False
    
    # return user
    if user:
        print(f"User found: {user.email}")
        hashed_password2 = _hash.bcrypt.hash(password)
        print(f"Stored hashed password: {user.hashed_password}")
        # print(f"Stored  password: {password}")
        # print(_hash.bcrypt.verify(password,hashed_password2))
        if user.verify_password(password=password):
            print("Password verification successful")
            return user
        else:
            print("Password verification failed")
            return None
    else:
        print("User not Found")
        return None

def get_current_user(db:_orm.Session = Depends(get_db),token:str=Depends(oauth2schema)):

    try:
        payload = _jwt.decode(token,JWT_SECRETE,algorithms=["HS256"])
        # user = db.query(_model.User).get(payload["id"])
        user_id = payload["id"]
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=401,detail="User not found")
        
    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return User.model_validate(user)

def create_task(user:User, db:_orm.Session, task:TaskCreate):
    task_data = task.model_dump()
    task_data["owner_id"] = user.id
    task_data["is_completed"] = False
    task = Task(**task_data)
    db.add(task)
    db.commit()
    db.refresh(task)
    return Task.model_validate(task)

def create_user_Task(db:_orm.Session,user_id:int, task:TaskCreate):
    user_task =  Task(**task.model_dump(),owner_id=user_id)
    db.add(user_task)
    db.commit()
    db.refresh(user_task)
    return Task.model_validate(user_task)


def get_user_task(user:User,db:_orm.Session):
    tasks = db.query(Task).filter(Task.owner_id == user.id).all()
    return list(map(Task.from_orm,tasks))
    # return [task.model_dump for task in tasks]

def updateTask(
        user:User, 
        task_id:int, 
        db:_orm.Session, 
        task_title:Optional[str] = None, # added the title also
        is_completed:Optional[bool] = None  # is_completed:bool :converting to Optional Field
        ):
    task = db.query(Task).filter(Task.id == task_id,Task.owner_id == user.id).first()

    # if task:
        # task.is_completed = is_completed
    #     db.commit()
    #     return task
    # If the task doesn't exist, raise an error
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    #Update fields only if they are provided
    if is_completed is not None:
        task.is_completed = is_completed

    if task_title is not None:
        task.task_title = task_title
    
    # Commit the changes to the database
    db.commit()
    db.refresh(task)

    return task

def deleteTask(
        user:User, 
        task_id:int, 
        db:_orm.Session, ):
    tasks = db.query(Task).filter(Task.id==task_id,Task.owner_id == user.id).first()

    if not tasks:
        raise HTTPException(status_code=404,detail="Task not found")
    
    db.delete(tasks)
    db.commit()

    return tasks
    # return {"status":200,"msg": "task succefully deleted"}
