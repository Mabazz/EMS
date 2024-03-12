import sqlite3
import logging
from decorators import handle_errors
from main import send_data


class EmsModel:
    """ 
    Manages the interaction with the SQLite database for employee information.

    This class provides an interface for database operations and implements the Observer pattern
    to notify registered observers about changes in the data model.

    Attributes:
        db_path (str): Path to the SQLite database file.
        con (sqlite3.Connection): Active database connection object.
        cursor (sqlite3.Cursor): Cursor object for executing SQL commands.
        observers (list): List of observer objects to be notified of changes.
    """


    def __init__(self, db_path):
        """
        Initializes the ModelObservable with a database path.

        Establishes a connection to the SQLite database and prepares a cursor for SQL operations.
        Initializes an empty list of observers for the Observer pattern.

        Parameters:
            db_path (str): Path to the SQLite database file.
        """
        self.db_path = db_path
        self.con = sqlite3.connect(self.db_path)
        self.cursor = self.con.cursor()
        self.observers = []


    def get_observers(self):
        """Returns the list of observers."""
        return self.observers


    def add_observer(self, observer):
        """
        Adds an observer to the list if it's not already present.

        Parameters:
            observer (object): The observer object to be added to the list.
        """
        if observer not in self.observers:
            self.observers.append(observer)


    def remove_observer(self, observer):
        """
        Removes an observer from the list.

        Parameters:
            observer (object): The observer object to be removed from the list.
        """
        self.observers.remove(observer)


    def notify_observers(self):
        """
        Notifies all registered observers of a change in the data model.

        Each observer's update method is called to handle the notification.
        """
        for observer in self.observers:
            observer.update()


    def update_data(self):
        """
        Simulates a change: Modifies an existing record or adds a new one.

        Notifies the Observer.

        Logs the changes made.
        """
        existing_records = self.select_employee()
        if existing_records:
            # Assuming the first record undergoes modifications
            first_record_id = existing_records[0][0]
            modified_data = ("Nombre1", "Apellido1", 12345678, "Area1", "Cargo1", 1000.0, 1)
            self.update_employee(modified_data + (first_record_id,))
            logging.info("Data modified.")
        else:
            # Or create a new record if none existed
            new_record_data = ("Nombre2", "Apellido2", 12345678, "Area2", "Cargo2", 1000.0, 1)
            self.insert_employee(new_record_data)
            logging.info("New record created.")

        # Notify the observer
        self.notify_observers()


    @handle_errors
    def create_table(self):
        """
        Creates the 'Empleados' table in the database if it does not exist.

        Raises sqlite3.Error if an error occurs while creating the table.
        """
        query = """
            CREATE TABLE IF NOT EXISTS Empleados(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Nombre TEXT,
                Apellido TEXT,
                DNI INTEGER,
                Area TEXT,
                Cargo TEXT,
                Sueldo FLOAT,
                Antiguedad INTEGER
            )
        """
        with sqlite3.connect(self.db_path) as con:
            con.execute(query)
        logging.info("Table created successfully.")


    @handle_errors
    def insert_employee(self, data):
        """
        Inserts a new employee into the database.

        Raises sqlite3.Error if an error occurs while inserting the data.
        """
        query = "INSERT INTO Empleados VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)"
        with sqlite3.connect(self.db_path) as con:
            cursor = con.cursor()
            cursor.execute(query, data)
            con.commit()

        info_for_log = f'New employee inserted: {data}'
        send_data(info_for_log)


    @handle_errors
    def select_employee(self):
        """
        Selects and returns all employees from the database.

        Raises sqlite3.Error if an error occurs while selecting the data.
        """
        query = "SELECT * FROM Empleados"
        with sqlite3.connect(self.db_path) as con:
            cursor = con.cursor()
            cursor.execute(query)
            return cursor.fetchall()


    @handle_errors
    def update_employee(self, data):
        """
        Updates the data of an employee in the database.

        Raises sqlite3.Error if an error occurs while updating the data.
        """
        query = """
            UPDATE Empleados SET
                Nombre=?,
                Apellido=?,
                DNI=?,
                Area=?,
                Cargo=?,
                Sueldo=?,
                Antiguedad=?
                WHERE id=?
        """
        with sqlite3.connect(self.db_path) as con:
            cursor = con.cursor()
            cursor.execute(query, data)
            con.commit()

        info_for_log = f'Employee updated: {data}'
        send_data(info_for_log)


    @handle_errors
    def delete_employee(self, employee_id):
        """
        Deletes an employee from the database.

        Raises sqlite3.Error if an error occurs while deleting the employee.
        """
        query = "DELETE FROM Empleados WHERE id = ?"
        with sqlite3.connect(self.db_path) as con:
            cursor = con.cursor()
            cursor.execute(query, (employee_id,))
            con.commit()

        info_for_log = f'Employee deleted: {employee_id}'
        send_data(info_for_log)


    @handle_errors
    def delete_table(self):
        """
        Deletes the 'Empleados' table from the database.

        Raises sqlite3.Error if an error occurs while deleting the table.  
        """
        query = "DROP TABLE IF EXISTS Empleados"
        with sqlite3.connect(self.db_path) as con:
            con.execute(query)
        logging.info("Table deleted successfully.")