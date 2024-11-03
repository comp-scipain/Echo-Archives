from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/reset")
def reset():
    """
    Reset everything
    """
    print("Nuking everything")    
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("DELETE FROM test_table"))
        # Remember to uncomment this later
        #connection.execute(sqlalchemy.text("DELETE FROM employees"))

    return "OK"