import re
from decorators import *
from main import send_data


class EmsController:
    """
    Controller for the employee management application.

    This class contains methods to validate input fields in the employee view and interacts with the model to reflect changes.

    Attributes:
        model (ModelObservable): The data model for the employee information.
    """
    NAME_REGEX = r"^[A-Za-z\s]+$"
    DNI_REGEX = r"^\d{8}$"
    SUELDO_REGEX = r"^\d+(\.\d{1,2})?$"
    ANTIGUEDAD_REGEX = r"^\d+$"


    def __init__(self, model):
        """
        Initializes the EmpleadosController with a reference to the data model.

        Parameters:
            model (ModelObservable): The data model for the employee information.
        """
        self.model = model

    @log_execution
    @measure_execution_time
    def validate_fields(self, fields):
        """
        Validates the provided input fields.

        Checks each field against a regular expression to ensure it meets the expected format.
        Returns None if all fields are valid, or an error message string if any validation fails.

        Parameters:
            fields (tuple): A tuple containing the input fields to be validated.

        Returns:
            str or None: An error message if validation fails, or None if all fields are valid.

        Raises:
            ValueError: If any of the input fields do not match the expected format.
        """
        print("Received fields:", fields)
        print("Number of values:", len(fields))

        nombre, apellido, dni, area, cargo, sueldo, antiguedad = map(str.strip, fields)

        if not re.match(self.NAME_REGEX, nombre):
            return "Nombre inválido. Solo se permiten letras y espacios."
        if not re.match(self.NAME_REGEX, apellido):
            return "Apellido inválido. Solo se permiten letras y espacios."
        if not re.match(self.DNI_REGEX, dni):
            return "DNI inválido. Debe contener exactamente 8 dígitos."
        
        try:
            sueldo = float(sueldo)
        except:
            return "Invalid 'salario'. Must be a valid number"
        

        if not re.match(self.ANTIGUEDAD_REGEX, antiguedad):
            return "Invalid 'Antiguedad'. Must be a whole number."
        
        record_info = f'Validated fields: {fields}'
        send_data(record_info)

        return None