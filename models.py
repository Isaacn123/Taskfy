from datetime  import datetime as _dt

import sqlalchemy as _sql
import sqlalchemy.orm  as _orm
import passlib.hash as _hash

from database import Base

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer,primary_key=True,index=True)
    email = _sql.Column(_sql.String,unique=True,index=True)
    name = _sql.Column(_sql.String)
    hashed_password = _sql.Column(_sql.String)
    date_created = _sql.Column(_sql.DateTime,default=_dt.utcnow)
   #  tasks = _sql.Column("Task", back_populates="owner")
    tasks = _orm.relationship("Task", back_populates="owner")

    def verify_password(self,password:str):
         return _hash.bcrypt.verify(password,self.hashed_password)
      #   except _hash.bcrypt.MissingBackendError:
      #      raise RuntimeError("bcrypt backend is not available. Please install the 'bcrypt' package.")
        
    def to_dict(self):
       return {
          "id":self.id,
          "name":self.name,
          "email": self.email,
          "hashed_password":self.hashed_password,
          "date_created":self.date_created.isoformat() if self.date_created else None,
       }

class Task(Base):
   __tablename__ = "tasks"
   id = _sql.Column(_sql.Integer,primary_key=True,index=True)
   task_title = _sql.Column(_sql.String)
   is_completed = _sql.Column(_sql.Boolean,default=False)
   owner_id = _sql.Column(_sql.Integer,_sql.ForeignKey("users.id"))
   date_created = _sql.Column(_sql.DateTime,default=_dt.utcnow)

   # owner = _sql.Column("User",back_populates="tasks")
   owner = _orm.relationship("User", back_populates="tasks")

