## Test Case 1

Two different users try to calculate the department's total pay simultaneously when one employee's salary is being updated. The results might need to be more consistent because the first user sees the old wage, and the second sees the new one. The summation of all employee salaries gives the total pay, and if any update happens during the calculation, then this leads to a wrong result. This represents a non-repeatable read phenomenon where reading the same data twice yields different results.

## Test Case 2

A user tries to retrieve the total paid amount across all the departments from the history records while the new employee payment records are added. During this calculation, which combines data from the history table, new records may be inserted. This turns into a phantom read since additional records would appear during the calculation, which may result in incorrect totals in the department's payment history.

## Test Case 3

The user attempts to update a department's population count while another transaction tries to modify the same department's population. Both transactions read the initial population value, perform their calculations, and attempt to save the new value. Without proper controls, one of these updates could be lost as both transactions work with the same initial value, unaware of each other's changes. This represents a lost update phenomenon where concurrent modifications lead to data loss.
