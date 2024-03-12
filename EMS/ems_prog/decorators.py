import time
import logging
from functools import wraps
from tkinter import messagebox


def handle_errors(func):
    """
    A decorator to centralize the handling of common exceptions.

    This decorator wraps a function to provide a unified error handling mechanism.
    It does not replace existing try/except blocks, which may provide custom error messages.

    Parameters:
        func (function): The function to be wrapped by the decorator.

    Returns:
        function: The wrapped function with error handling.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as error:
            logging.error(f"An error occurred: {str(error)}")
            messagebox.showerror("Error", f"An error occurred: {str(error)}")
            return None
    return wrapper


def log_execution(func):
    """
    A decorator for logging the execution of functions.

    Logs the function name, arguments, and confirmation of execution.

    Parameters:
        func (function): The function to be wrapped by the decorator.

    Returns:
        function: The wrapped function with logging.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Executing function '{func.__name__}' with arguments: {args} and keyword arguments: {kwargs}.")
        result = func(*args, **kwargs)
        logging.info(f"Function '{func.__name__}' executed successfully.")
        return result
    return wrapper


def measure_execution_time(func):
    """
    A decorator for measuring the execution time of functions.

    Records and prints the time taken to execute the wrapped function.

    Parameters:
        func (function): The function to be wrapped by the decorator.

    Returns:
        function: The wrapped function with execution time measurement.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(f"Execution of function '{func.__name__}' took {elapsed_time:.6f} seconds.")
        return result
    return wrapper