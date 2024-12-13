from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/employee",
    tags=["employee"],
    dependencies=[Depends(auth.get_api_key)],
)


class Employee(BaseModel):
    id: int
    name: str
    skills: list[str]
    pay: float
    department: str
    level: int


@router.get("/stats", response_model=Employee)
def get_employee_stats(emp_id: int):
    #Execution Time: 27ms
    with db.engine.begin() as connection:
        try:
            result = connection.execute(
                sqlalchemy.text("SELECT id, name, skills, pay, department, level FROM employees WHERE id = :id"),
                {"id": emp_id}).one()
        except sqlalchemy.exc.NoResultFound:
            raise HTTPException(status_code=404, detail=f"Employee with id {emp_id} not found")
        
        result_id,result_name, result_skills, result_pay, result_department, result_level = result
        return Employee(
            id=result_id,
            name=result_name,
            skills=result_skills,
            pay=result_pay,
            department=result_department,
            level=result_level
        )

@router.get("/{employee_id}/get")
def get_all_employee_stats():
    #Execution Time: 61.287ms
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("""
        CREATE INDEX IF NOT EXISTS idx_employees_composite 
        ON employees(id, name, department, level)
        """))

        employees = connection.execute(
            sqlalchemy.text("SELECT id, name, skills, pay, department, level FROM employees")
        ).fetchall()
        
        return [
            Employee(
                id=e.id,
                name=e.name,
                skills=e.skills,
                pay=e.pay,
                department=e.department,
                level=e.level
            ) for e in employees
        ]


@router.post("/add")
def add_new_employee(name: str, skills: list[str], department: str):
    #Execution Time: 6.97ms
    """
    Add a new employee to the Database
    """
    with db.engine.begin() as connection:
        try:
            # Fetch base_pay from the department
            result = connection.execute(
                sqlalchemy.text("SELECT base_pay FROM dept WHERE dept_name = :dept_name"), 
                {"dept_name": department}
            ).fetchone()
            
            if result is None:
                raise HTTPException(status_code=404, detail="Department not found")

            # Extract base_pay value
            pay = result[0]  # result is a tuple, we take the first element which is base_pay

            print(f"Adding employee named {name} with {skills} skills being paid ${pay} to work in the {department} department")

            # Insert new employee
            connection.execute(
                sqlalchemy.text("INSERT INTO employees (name, skills, pay, department, level) VALUES (:name, :skills, :pay, :department, :level)"),
                {"name": name, "skills": skills, "pay": pay, "department": department, "level": 0}
            )
         
            # Update department population
            connection.execute(
                sqlalchemy.text("UPDATE dept SET dept_populus = dept_populus + 1 WHERE dept_name = :dept_name"),
                {"dept_name": department}
            )
            id = connection.execute(sqlalchemy.text("SELECT id FROM employees WHERE name = :name AND skills = :skills AND department = :department"),
            {"name": name, "skills": skills, "department": department}).scalar()
            print("Done")
            return {"id": id}
        
        except Exception as e:
            print(f"An error occurred: {e}")
            raise HTTPException(status_code=500, detail="You are trying to add an employee to a department that might not exist")


@router.delete("/{employee_id}/delete")
def fire_employee(employee_id: int):
    #Execution Time: 0.905ms
    """
    Removes a specific employee from the database based on the employee_id passed in
    """
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text("""
                CREATE INDEX IF NOT EXISTS idx_employees_id 
                ON employees(id)
            """)
        )
        connection.execute(
            sqlalchemy.text("""
                CREATE INDEX IF NOT EXISTS idx_dept_name 
                ON dept(dept_name)
            """)
        )
      
        to_be_fired = connection.execute(
            sqlalchemy.text("SELECT id, name, skills, pay, department, level FROM employees WHERE id = :id"), 
            {"id": employee_id}
        ).fetchone()

        if not to_be_fired:
            raise HTTPException(status_code=404, detail="Employee not found")    
        department = to_be_fired[4]
        
    
        days_employed = connection.execute(
            sqlalchemy.text("SELECT EXTRACT(DAY FROM AGE(NOW(), hire_date))::INTEGER FROM employees WHERE id = :id"),
            {"id": employee_id}
        ).scalar_one()
        
        wage = to_be_fired[3]
        print(f"This employee will be fired: {to_be_fired}")
    log_employee_history(employee_id, days_employed, wage, department)
    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text("DELETE FROM employees WHERE id = :id"), 
            {"id": employee_id}
        )         

        connection.execute(
            sqlalchemy.text("UPDATE dept SET dept_populus = dept_populus - 1 WHERE dept_name = :dept_name"), 
            {"dept_name": department}
        )
        
    return {"status": f"Successfully fired the employee with id {employee_id}"}


