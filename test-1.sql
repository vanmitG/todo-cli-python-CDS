-- SQLite

SELECT id, name FROM users
WHERE id NOT IN
(SELECT DISTINCT T.user_id
FROM todos T)





