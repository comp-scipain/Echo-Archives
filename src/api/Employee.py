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


class NewEmployee(BaseModel):
    name: str
    skills: list[str]
    department: str


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
            {"id": emp_id}).fetchone()
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
            sqlalchemy.text("SELECT name, skills, pay, department, level FROM employees")).fetchall()
        if not employees:
            raise HTTPException(status_code=404, detail="No employees found")
        return [Employee(name=e.name, skills=e.skills, pay=e.pay, department=e.department, level=e.level) for e in employees]


@router.post("/add")
def add_new_employee(employee: NewEmployee):
    """
    Add a new employee to the Database
    """
    with db.engine.begin() as connection:
        try:
            # Fetch base_pay from the department
            result = connection.execute(
                sqlalchemy.text("SELECT base_pay FROM dept WHERE dept_name = :dept_name"), 
                {"dept_name": employee.department}
            ).fetchone()
            
            if result is None:
                raise HTTPException(status_code=404, detail="Department not found")

            # Extract base_pay value
            pay = result[0]  # result is a tuple, we take the first element which is base_pay

            print(f"Adding employee named {employee.name} with {employee.skills} skills being paid ${pay} to work in the {employee.department} department")

            # Insert new employee
            connection.execute(
                sqlalchemy.text("INSERT INTO employees (name, skills, pay, department, level) VALUES (:name, :skills, :pay, :department, :level)"),
                {"name": employee.name, "skills": employee.skills, "pay": pay, "department": employee.department, "level": 0}
            )

            # Update department population
            connection.execute(
                sqlalchemy.text("UPDATE dept SET dept_populus = dept_populus + 1 WHERE dept_name = :dept_name"),
                {"dept_name": employee.department}
            )

            print("Done")
            return {"status": "OK"}
        
        except Exception as e:
            print(f"An error occurred: {e}")
            raise HTTPException(status_code=500, detail="An error occurred while adding the employee")


@router.post("/delete")
def fire_employee(employee_id: int):
    """
    Removes a specific employee from the database based on the employee_id passed in
    """
    with db.engine.begin() as connection:
        to_be_fired = connection.execute(
            sqlalchemy.text("SELECT id, name, skills, pay, department, level FROM employees WHERE id = :id"), {"id": employee_id}).fetchone()
        if not to_be_fired:
            raise HTTPException(status_code=404, detail="Employee not found")
        department = to_be_fired[4]
        print(f"This employee will be fired: {to_be_fired}")
        connection.execute(
            sqlalchemy.text("DELETE FROM employees WHERE id = :id"), {"id": employee_id})
        connection.execute(
            sqlalchemy.text("UPDATE dept SET dept_populus = dept_populus - 1 WHERE dept_name = :dept_name"), {"dept_name": department})
        print("Done!")
    return {"status": "OK"}


@router.post("/promote")
def promote_employee(employee_id: int):
    """
    Promotes an employee by increasing their level by 1 and increasing their pay by approximately 7%
    """
    with db.engine.begin() as connection:
        # Fetch the employee to be promoted
        employee = connection.execute(
            sqlalchemy.text("SELECT id, name, skills, pay, department, level FROM employees WHERE id = :id"), 
            {"id": employee_id}
        ).fetchone()

        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        new_level = employee[5] + 1  # Increment the level
        new_pay = round(employee[3] * 1.07, 2)  # Increase pay by 7% and round to 2 decimal places

        # Update the employee's level and pay
        connection.execute(
            sqlalchemy.text("UPDATE employees SET level = :level, pay = :pay WHERE id = :id"),
            {"level": new_level, "pay": new_pay, "id": employee_id}
        )

        print(f"Promoted employee: {employee[1]} to level {new_level} with new pay: ${new_pay}")
        return {"status": "OK", "new_level": new_level, "new_pay": new_pay}


@router.post("/demote")
def demote_employee(employee_id: int):
    """
    Demotes an employee by decreasing their level by 1 and decreasing their pay by approximately 7%
    """
    with db.engine.begin() as connection:
        # Fetch the employee to be demoted
        employee = connection.execute(
            sqlalchemy.text("SELECT id, name, skills, pay, department, level FROM employees WHERE id = :id"), 
            {"id": employee_id}
        ).fetchone()

        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        new_level = employee[5] - 1  # Decrement the level
        new_pay = round(employee[3] * 0.93, 2)  # Decrease pay by 7% and round to 2 decimal places

        # Update the employee's level and pay
        connection.execute(
            sqlalchemy.text("UPDATE employees SET level = :level, pay = :pay WHERE id = :id"),
            {"level": new_level, "pay": new_pay, "id": employee_id}
        )

        print(f"Demoted employee: {employee[1]} to level {new_level} with new pay: ${new_pay}")
        return {"status": "OK", "new_level": new_level, "new_pay": new_pay}


