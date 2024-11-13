from services import create_database
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__" :
    create_database()
    print("Data Created Here...")