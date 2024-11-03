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


@router.post("/employee")
def get_employee_stats(Employee: Employee):

    print(f"Name: {Employee.name}")
    print(f"Skills: {Employee.skills}")
    print(f"Pay: {Employee.pay}")
    print(f"Department: {Employee.department}")


@router.post("/get")
def get_all_employee_stats():
    """
    Get a list of all the current employees
    """
    print("Reading employee data from database")
    with db.engine.begin() as connection:
        employee = connection.execute(sqlalchemy.text("SELECT name, skills, pay, department FROM employees")).all()
        for person in employee:
            print(f"Employee name: {person.name}")
            print(f"Employee skills: {person.skills}")
            print(f"Employee pay: {person.pay}")
            print(f"Employee Department: {person.department}")
            

@router.post("/add")
def add_new_employee(Employee: Employee):
    """
    Add a new employee to the database
    """
    print(f"adding employee named {Employee.name} with {Employee.skills} skills being paid ${Employee.pay} to work in {Employee.department}")
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("INSERT INTO employees (name, skills, pay, department) Values (:name, :skills, :pay, :department)"),
        {"name":Employee.name,"skills": Employee.skills, "pay":Employee.pay,"department":Employee.department})
        print("Done")


@router.post("/search")
def search_employees():
    """
    search for specific employees
    """
    print("Not currently implemented :(")