@router.post("/transfer")
def transfer_employee(employee_id: int, new_department: str):
    """
    Transfers an employee to a new department, resetting their pay, level, and updating dept_populus.
    """
    with db.engine.begin() as connection:
        # Fetch the current employee details
        employee = connection.execute(
            sqlalchemy.text("SELECT id, name, skills, pay, department, level FROM employees WHERE id = :id"), 
            {"id": employee_id}
        ).fetchone()

        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        current_department = employee[4]

        if current_department == new_department:
            raise HTTPException(status_code=400, detail="Employee is already in the specified department")

        # Fetch the base pay for the new department
        base_pay_result = connection.execute(
            sqlalchemy.text("SELECT base_pay FROM dept WHERE dept_name = :dept_name"), 
            {"dept_name": new_department}
        ).fetchone()

        if not base_pay_result:
            raise HTTPException(status_code=404, detail="New department not found")

        new_base_pay = base_pay_result[0]

        # Update the employee's department, pay, and level
        connection.execute(
            sqlalchemy.text("UPDATE employees SET department = :new_department, pay = :new_pay, level = :new_level WHERE id = :id"),
            {"new_department": new_department, "new_pay": new_base_pay, "new_level": 0, "id": employee_id}
        )

        # Update department populations
        connection.execute(
            sqlalchemy.text("UPDATE dept SET dept_populus = dept_populus - 1 WHERE dept_name = :dept_name"),
            {"dept_name": current_department}
        )

        connection.execute(
            sqlalchemy.text("UPDATE dept SET dept_populus = dept_populus + 1 WHERE dept_name = :dept_name"),
            {"dept_name": new_department}
        )

        print(f"Transferred employee: {employee[1]} to new department {new_department} with new pay: ${new_base_pay} and level reset to 0")
        return {"status": "OK", "new_department": new_department, "new_pay": new_base_pay, "new_level": 0}



@router.post("/search")
def search_employees():
    """
    Search for specific employees
    """
    print("Not currently implemented :(")
    raise HTTPException(status_code=501, detail="Not currently implemented")

#Note: in order to get the days employed we could use DATEDIFF(NOW(),created_at)
@router.post("/log_history")
def log_employee_history(emp_id: int, days_employed: int, day_wage: float, in_dept: str):
    """
    Logs an employee's history into the history table.
    """
    try:
        with db.engine.begin() as connection:
            employee = connection.execute(
                sqlalchemy.text("SELECT id, name FROM employees WHERE id = :id"), 
                {"id": emp_id}).fetchone()

            if not employee:
                raise HTTPException(status_code=404, detail="Employee not found")

            connection.execute(
                sqlalchemy.text("""LOCK TABLE history IN EXCLUSIVE MODE;
                    INSERT INTO history (emp_id, emp_name, days_employed, day_wage, in_dept) VALUES (:emp_id, :emp_name, :days_employed, :day_wage, :in_dept)"""),
                {
                    "emp_id": employee[0],
                    "emp_name": employee[1],
                    "days_employed": days_employed,
                    "day_wage": day_wage,
                    "in_dept": in_dept
                }
            )

            print(f"Logged history for employee: {employee[1]}")
            return {"status": "OK"}

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while logging the employee's history")


@router.get("/employee/total_paid")
def get_total_paid_by_employee(emp_id: int):
    """
    Calculates the total paid value for a specific employee by multiplying their wage by the days employed,
    and aggregates this total by department.
    """
    with db.engine.begin() as connection:
        history_records = connection.execute(
            sqlalchemy.text("SELECT days_employed, day_wage, in_dept FROM history WHERE emp_id = :emp_id"),
            {"emp_id": emp_id}
        ).fetchall()
        if not history_records:
            raise HTTPException(status_code=404, detail="No history records found for the specified employee")

        department_totals = {}
        total_paid = 0.0
        for record in history_records:
            department = record[2]
            total_paid_for_row = record[0] * record[1]  # days_employed * day_wage
            total_paid += total_paid_for_row

            if department in department_totals:
                department_totals[department] += total_paid_for_row
            else:
                department_totals[department] = total_paid_for_row

        formatted_department_totals = [
            {"department": dept, "total_paid": round(total, 2)}
            for dept, total in department_totals.items()
        ]
        employee = connection.execute(
                sqlalchemy.text("SELECT name FROM employees WHERE id = :id"), 
                {"id": emp_id}).fetchone()
        response = {
            "Employee Name": employee,
            "total_paid": round(total_paid, 2),
            "total_paid_by_department": formatted_department_totals
        }

        print(f"Total paid for employee {emp_id}: {response}")
        return {"status": "OK", "data": response}
