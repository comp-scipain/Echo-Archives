from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api import auth
import sqlalchemy  
from src import database as db
from datetime import datetime
import time

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
    dependencies=[Depends(auth.get_api_key)],
)

class Review(BaseModel):
    employee_id: int
    performance_score: int  # 1-5
    review_text: str
    reviewer_id: int
    review_date: datetime = datetime.now()

@router.post("/add")
def add_review(review: Review):
    #Exectuion Time: 1.385ms
    """
    Add a performance review for an employee
    """
    if not 1 <= review.performance_score <= 5:
        raise HTTPException(status_code=400, detail="Performance score must be between 1 and 5")
    
    with db.engine.begin() as conn:
        # Verify employee exists
        employee = conn.execute(
            sqlalchemy.text("SELECT name, department, level FROM employees WHERE id = :id"),
            {"id": review.employee_id}
        ).fetchone()

        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        # Add review
        conn.execute(
            sqlalchemy.text("""
            INSERT INTO reviews (employee_id, performance_score, review_text, 
                               reviewer_id, review_date)
            VALUES (:emp_id, :score, :text, :reviewer_id, :date)
            """),
            {
                "emp_id": review.employee_id,
                "score": review.performance_score,
                "text": review.review_text,
                "reviewer_id": review.reviewer_id,
                "date": review.review_date
            }
        )
  
        # If score is 1 or 2, demote employee
        if review.performance_score <= 2:
            conn.execute(
                sqlalchemy.text("UPDATE employees SET level = level - 1 WHERE id = :id"),
                {"id": review.employee_id}
            )
        # If score is 5, promote employee  
        elif review.performance_score == 5:
            conn.execute(
                sqlalchemy.text("UPDATE employees SET level = level + 1 WHERE id = :id"),
                {"id": review.employee_id}
            )
        return {"status": "OK"}

@router.get("/employee/{emp_id}")
def get_employee_reviews(emp_id: int):
    #Execution Time: 95.359ms
    """
    Get all reviews for a specific employee
    """
    with db.engine.begin() as conn:
        reviews = conn.execute(
            sqlalchemy.text("""
            SELECT r.review_date, r.performance_score, r.review_text, 
                   e.name as reviewer_name
            FROM reviews r
            JOIN employees e ON r.reviewer_id = e.id 
            WHERE r.employee_id = :emp_id
            ORDER BY r.review_date DESC
            """),
            {"emp_id": emp_id}
        ).fetchall()

        if not reviews:
            raise HTTPException(status_code=404, detail="No reviews found for employee")
  
        return [{
            "date": r[0],
            "score": r[1],
            "text": r[2],
            "reviewer": r[3]
        } for r in reviews]

@router.get("/department/{dept_name}")
def get_department_reviews(dept_name: str):
    #Execution Time: 152.635ms
    """
    Get average review scores for a department
    """
    with db.engine.begin() as conn:
        result = conn.execute(
            sqlalchemy.text("""
            SELECT e.name, AVG(r.performance_score) as avg_score,
                   COUNT(r.employee_id) as review_count
            FROM employees e
            JOIN reviews r ON e.id = r.employee_id
            WHERE e.department = :dept_name
            GROUP BY e.id, e.name
            ORDER BY avg_score DESC
            """),
            {"dept_name": dept_name}
        ).fetchall()
        
        if not result:
            raise HTTPException(status_code=404, detail="No reviews found for department")
        return [{
            "employee_name": r[0],
            "average_score": float(r[1]),
            "review_count": r[2]
        } for r in result]

@router.get("/stats")
def get_review_stats():
    #Execution Time: 356.865ms
    """
    Get overall review statistics
    """
    with db.engine.begin() as conn:
        stats = conn.execute(
            sqlalchemy.text("""
            SELECT 
                department,
                AVG(performance_score) as avg_score,
                COUNT(*) as review_count,
                MIN(performance_score) as min_score,
                MAX(performance_score) as max_score
            FROM reviews r
            JOIN employees e ON r.employee_id = e.id
            GROUP BY department
            ORDER BY avg_score DESC
            """)
        ).fetchall()
        
        if not stats:
            raise HTTPException(status_code=404, detail="No review statistics found")
        return [{
            "department": s[0],
            "average_score": float(s[1]),
            "review_count": s[2],
            "lowest_score": s[3],
            "highest_score": s[4]
        } for s in stats]