@router.post("/{employee_id}/promote")
def promote_employee(employee_id: int):
    #Execution Time: 1.596ms
    """
    Promotes an employee by increasing their level by 1 and increasing their pay by approximately 7%
    """
    with db.engine.begin() as connection:
        employee = connection.execute(
            sqlalchemy.text("SELECT id, name, skills, pay, department, level FROM employees WHERE id = :id"), 
            {"id": employee_id}
        ).fetchone()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
            
        days_employed = connection.execute(sqlalchemy.text("SELECT EXTRACT(DAY FROM AGE(NOW(), hire_date))::INTEGER FROM employees WHERE id = :id"),
        {"id":employee_id}).scalar_one()
     
        new_level = employee[5] + 1  # Increment the level
        new_pay = round(employee[3] * 1.07, 2)  # Increase pay by 7% and round to 2 decimal places
        old_pay = employee[3]
        # Update the employee's level and pay
        connection.execute(
            sqlalchemy.text("UPDATE employees SET level = :level, pay = :pay, hire_date = NOW() WHERE id = :id"),
            {"level": new_level, "pay": new_pay, "id": employee_id}
        )

        print("Logging changes")
        department = employee[4]
    log_employee_history(employee_id, days_employed, old_pay, department)


    return {"status": "OK", "new_level": new_level, "new_pay": new_pay}


@router.post("/{employee_id}/demote")
def demote_employee(employee_id: int):
    #Execution Time: 0.495ms
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
        old_pay = employee[3]
        days_employed = connection.execute(sqlalchemy.text("SELECT EXTRACT(DAY FROM AGE(NOW(), hire_date))::INTEGER FROM employees WHERE id = :id"),
        {"id":employee_id}).scalar_one()

        # Update the employee's level and pay
        connection.execute(
            sqlalchemy.text("UPDATE employees SET level = :level, pay = :pay, hire_date = NOW() WHERE id = :id"),
            {"level": new_level, "pay": new_pay, "id": employee_id}
        )

        print("Logging changes")
        department = employee[4]
    log_employee_history(employee_id, days_employed, old_pay, department)

    print(f"Demoted employee: {employee[1]} to level {new_level} with new pay: ${new_pay}")
 
    return {"status": "OK", "new_level": new_level, "new_pay": new_pay}


@router.post("/{employee_id}/transfer")
def transfer_employee(employee_id: int, new_department: str):
    #Execution Time: 0.232ms
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
        days_employed = connection.execute(sqlalchemy.text("SELECT EXTRACT(DAY FROM AGE(NOW(), hire_date))::INTEGER FROM employees WHERE id = :id"),{"id":employee_id}).scalar_one()

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
            sqlalchemy.text("UPDATE employees SET department = :new_department, pay = :new_pay, level = :new_level, hire_date = NOW() WHERE id = :id"),
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
        print("Logging changes")
        old_pay = employee[3]
    log_employee_history(employee_id, days_employed, old_pay, current_department)

    print(f"Transferred employee: {employee[1]} to new department {new_department} with new pay: ${new_base_pay} and level reset to 0")
    return {"status": "OK", "new_department": new_department, "new_pay": new_base_pay, "new_level": 0}


#Note: in order to get the days employed we could use DATEDIFF(NOW(),created_at)
@router.post("{employee_id}/log_history")
def log_employee_history(emp_id: int, days_employed: int, day_wage: float, in_dept: str):
    #Execution Time: .027ms
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
                sqlalchemy.text("""
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
            return {"status": f"Successfully logged history for {employee[1]}"}

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while logging the employee's history")


@router.get("/{employee_id}/total_paid")
def get_total_paid_by_employee(emp_id: int):
    #Execution Time: 85.185ms
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
        response = {
            "total_paid": round(total_paid, 2),
            "total_paid_by_department": formatted_department_totals
        }

        print(f"Total paid for employee {emp_id}: {response}")
        return {"status": "OK", "data": response}
