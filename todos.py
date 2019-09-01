import os
import sys
import fire
import code
import sqlite3
from datetime import datetime
# from termcolor import colored
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')
conn = sqlite3.connect(DEFAULT_PATH)

sql_todos = """
  CREATE TABLE IF NOT EXISTS todos(
    id INTEGER PRIMARY KEY,
    body TEXT NOT NULL,
    due_date TEXT NOT NULL DEFAULT "",
    status TEXT DEFAULT "incomplete",
    user_id INTERGER
    project_id INTEGER
  )
"""
sql_users = """
  CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
  )

"""
sql_projects = """
  CREATE TABLE IF NOT EXISTS projects(
    id INTEGER PRIMARY KEY,
    name TEXT
  )
"""


cur = conn.cursor()
cur.execute(sql_todos)
cur.execute(sql_users)
cur.execute(sql_projects)


def show_help_menu():
    # os.system('cls' if os.name == 'nt' else 'clear')
    print('Todo List Options')
    print("*"*18)
    print("__List all todos: ")
    print("python todos.py --list")
    print("-"*23)
    print("__List all todos in reverse order: ")
    print("python todos.py --list all d")
    print("-"*23)
    print("__List completed todos: ")
    print("python todos.py --list done")
    print("-"*23)
    print("__List completed todos in reverse: ")
    print("python todos.py --list done d")
    print("-"*23)
    print("__List not completed todos: ")
    print("python todos.py --list not-done")
    print("-"*23)
    print("__List not completed todos in reverse: ")
    print("python todos.py --list not-done d")
    print("-"*23)
    print("__List all todos in a project: ")
    print('python todos.py --list project project_id <a/d> (for sorted by due_date)')
    print("-"*23)
    print("__Add a new todo: ")
    print('python todos.py --add', '"My Todo Body"')
    print("-"*23)
    print("__Delete a todo: ")
    print("python todos.py --delete 1")
    print("-"*23)
    print("__Mark a todo complete: ")
    print("python todos.py --do 1")
    print("-"*23)
    print("__Mark a todo uncomplete: ")
    print("python todos.py --undo 1")
    print("-"*23)
    print("__Modify a todo body: ")
    print('python todos.py --update id', '"My new Todo Body"')
    print("-"*23)
    print("__Add user_id to a todo: ")
    print('python todos.py --add_user_id user-id todo-id')
    print("-"*23)
    print("__Add a user to system: ")
    print('python todos.py --add_user name email')
    print("-"*23)
    print("__Add a project to system: ")
    print('python todos.py --add_project name')
    print("-"*23)
    print("__List Projects with staff name: ")
    print('python todos.py --staff')


def handle_arg_errors(cmd):
    print(f'Wrong {cmd} arguments. See options belows:')
    print("*"*40)
    show_help_menu()


def validate_todos_id(id):
    sql = """
        SELECT id FROM todos
        """
    cur.execute(sql)
    results = cur.fetchall()
    # print(type(results[2]))
    for tup1 in results:
        # extract int from tuple
        num = tup1[0]
        if id == num:
            return id
    return None


def validate_proj_id(id):
    sql = """
        SELECT id FROM projects
        """
    cur.execute(sql)
    results = cur.fetchall()
    # print(type(results[2]))
    for tup1 in results:
        # extract int from tuple
        num = tup1[0]
        if id == num:
            return id
    return None


def validate_user_id(id):
    sql = """
        SELECT id FROM users
        """
    cur.execute(sql)
    results = cur.fetchall()
    # print(type(results[2]))
    for tup1 in results:
        # extract int from tuple
        num = tup1[0]
        if id == num:
            return id
    return None


def print_results(results, table=None):
    try:
        print_result = results
        if table == None:
            print(len(print_result), 'todos')
        else:
            print(len(print_result), table)
        for row in print_result:
            print(row)
    except:
        print("can not find results")


def add(body, due_date, project_id=None, *addTodos):

    if body == None and due_date == None and project_id == None:
        handle_arg_errors("--add")
    elif due_date == None and project_id == None:
        handle_arg_errors("--add")
    elif project_id == None:
        sql = """
            INSERT INTO `todos` (body,due_date)
            VALUES (?,?);
            """
        cur.execute(sql, (body, due_date,))
        conn.commit()
    else:
        sql = """
            INSERT INTO `todos` (body,due_date,project_id)
            VALUES (?,?,?);
            """
        cur.execute(sql, (body, due_date, project_id))
        conn.commit()
    print("Successfully Add New Todos")


