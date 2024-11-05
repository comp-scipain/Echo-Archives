from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/employee",
    tags=["Employee"],
    dependencies=[Depends(auth.get_api_key)],
)


class Employee(BaseModel):
    name: str
    skills: list[str]
    pay: float
    department: str
    level: int


@router.post("/stats", response_model=Employee)
def get_employee_stats(emp_id: int):
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text("SELECT name, skills, pay, department, level FROM employees WHERE id = :id"),
            {"id": emp_id}
        ).fetchone()
        
        if result is None:
            raise HTTPException(status_code=404, detail="Employee not found")

        name, skills, pay, department, level = result

        return Employee(
            name=name,
            skills=skills,
            pay=pay,
            department=department,
            level=level
        )


@router.post("/get")
def get_all_employee_stats():
    """
    Get a list of all the current employees
    """
    print("Reading employee data from database")
    with db.engine.begin() as connection:
        employees = connection.execute(
            sqlalchemy.text("SELECT name, skills, pay, department, level FROM employees")
        ).fetchall()

        if not employees:
            raise HTTPException(status_code=404, detail="No employees found")

        return [Employee(name=e.name, skills=e.skills, pay=e.pay, department=e.department, level=e.level) for e in employees]


@router.post("/add")
def add_new_employee(employee: Employee):
    """
    Add a new employee to the Database
    """
    print(f"Adding employee named {employee.name} with {employee.skills} skills being paid ${employee.pay} to work in the {employee.department} department")
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text("INSERT INTO employees (name, skills, pay, department, level) VALUES (:name, :skills, :pay, :department, :level)"),
            {"name": employee.name, "skills": employee.skills, "pay": employee.pay, "department": employee.department, "level": employee.level}
        )
        print("Done")
    return {"status": "OK"}


@router.post("/delete")
def fire_employee(employee_id: int):
    """
    Removes a specific employee from the database based on the employee_id passed in
    """
    with db.engine.begin() as connection:
        to_be_fired = connection.execute(
            sqlalchemy.text("SELECT * FROM employees WHERE id = :id"), {"id": employee_id}
        ).fetchone()

        if not to_be_fired:
            raise HTTPException(status_code=404, detail="Employee not found")

        print(f"This employee will be fired: {to_be_fired}")
        connection.execute(
            sqlalchemy.text("DELETE FROM employees WHERE id = :id"), {"id": employee_id}
        )
        print("Done!")
    return {"status": "OK"}


@router.post("/search")
def search_employees():
    """
    Search for specific employees
    """
    print("Not currently implemented :(")
    raise HTTPException(status_code=501, detail="Not currently implemented")

