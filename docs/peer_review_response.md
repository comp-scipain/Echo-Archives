## Test Results (Zoila Kanu) #25 

We were unable to reproduce the forbidden error described in any of the test cases described. It looks like the error might be caused by Postman.

## Product Ideas (Zoila Kanu) #24
We implemented something somewhat similar to the suggested `GET /employee/{employee_id}/company_job_history`, but it's a built-in function `log_employee_history` that gets called whenever an employee get promoted, demoted, or transferred.

We decided to not implement giving employees off due to time constraints. 


## Product ideas (Carson Olander) #23 

Didn't add either product idea due to time constraints.

## Schema/API Design Comments (Zoila Kanu) #22 

We added some error handling where it makes sense, fixed some typos, updated the APISpec to better reflect the current state of the project, and other changes to help improve readability and consistency. Regarding the comment about adding a level constraint (i.e only positive integers) we decided to not make that. Since level represents an increase/decrease in pay and the way that pay change is calculated it will approach 0, but never actually reach 0. So we didn't feel like it was necessary to make level only positive integers We also added a way to track how long an Employee has been with the company. We will not be adding a fire_date since we defined being fired as being erased from the database. Regarding the use of the NULL constraint the comment was incomplete and we have no idea what to make of it.

## Code Review Comments (Zoila Kanu) #21 

Changed the names of a couple variables to make slightly more sense as suggested. Also implemented other smaller suggestions such as the use of one() instaed of fetchone() since we only need to return a single row. We will not implement some of the SQL suggestions again due to time constraints.

## Product Ideas (Sue Sue) #20 

We added a review system and budget audit for a department. However, they don't function exactly how the suggestion described.

## Test Results (Sue Sue) #19 

Test case 1 works as intended, but as mention the `/employee/add` endpoint is limited to adding one employee at a time. We won't modify it to allow for batch additions due to time constraints.
Test case 2 works as intended. We also changed `/employee/get` so that it also returns employee id.
Test case 3 mostly works as intended. Running this test case exposed a mistake in our schema that has been fixed (emp_name in the history was mistakenly set to be unique).

## Code Review Comments (Sue Sue) #18 

We added more detailed error messages, and changed a couple paths to keep things consistent as suggested (i.e /Departments to /departments). We won't be adding a boundary check for new_pay in Employee.py. After some testing, we found that the amount new_pay decreases by after each demotion decreases as it approaches 0 and it will stop decreasing once it reaches $0.07. The only way new_pay can be negative is if the user enters a negative base_pay in `departments/add`. Which we now have a check for. We also implemented the suggestion of giving additional context to endpoints that only returned "status":"OK".

## Schema/API Design Comments (Sue Sue) #17 

Fixed the naming conflict in dept table, added missing commas, changed the data types and names of some fields to be more consistent and make more sense in schema.sql. Also added some important notes and added more specific URLS to APISpec.md and the project. Also added some missing response and request bodies in the APISpec. Also the reason why pay and level aren't parameters for `/employee/add` is because those attributes are not exactly determined by the user. Pay is dependent on the base pay for whatever department they end up being added to and level always starts at 0.

## Test results (Carson Olander) #16 

In test Case 1 the reason why it returned an error is that you were trying to add an employee to a department that doesn't exist. We changed the error message to make this fact more clear.
New test Case 2 works as intended.
New test Case 3 works as intended.