def lists(thingy=None, d=None, *listTodo):
    print("extra argument", listTodo)
    print("argument", thingy, d)
    results = []
    if thingy == None and d == None:
        sql = """
          SELECT * FROM todos
          ORDER BY due_date
        """
        cur.execute(sql)
        results = cur.fetchall()
    elif thingy == "all" and d == "d":
        sql = """
          SELECT * FROM todos
          ORDER BY due_date DESC
        """
        cur.execute(sql)
        results = cur.fetchall()
    elif thingy == "done" and d == "d":
        sql = """
        SELECT * FROM todos
        WHERE status = ?
        ORDER BY due_date DESC
        """
        cur.execute(sql, ("completed",))
        results = cur.fetchall()
    elif thingy == "done" and d == None:
        sql = """
            SELECT * FROM todos
            WHERE status = ?
            ORDER BY due_date ASC
            """
        cur.execute(sql, ("completed",))
        results = cur.fetchall()

    elif thingy == "not-done" and d == None:
        sql = """
        SELECT * FROM todos
        WHERE status = ?
        ORDER BY due_date ASC
        """
        cur.execute(sql, ("incompleted",))
        results = cur.fetchall()
    elif thingy == "not-done" and d == "d":
        sql = """
        SELECT * FROM todos
        WHERE status = ?
        ORDER BY due_date DESC
        """
        cur.execute(sql, ("incompleted",))
        results = cur.fetchall()
    elif thingy == "project" and d != None and listTodo[0] == "d":
        val = validate_proj_id(d)
        if val:
            sql = """
                SELECT body, due_date,status,project_id,projects.name AS "proj name"
                FROM todos 
                INNER JOIN projects
                ON todos.project_id = projects.id
                WHERE project_id = ?
                ORDER BY due_date DESC
            """
            cur.execute(sql, (d,))
            results = cur.fetchall()
        else:
            print(f"project #{d} not exist")
    elif thingy == "project" and d != None and listTodo[0] == "a":
        val = validate_proj_id(d)
        if val:
            sql = """
                SELECT body, due_date,status,project_id,projects.name AS "proj name"
                FROM todos 
                INNER JOIN projects
                ON todos.project_id = projects.id
                WHERE project_id = ?
                ORDER BY due_date ASC
            """
            cur.execute(sql, (d,))
            results = cur.fetchall()
        else:
            print(f"project #{d} not exist")
    else:
        handle_arg_errors("--list")

    print_results(results)


def delete(*deleteTodos):
    val = validate_todos_id(deleteTodos[0])
    if val:
        sql = """
          DELETE FROM todos WHERE id = ?;
        """
        cur.execute(sql, (val,))
        conn.commit()
        print(f'Successfully delete todo #{val}')
    else:
        print(f"todo #{deleteTodos[0]} not exist")


def do(*doneTodo):
    val = validate_todos_id(doneTodo[0])
    if val:
        sql = """
            UPDATE todos
            SET status = ?
            WHERE id = ?;
        """
        cur.execute(sql, ("completed", val,))
        conn.commit()
        print(f'Successfully completed todo #{val}')
    else:
        print(f"todo #{doneTodo[0]} not exist")


def undo(*undoneTodo):
    val = validate_todos_id(undoneTodo[0])
    if val:
        sql = """
            UPDATE todos
            SET status = ?
            WHERE id = ?;
        """
        cur.execute(sql, ("incompleted", val,))
        conn.commit()
        print(f'Successfully postpone todo #{val}')
    else:
        print(f"todo #{undoneTodo[0]} not exist")


def update(*updateTodo):
    val = validate_todos_id(updateTodo[0])
    body = updateTodo[1]
    if val:
        sql = """
            UPDATE todos
            SET body = ?
            WHERE id = ?;
        """
        cur.execute(sql, (body, val,))
        conn.commit()
        print(f'Successfully update todo #{id}')
    else:
        print(f"todo #{updateTodo[0]} not exist")


def add_user_id(*addUserId):
    todo_id = validate_todos_id(addUserId[1])
    user_id = validate_user_id(addUserId[0])
    if todo_id and user_id:
        sql = """
            UPDATE todos
            SET user_id = ?
            WHERE id = ?;
        """
        cur.execute(sql, (user_id, todo_id,))
        conn.commit()
        print(f'Successfully add user #{addUserId[0]} to todo #{addUserId[1]}')
    else:
        print(f"todo #{addUserId[1]} or user #{addUserId[0]} are not existed.")


def add_user(*addUser):
    name = addUser[0]
    email = addUser[1]
    sql = """
        INSERT INTO `users` (name,email)
        VALUES (?,?);
        """
    cur.execute(sql, (name, email,))
    conn.commit()
    print("Successfully Add user")


def add_project(*addProject):
    name = addProject[0]
    sql = """
        INSERT INTO `projects` (name)
        VALUES (?);
        """
    cur.execute(sql, (name,))
    conn.commit()
    print("Successfully Add projects")


def list_user(*listUser):
    sql = """
      SELECT * FROM users
      ORDER BY id
    """
    cur.execute(sql)
    results = cur.fetchall()
    print_results(results, "users")


def list_project(*listProject):
    sql = """
      SELECT * FROM projects
      ORDER BY id
    """
    cur.execute(sql)
    results = cur.fetchall()
    print_results(results, "projects")


def staff(*staffTodo):
    sql = """
        SELECT projects.name,users.name
        FROM todos
        LEFT JOIN users
        ON todos.user_id = users.id
        LEFT JOIN projects
        ON project_id = projects.id
        ORDER BY projects.name;
    """
    cur.execute(sql)
    results = cur.fetchall()
    print_results(results, "lines")


def who_to_fire(*wtfTodo):
    sql = """
        SELECT id, name FROM users
        WHERE id NOT IN
            (SELECT DISTINCT T.user_id
            FROM todos T);
    """
    cur.execute(sql)
    results = cur.fetchall()
    print_results(results, "person")


def helps():
    show_help_menu()


if __name__ == '__main__':
    try:
        arg1 = sys.argv[1]
        # print("arg1[1] == --help", arg1)
        if arg1 == "--help":
            show_help_menu()
        else:
            fire.Fire({
                '--list': lists,
                '--add': add,
                '--delete': delete,
                '--do': do,
                '--undo': undo,
                '--update': update,
                '--add_user_id': add_user_id,
                '--add_user': add_user,
                '--add_project': add_project,
                '--list_user': list_user,
                '--list_project': list_project,
                '--staff': staff,
                '--who_to_fire': who_to_fire,
                '--help': helps
            })
    except IndexError:
        print("Argument Error! Look like you don't provide enough argument. Type <python todos.py --help>  for more information")
        # print("IndexError", sys.exc_info())
