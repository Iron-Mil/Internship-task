import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_worker(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO workers(first_name,last_name,date_of_birth,phone_number)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid


def create_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO tasks(name,priority,done,worker_id)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    return cur.lastrowid


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = "placeholder.db"
    empty = True
    sql_create_worker_table = """ CREATE TABLE IF NOT EXISTS workers (
                                        id integer PRIMARY KEY,
                                        first_name text NOT NULL,
                                        last_name text NOT NULL,
                                        date_of_birth int NOT NULL,
                                        phone_number text NOT NULL
                                    ); """

    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    priority integer,
                                    done text NOT NULL,
                                    worker_id integer NOT NULL,
                                    FOREIGN KEY (worker_id) REFERENCES projects (id)
                                );"""
    # create a database connection
    conn = create_connection(database)
    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_worker_table)

        # create tasks table
        create_table(conn, sql_create_tasks_table)
    else:
        print("Error! cannot create the database connection.")

    with conn:
        # Checking if the database is empty
        for row in conn.execute("""SELECT * FROM workers"""):
            empty = False

        # If the database is empty, we fill it up with a default one
        if empty:

            worker = ('Milos', 'Korac', '1996', 'xxx yyy xx xx')
            worker_id = create_worker(conn, worker)

            worker = ('Pera', 'Peric', '1990', 'xyy yxx zz zz')
            worker_id_2 = create_worker(conn, worker)

            worker = ('Zika', 'Zikic', '1995', 'xyz zxy xy yx')
            worker_id_3 = create_worker(conn, worker)

            # tasks
            task_1 = ('Design the project', 2, 'Yes', worker_id)
            task_2 = ('Create the project', 1, 'No', worker_id)
            task_3 = ('Market the project', 3, 'No', worker_id_2)

            # create tasks
            create_task(conn, task_1)
            create_task(conn, task_2)
            create_task(conn, task_3)

    # Starting the main loop
    while True:
        print("What do you wish to do with the current database? (input number to select)")
        print("")
        print("1. View the workers table")
        print("2. View the tasks table")
        print("3. Add a new worker")
        print("4. Add a new task")
        print("5. Close the program")

        choice = input()
        if choice == '1':
            print("Worker table selected")
            print("{:<3} {:<11} {:<11} {:<5} {:<15}".format("ID", "First Name", "Last Name", "DoB", "Phone Number"))
            for row in conn.execute('''SELECT * FROM workers'''):
                print("{:<3} {:<11} {:<11} {:<5} {:<15}".format(row[0], row[1], row[2], row[3], row[4]))
            print("Press Enter to continue:")
            input()

        elif choice == '2':
            print("Task table selected")
            print("{:<3} {:<20} {:<10} {:<5} {:<10}".format("ID", "Name", "Priority", "Done", "Assigned to"))
            for row in conn.execute('''SELECT * FROM tasks'''):
                print("{:<3} {:<20} {:<10} {:<5} {:<10}".format(row[0], row[1], row[2], row[3], row[4]))
            print("Press Enter to continue:")
            input()

        elif choice == '3':
            print("Worker input selected")
            print("Please enter the worker's first name:")
            first_name = input()
            print("Please enter their last name:")
            last_name = input()
            print("Enter their date of birth:")
            dob = input()
            print("Finally, their phone number:")
            phone = input()

            worker = (first_name, last_name, dob, phone)
            worker_id = create_worker(conn, worker)
            print("Worker", first_name, "successfully added")
            print("Press Enter to continue:")
            input()

        elif choice == '4':
            print("Task input selected")
            print("Please enter the task in question:")
            name = input()
            print("Please enter the task's priority:")
            priority = int(input())
            print("Is the task already completed?")
            done = input()
            print("Who is it assigned to? (Insert the ID of the worker in question)")
            worker = input()

            task = (name, priority, done, worker)
            task_id = create_task(conn, task)
            print("Task", name, "successfully added")
            print("Press Enter to continue:")
            input()

        elif choice == '5':
            break

        else:
            print("Incorrect input, please try again")
            print("")
    conn.close()


if __name__ == '__main__':
    main()
