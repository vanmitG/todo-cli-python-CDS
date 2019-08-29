import os
import sys
import fire
import code
import sqlite3
from datetime import datetime
# from termcolor import colored
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')
conn = sqlite3.connect(DEFAULT_PATH)

sql = """
  CREATE TABLE IF NOT EXISTS todos(
    id INTEGER PRIMARY KEY,
    body TEXT NOT NULL,
    due_date TEXT NOT NULL,
    status TEXT DEFAULT "incomplete",
    user_id INTERGER
    project_id INTEGER
  );
  CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
  );
  CREATE TABLE IF NOT EXISTS projects(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    due_date TEXT NOT NULL,
    status TEXT DEFAULT "incomplete",
    project_id INTEGER
  )


"""

cur = conn.cursor()
cur.execute(sql)
# print("sql", sql)


def show_help_menu():
    # os.system('cls' if os.name == 'nt' else 'clear')
    print('Todo List Options')
    print("*"*18)
    print("__List all todos: ")
    print("python todos.py --list")
    print("-"*16)
    print("__List completed todos: ")
    print("python todos.py --list done")
    print("-"*16)
    print("__List not completed todos: ")
    print("python todos.py --list not-done")
    print("-"*16)
    print("__Add a new todo: ")
    print('python todos.py --add', '"My Todo Body"')
    print("-"*16)
    print("__Delete a todo: ")
    print("python todos.py --delete 1")
    print("-"*16)
    print("__Mark a todo complete: ")
    print("python todos.py --do 1")
    print("-"*16)
    print("__Mark a todo uncomplete: ")
    print("python todos.py --undo 1")
    print("-"*16)
    print("__Modify a todo body: ")
    print('python todos.py --update', '"My new Todo Body"')


def handle_arg_errors(cmd):
    print(f'Wrong {cmd} arguments. See options belows:')
    print("*"*40)
    show_help_menu()


def print_results(results):
    try:
        print_result = results
        print(len(print_result), 'todos')
        for row in print_result:
            print(row)
    except:
        print("can not find results")


def add(body):
    try:
        print("add", body)
    except:
        print("argument error, try python todos.py --help  for more information")

    sql = """

      INSERT INTO `todos` (id, body, due_date)
      VALUES (3,"finish cli","29/08/2019");

    """


def lists(thingy=None, *listTodo):
    # print("extra argument", listTodo)
    results = []
    if thingy == None:
        print("insideNone")
        sql = """
        SELECT * FROM todos
        ORDER BY due_date
        """
        cur.execute(sql)
        results = cur.fetchall()
    elif thingy == "done":
        sql = """
        SELECT * FROM todos
        WHERE status = ?
        """
        cur.execute(sql, ("complete",))
        results = cur.fetchall()
    elif thingy == "not-done":
        sql = """
        SELECT * FROM todos
        WHERE status = ?
        """
        cur.execute(sql, ("not complete",))
        results = cur.fetchall()
    else:
        handle_arg_errors("--list")

    print_results(results)


def delete():
    print("delete")


def do():
    print("do")


def undo():
    print("undo")


def update():
    print("update")


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
                '--help': helps
            })

    except IndexError:
        print("Error, try python todos.py --help  for more information")
        # print("IndexError", sys.exc_info())
