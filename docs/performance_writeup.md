## Fake Data Modeling

### Python Script: https://github.com/comp-scipain/Echo-Archives/blob/main/create_fake_data.py
### Explanation:
  We generated 1,000,000 rows across different tables to simulate a semi-realistic production environment.

Breakdown of data distribution:
    
    employees: 333,317 rows
    dept: 50 rows (one for each department)
    history: 333,317 rows
    reviews: 333,317 rows

### Justification:
#### Employees Table: 
Each employee represents a unique entry with a variety of skills, pay, departments, and employment levels. This mimics a large-scale organization where diversity in employee attributes is crucial.
#### Departments Table: 
We have 50 departments to cover a broad spectrum of technical fields, ensuring a semi-realistic and complex data distribution.
#### History Table: 
Captures the employment history, making it proportional to the number of employees.
#### Reviews Table: 
Provides performance review data, again proportional to the number of employees. 
The rationale behind these numbers is to ensure that our service can handle a realistic distribution of employees and their corresponding records, mirroring a large and diverse company.

## Performance results of hitting endpoints

**/employee/{employee_id}/get ENDPOINT BEFORE INDEX**
    
    Seq Scan on employees  (cost=0.00..10099.17 rows=333317 width=122) (actual time=0.053..320.924 rows=333317 loops=1)
    Planning Time: 1.751 ms
    Execution Time: 330.498 ms
    
    Endpoint took 2607.79 ms


**/employee/{employee_id}/get ENDPOINT AFTER INDEX**

    Seq Scan on employees  (cost=0.00..10099.17 rows=333317 width=122) (actual time=0.014..61.287 rows=333317 loops=1)
    Planning Time: 1.039 ms
    Execution Time: 70.674 ms
    
    Endpoint took 2807.08 ms

**/departments/total_paid get ENDPOINT BEFORE INDEX**
    
    Seq Scan on history  (cost=0.00..7809.26 rows=333326 width=36) (actual time=0.096..52.153 rows=333326 loops=1)
    Planning Time: 1.335 ms
    Execution Time: 57.388 ms
    
    Endpoint took 1219.87 ms

**/departments/total_paid get ENDPOINT AFTER INDEX**

Query Plan:
    
    Index Only Scan using idx_history_total_paid on history  (cost=0.42..15425.71 rows=333331 width=36) (actual time=0.062..47.676 rows=333331 loops=1)
      Index Cond: (in_dept IS NOT NULL)
      Heap Fetches: 273
    Planning Time: 0.109 ms
    Execution Time: 53.853 ms
    Endpoint took 1712.19 ms

**/employee/{employee_id}/delete ENDPOINT BEFORE INDEX**

Query Plan for Employee Lookup:

    Index Scan using idx_employees_composite on employees  (cost=0.42..8.44 rows=1 width=122) (actual time=2.240..2.243 rows=1 loops=1)
      Index Cond: (id = 23212)
    Planning Time: 1.283 ms
    Execution Time: 2.269 ms

Query Plan for Days Calculation:
    
    Index Scan using idx_employees_composite on employees  (cost=0.42..8.45 rows=1 width=4) (actual time=0.031..0.031 rows=1 loops=1)
      Index Cond: (id = 23212)
    Planning Time: 0.038 ms
    Execution Time: 0.040 ms
    Endpoint took 8.45 ms

Query Plan for Delete Operation:
    
    Delete on employees  (cost=0.42..8.44 rows=0 width=0) (actual time=0.026..0.027 rows=0 loops=1)
      ->  Index Scan using idx_employees_composite on employees  (cost=0.42..8.44 rows=1 width=6) (actual time=0.008..0.009 rows=1 loops=1)
            Index Cond: (id = 23212)
    Planning Time: 0.068 ms
    Execution Time: 0.124 ms

Query Plan for Department Update:
    
    Update on dept  (cost=0.00..3436.63 rows=0 width=0) (actual time=7.385..7.385 rows=0 loops=1)
      ->  Seq Scan on dept  (cost=0.00..3436.63 rows=1 width=10) (actual time=7.350..7.356 rows=1 loops=1)
            Filter: (dept_name = 'Data Science'::text)
            Rows Removed by Filter: 51
    Planning Time: 0.950 ms
    Execution Time: 7.432 ms
Done!

**/employee/{employee_id}/delete ENDPOINT AFTER INDEX**

Query Plan for Employee Lookup:
    
    Index Scan using idx_employees_id on employees  (cost=0.42..8.44 rows=1 width=122) (actual time=0.151..0.152 rows=1 loops=1)
      Index Cond: (id = 84543)
    Planning Time: 2.372 ms
    Execution Time: 0.185 ms

Query Plan for Days Calculation:
    
    Index Scan using idx_employees_id on employees  (cost=0.42..8.45 rows=1 width=4) (actual time=0.034..0.035 rows=1 loops=1)
      Index Cond: (id = 84543)
    Planning Time: 0.123 ms
    Execution Time: 0.071 ms
    This employee will be fired: (84543, 'Joshua Mccoy', ['Ethical Hacking', 'Design Patterns'], 89740.305, 'Data Analytics', 1)
    Logged history for employee: Joshua Mccoy
    Endpoint took 3.48 ms

Query Plan for Delete Operation:
    
    Delete on employees  (cost=0.42..8.44 rows=0 width=0) (actual time=0.460..0.461 rows=0 loops=1)
      ->  Index Scan using idx_employees_id on employees  (cost=0.42..8.44 rows=1 width=6) (actual time=0.016..0.018 rows=1 loops=1)
            Index Cond: (id = 84543)
    Planning Time: 0.089 ms
    Execution Time: 0.648 ms

Query Plan for Department Update:
    
    Update on dept  (cost=0.14..8.17 rows=0 width=0) (actual time=0.030..0.030 rows=0 loops=1)
      ->  Index Scan using idx_dept_name on dept  (cost=0.14..8.17 rows=1 width=10) (actual time=0.015..0.016 rows=1 loops=1)
            Index Cond: (dept_name = 'Data Analytics'::text)
    Planning Time: 0.730 ms
    Execution Time: 0.050 ms
    
    Endpoint took 26.95 ms


## Performance tuning

For each of the three slowest endpoints, the following steps were taken to analyze and improve performance. Each endpoint was optimized by adding appropriate indexes and re-running the queries to measure improvements.

/employee/{employee_id}/get

  ```sql
      Initial EXPLAIN output showed full table scan.
      Added index on department and name.
      New EXPLAIN output showed reduced execution time.
  ```

/departments/total_paid

  ```sql
      Initial EXPLAIN output showed full table scan.
      
      Added index on in_dept.
      
      New EXPLAIN output showed reduced execution time.
  ```

/employee/{employee_id}/delete

  ```sql
      Initial EXPLAIN output showed multiple scans and operations.
      Added index on id for employees.
      Added index on dept_name for departments.
      New EXPLAIN output showed reduced execution time.
  ```
