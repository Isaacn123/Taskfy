from pydantic import BaseModel
import sqlalchemy as  _sql
import datetime as _dt

class _BaseUser(BaseModel):
    email:str
    name:str

class UserCreate(_BaseUser):
    password:str
    

    class Config:
        from_attributes=True

class User(_BaseUser):
    id:int
    date_created:_dt.datetime

    class Config:
        from_attributes = True


class _TaskBase(BaseModel):
    task_title:str

class TaskCreate(_TaskBase):
   pass

class Task(_TaskBase):
    id:int
    owner_id:int
    is_completed:bool = False
    date_created:_dt.datetime


    class Config:
        from_attributes = True




