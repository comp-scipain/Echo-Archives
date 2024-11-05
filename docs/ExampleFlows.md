Example Flow 1: 

John Apple is the COO of a small tech company and needs a way to keep track of his employees. First, John creates a department to track by calling `POST /Departments/new/`. He's also going to need to add all of his employees to the database using `POST /employee/add`. After setting everything up he's curious about how much money all employees per given department is being payed. So he calls `GET /Departments/department/total_pay` which tells him that the marketing department is being payed 18,523,691.45 in total. Which can help him decide whether he should reduce the number of employees working that department or not.

Example Flow 2:

Kevin Coopa is the president of a video game development company who's been using our app for a little while. A need to move a couple employees to the legal department for upcoming lawsuit. So he calls `POST /employee/transfer` to transfer various qualified employees from other departments to the Legal department. After winning the lawsuit, he decides that the employees that worked on it deserve a promotion. So he uses `POST /employee/promote` to give those employees a promotion which raises their pay by 7%. 

Example Flow 3:

Macrohard, the largest AI company in the world, is struggling to expand due to current economic conditions. So they must downsize in order to maintain profits. So they call `GET /Departments/department/total_pay` to assess how much all the employees in each department is being payed. After some deliberation, they call `POST /employee/delete` to remove a few employees from the database and call `POST /employee/demote` to reduce the pay of some their remaining employees by 7%.