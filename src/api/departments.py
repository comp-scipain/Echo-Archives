from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter (
    prefix="/Departments",
    tags=["Departments"],
    dependencies=[Depends(auth.get_api_key)],
)

class Department(BaseModel):
    name: str
    basePay: float
    population: int


@router.post("/new/")
def add_new_department(dept: Department):
    """
    Add a new department to the Database
    """
    print(f"Adding department named {dept.name} with ${dept.basePay} base pay and population {dept.population}.")
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text("INSERT INTO dept (dept_name, base_pay, dept_populus) VALUES (:name, :pay, :popul)"),
            {"name": dept.name, "pay": dept.basePay, "popul": 0}
        )
        print("Done")
    return {"status": "OK"}



@router.get("/department/total_pay")
def get_total_department_pay(department_name: str):
    """
    Returns the total pay for all employees in the specified department
    """
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text("SELECT SUM(pay) FROM employees WHERE department = :department_name"),
            {"department_name": department_name}
        ).fetchone()

        if not result or result[0] is None:
            raise HTTPException(status_code=404, detail="Department not found or no employees in the department")

        total_pay = result[0]
        
        print(f"Total pay for department {department_name} is: ${total_pay:.2f}")
        return {"department": department_name, "total_pay": total_pay}
