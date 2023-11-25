SELECT COUNT (e.id) AS count, 
e.fname , e.lname, d.designation_name , d.num_of_leaves 
FROM employees e
JOIN leaves l
ON e.id = l.employee_id 
JOIN designation d
ON e.designation = d.designation_name 
WHERE e.id = %s
GROUP BY e.id,e.fname,e.email,d.num_of_leaves,d.designation_name;
