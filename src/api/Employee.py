from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter (
    prefix="/Employee",
    tags=["Employee"],
    dependencies=[Depends(auth.get_api_key)],
)
    

class Employee(BaseModel):
    name: str

    skills: list[str]
    pay: float

    department: str


@router.post("/get")
def get_employee_stats(Employee: Employee):

    print(f"Name: {Employee.name}")
    print(f"Skills: {Employee.skills}")
    print(f"Pay: {Employee.pay}")
    print(f"Department: {Employee.department}")

@router.post("/read")
def read_employee_stats():
    print("Reading employee data from database")
    with db.engine.begin() as connection:
        Employee = connection.execute(sqlalchemy.text("SELECT * FROM employees")).all()
        print(Employee)