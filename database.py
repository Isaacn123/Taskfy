import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm
import os
from dotenv import load_dotenv
# import models as _mo
#DATABASE_URL = "postgresql://USER:PASSWORD@localhost:5432/DATABASE_NAME"


# DATABASE_URL = "sqlite:///./database.db"
# DATABASE_URL = "postgresql://user:password@localhost:5432/taskify_db"
# DATABASE_URL = os.getenv("DATABASE_URL","postgresql://user:password@localhost:5432/database.db")
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
# engine = _sql.create_engine(DATABASE_URL,connect_args={"check_same_thread":False})
engine = _sql.create_engine(DATABASE_URL)  # for postgress we dont need the string "check_same_thread" its for sqlite
SessionLocal = _orm.sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = _declarative.declarative_base()