## Schema/API Design comments (Carson Olander) #15 

    Schema.sql - dept_id twice in creating table. 
    - Fixed (removed the duplicate dept_id)

    Schema.sql - employee.id should be employee_id to keep consistency.
    - Fixed (changed employee.id to employee_id)

    Schema.sql - not ideal to store skills as a single column because it is a list and will require parsing to access specific skills within the list, additionally filtering queries on the skills column more difficult.
    - Won't implement since we skills aren't really used so we don't have to worry.

    Schema.sql - could add employee's manager as a column.
    - Won't implement due to time constraints.

    Schema.sql - employee table column department should have a foreign key reference to the dept_id column in the dept table.
    - Won't implement due to time constraints.

    APISpec.md - Promote Employee return value doesn't match what is returned in the corresponding function in Employee.py
    - Fixed (Made sure that return value matches what's returned in the corresponding function)

    APISpec.md - Demote Employee return value doesn't match what is returned in the corresponding function in Employee.py
    - Fixed (Made sure that return value matches what's returned in the corresponding function)

    APISpec.md - New Department takes in a parameter for department population but should be hard coded to 0 because in the database there won't be any employees in that 
    department yet.
    - Fixed (Removed department population parameter since it is hard coded to start at 0)

    APISpec.md - Transfer Employee return value doesn't match what is returned in the corresponding function in Employee.py
    - Fixed (Made sure that return value matches what's returned in the corresponding function)

    APISpec.md - Multiple POST specifications missing the expected "Response" body.
    - Fixed (Added missing Response body)

    APISpec.md - Fire Employee missing expected Request and Response bodies.
    - Fixed (Added missing expected Request and Response bodies)

    APISpec.md - Reset app - missing expected Request and Response bodies.
    - Fixed (Added missing expected Request and Response bodies)


## Code Review Comments (Tracy Huang) #13 

Implemented some of the reformating suggestions to help with readability that can be done quickly. Other suggestions like using aggregate functions will not be implement due to a lack of time. Regarding the comment about inconsistency of dept_populus, that function was partially rewritten since initially a "department" object was used as a parameter forcing the user to specify a population that would later get overwritten. Now, it uses a name and base pay. We also added a unique constraint to dept_name as suggested. Some of the other suggestions won't be implemented due to time constraints.

## Code Review Comments (Carson Olander) #12


    Employee.py - NewEmployee class is unnecessary since it is only used once to create a new employee. Instead just use parameters to pass in needed values.
    - We implemented this exact suggestion.

    Employee.py - in add_new_employee() method the base_pay can be passed as a SELECT for the pay in the VALUES part of the INSERT when creating the new employee instead of returning it as result to store in python and then passing it in.
    - Won't implement due to time constraints.

    Employee.py - in fire_employee instead of doing a SELECT query for the employee that will be fired, add "RETURNING *" to the end of the DELETE query.
    - Won't implement due to time constraints.

    Employee.py - in promote_employee() instead of doing a SELECT query for the employee's level and pay to store as variable to update in python, update all values in the UPDATE query and add "RETURNING ..." for whatever values are wanted to be printed (employee's new level, employee's new pay, etc.).
    - Won't implement due to time constraints.

    Employee.py - in demote_employee() same as number 4 (promotion) but for demotion this time.
    - Won't implement due to time constraints.

    Employee.py - in transfer_employee() update employee's department and pay in UPDATE query instead of doing a SELECT query to store and update.
    - Won't implement due to time constraints.

    department.py - the Department class doesn't need a population variable because the class is currently only used to create a new department and the population of the department is hard coded to 0 in add_new_department().
    - Fixed by removing the population parameter. Since as mentioned population always starts at 0.

    department.py - can use ROUND in SQL query on the total pay rather than when printing it.
    - Implemented this exact suggestion.

    departments.py - In add_new_department() return the row inserted into the table to show important info like dept_id to the user on the swagger ui instead of only printing to the render logs.
    - We sort of implemented this suggestions. Except we don't return dept_id since it ended up being unused.

    Employee.py - In add_new_employee() return the row inserted into the table to show important info about the new employee that wasn't provided by the user like employee_id to the swagger ui instead of only printing to the render logs.
    - Implemented this exact suggestion.

    Employee.py - In get_all_employee_stats() it would be helpful to return the employee's id number to do other actions like promote, demote, fire etc.
    - Implemented this exact suggestion.

    Employee.py - In get_employee_stats() it would be helpful to return the employee's id number to do other actions like promote, demote, fire etc.
    - Implemented this exact suggestion.