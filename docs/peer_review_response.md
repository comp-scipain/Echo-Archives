## Test Results (Zoila Kanu) #25 

We were unable to reproduce the forbidden error described in any of the test cases described. It looks like the error might be caused by Postman.

## Product Ideas (Zoila Kanu) #24
We implemented something somewhat similar to the suggested `GET /employee/{employee_id}/company_job_history`, but it's a built-in function `log_employee_history` that gets called whenever an employee get promoted, demoted, or transferred.

We decided to not implement giving employees off due to time constraints. 


## Product ideas (Carson Olander) #23 

Didn't add either product idea due to time constraints.

## Schema/API Design Comments (Zoila Kanu) #22 

We added some error handling where it makes sense, fixed some of the typos, updated the APISpec to better reflect the current state of the project, and other changes to help improve readability and consistency. Regarding the comment about adding a level constraint (i.e only positive integers) we decided to not make that. Since level represents an increase/decrease in pay and the way that pay change is calculated it will approach 0, but never actually reach 0. So we didn't feel like it was necessary to make level only positive integers We also added a way to track how long an Employee has been with the company. We will not be adding a fire_date since we defined being fired as being erased from the database. Regarding the use of the NULL constraint the comment was incomplete and we have no idea what to make of it.

## Code Review Comments (Zoila Kanu) #21 

Changed the names of a couple variables to make slightly more sense as suggested.

## Product Ideas (Sue Sue) #20 

We did not add either a comprehensive review system or a proper budget audit for a department. However, we did add promotions and demotions with a subsequent bonus or pay cut and an endpoint that returns how much each department is spending.

## Test Results (Sue Sue) #19 

Test case 1 works as intended, but as mention the `/employee/add` endpoint is limited to adding one employee at a time. We won't modify it to allow for batch additions due to time constraints.
Test case 2 works as intended. We also changed `/employee/get` so that it also returns employee id.
Test case 3 mostly works as intended. Running this test case exposed a mistake in our schema that has been fixed (emp_name in the history was mistakenly set to be unique).

## Code Review Comments (Sue Sue) #18 



## Schema/API Design Comments (Sue Sue) #17 

Fixed the naming conflict in dept table, added missing commas, changed the data types and names of some fields to be more consistent and make more sense in schema.sql. Also added some important notes and added more specific URLS to APISpec.md and the project. Also added some missing response and request bodies in the APISpec.

## Test results (Carson Olander) #16 



## Schema/API Design comments (Carson Olander) #15 



## Code Review Comments (Tracy Huang) #13 

Implemented some of the reformating suggestions to help with readability that can be done quickly. Other suggestions like using aggregate functions will not be implement due to a lack of time. Regarding the comment about inconsistency of dept_populus, that function was partially rewritten since before a "department" object was used as a parameter. Now, it uses a name and base pay.

## Code Review Comments (Carson Olander) #12

