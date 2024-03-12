import os
import sys
import socket
import logging
import threading
import tkinter as tk


# Set the logging level based in the deployment enviroment.
# In production, set it to a higher level (e.g., logging.WARNING or logging.ERROR)
# In development, keep it at the default level (logging.INFO)
logging_level = logging.WARNING if os.environ.get('DEPLOYMENT_ENV') == 'production' else logging.INFO

# Get the directory where the executable is located
exe_folder = os.path.dirname(sys.executable)

# Specify the log file path
log_file_path = os.path.join(exe_folder, "server.log")

# Configure logging to include both console and file handlers
logging.basicConfig(level=logging_level,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    handlers=[logging.StreamHandler(), logging.FileHandler(log_file_path)])


class Server:
    """Class representing a simple TCP server."""

    # Event to signal the server thread to shut down
    shutdown_event = threading.Event()

    def __init__(self, host, port):
        """
        Initialize the Server object.

        Args:
            host (str): The server's hostname or IP address.
            port (int): The port on which the server will listen.
        """
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        logging.info(f'Server listening on {host}:{port}')

    def start(self):
        """Start the server and handle incoming connections."""
        try:
            while not self.shutdown_event.is_set():
                client, address = self.server.accept()
                logging.info(f'Incoming connection from {address}')

                data = client.recv(1024).decode('utf-8')
                logging.info(f'Received data from {address}: {data}')

                client.close()
        except Exception as e:
            logging.error(f'Server error: {e}')

class Client:
    """Class representing a simple TCP client."""

    def __init__(self, host, port):
        """
        Initialize the Client object.

        Args:
            host (str): The server's hostname or IP address.
            port (int): The port on which the client will connect to the server.
        """
        self.host = host
        self.port = port

    def send_data(self, data):
        """
        Send a string of data to the server via a TCP socket.

        Args:
            data (str): The string data to be sent to the server.

        Raises:
            socket.error: If there is an issue with the socket (e.g., connection error).
            OSError: If a system-related error occurs during the socket operation.
            UnicodeEncodeError: If there is an issue encoding the data to UTF-8.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.host, self.port))
                client.send(data.encode('utf-8'))
                logging.info(f'Data sent to the server: {data}')
        except (socket.error, OSError) as e:
            logging.error(f'Error connecting or sending data to the server: {e}')
        except UnicodeEncodeError as uee:
            logging.error(f'Error encoding data to UTF-8: {uee}')


def send_data(data):
    """
    Send a string of data to the server via a TCP socket.

    Args:
        data (str): The string data to be sent to the server.

    Raises:
        Exception: An error occurred while attempting to send data through the socket.
    """

    host = 'localhost'  # Replace with the server's IP address
    port = 5555
    try:
        # Create a client socket
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the server
        cliente.connect((host, port))
        # Send data to the server
        cliente.send(data.encode('utf-8'))
        logging.info(f'Data sent to the server: {data}')
    except Exception as e:
        logging.error(f'Error sending data to the server: {e}')
    finally:
        # Close the connection
        cliente.close()

        
def main():
    """
    Initialize and run the employee management application.

    This function sets up the database connection, initializes the MVC components (Model, View, Controller),
    and starts the Tkinter event loop to open the application window. It ensures the database table for
    employees exists and sets up the observer pattern between the model and the view.

    The database file is expected to be named 'mydatabase.db' and located in the same directory as this script.
    """
    from view import EmsView
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "mydatabase.db")

    from model import EmsModel
    model = EmsModel(db_path)
    model.create_table()

    from controller import EmsController
    controller = EmsController(model)

    # Example data for server logging
    record_info = 'Data for server records'

    # Initialize and start the server in a separate thread
    server_thread = threading.Thread(target=Server('localhost', 5555).start, daemon=True)
    server_thread.start()

    # Log when client data is being sent to the server
    logging.info("Sending data to the server...")

    # Automatically send data to the server
    Client('localhost', 5555).send_data(record_info)

    # Create the main application window.
    root = tk.Tk()

    # Initialize EmsView with the root window, model, and controller.
    view = EmsView(root, model, controller)

    # Set the Observer in the model.
    model.add_observer(view)

    # Start the main tkinter event loop.
    root.mainloop()

    # Set the shutdown event to signal the server thread to exit
    Server.shutdown_event.set()

    # Gracefully exit the server thread when the main application is closed.
    server_thread.join(timeout=5)


if __name__ == "__main__":
    main()