-- SQLite
SELECT body,projects.name,users.name, 
FROM todos
LEFT JOIN users
ON todos.user_id = users.id
LEFT JOIN projects
ON project_id = projects.id
ORDER BY projects.name;
