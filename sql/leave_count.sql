SELECT COUNT(l.employee_id), e.fname, e.lname, e.id 
FROM employees e 
JOIN leaves l ON e.id = l.employee_id 
WHERE e.id = %s
GROUP BY e.id, e.fname, e.lname, l.employee_id;

