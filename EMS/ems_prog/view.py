import sqlite3
import logging
from tkinter import *
from tkinter import ttk, messagebox
from main import send_data


class EmsView:
    """
    View for the employee management application's graphical user interface.

    This class provides the interface elements for user interaction with the employee database,
    including displaying, adding, updating, and deleting employee records.

    Attributes:
        root (tkinter.Tk): The main window of the application.
        model (EmpleadosModel): The data model for employee information.
        controller (EmpleadosController): The controller to handle actions in the view.
    """
    #Constants
    DATA_FRAME_TITLE = "Data upload"
    BUTTON_FRAME_TITLE = "Records"
    CONFIRM_DELETE_ALL = "DB will be erased.\nPress Yes to continue."
    CONFIRM_DELETE_ROW = "Selected record will be erased.\nPress Yes to continue."


    def __init__(self, root, model, controller):
        """
        Initializes the EmpleadosView with the main application window, data model, and controller.

        Registers the view as an observer to the model to receive updates on data changes.

        Parameters:
            root (tkinter.Tk): The main window of the application.
            model (EmpleadosModel): The data model for employee information.
            controller (EmpleadosController): The controller to handle actions in the view.
        """
        self.root = root
        self.model = model
        self.controller = controller
        model.add_observer(self)

        # Create main window
        self.root.title("Empleados Database")
        self.root.geometry("1000x500")

        # Add syle
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackround="#D3D3D3")

        # Change selected color
        style.map("Treeview", background=[("selected", "aquamarine4")])

        # Create Treeview frame
        tree_frame = Frame(root)
        tree_frame.pack(pady=0)

        # Create scroll-bar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create Treeview
        self.my_tree = ttk.Treeview(tree_frame, columns=(1,2,3,4,5,6,7,8), yscrollcommand=tree_scroll.set, selectmode="extended")
        self.my_tree.pack()

        # Get row data to see it on lables
        self.my_tree.bind("<<TreeviewSelect>>", self.retrieve_data)

        # Configure scroll-bar
        tree_scroll.config(command=self.my_tree.yview)

        # Define columns
        self.my_tree['columns'] = ('Nombre', 'Apellido', 'DNI', "Area", "Cargo", 'Sueldo bruto', "Antiguedad")

        # Create headings
        self.my_tree.column('#0', anchor=CENTER, width=77)
        self.my_tree.column('Nombre', anchor=W, width=117)
        self.my_tree.column('Apellido', anchor=W, width=117)
        self.my_tree.column('DNI', anchor=CENTER, width=117)
        self.my_tree.column('Area', anchor=W, width=157)
        self.my_tree.column('Cargo', anchor=W, width=117)
        self.my_tree.column('Sueldo bruto', anchor=CENTER, width=117)
        self.my_tree.column('Antiguedad', anchor=CENTER, width=117)

        # Configure headings
        self.my_tree.heading('#0', text='ID', anchor=CENTER)
        self.my_tree.heading('Nombre', text='Nombre', anchor=W)
        self.my_tree.heading('Apellido', text='Apellido', anchor=W)
        self.my_tree.heading('DNI', text='DNI', anchor=CENTER)
        self.my_tree.heading('Area', text='Area', anchor=W)
        self.my_tree.heading('Cargo', text='Cargo', anchor=W)
        self.my_tree.heading('Sueldo bruto', text='Sueldo bruto', anchor=CENTER)
        self.my_tree.heading('Antiguedad', text='Antiguedad', anchor=CENTER)

        # Create strip rows
        self.my_tree.tag_configure("oddrow", background="snow")
        self.my_tree.tag_configure("evenrow", background="AliceBlue")

        # Add data frame
        data_frame = LabelFrame(root, text="Carga de datos")
        data_frame.pack(fill="x", expand="yes", padx=20)
        button_frame = LabelFrame(root, text="Comandos")
        button_frame.pack(fill="x", expand="yes", padx=20)

        # Set variables
        self.nombre = StringVar()
        self.apellido = StringVar()
        self.dni = StringVar()
        self.area = StringVar()
        self.cargo = StringVar()
        self.sueldo = StringVar()
        self.anti = StringVar()
        self.selected_id = IntVar()

        # Labels and entries
        id_label = Label(data_frame, text="ID")
        id_label.grid(row=0, column=0, padx=10, pady=10, sticky=E)
        self.id_entry = Entry(data_frame, textvariable=self.selected_id, state="disabled", width=22)
        self.id_entry.grid(row=0, column=1, padx=10, pady=10)

        nombre_label = Label(data_frame, text="Nombre")
        nombre_label.grid(row=0, column=2, padx=10, pady=10, sticky=E)
        self.nombre_entry = Entry(data_frame, textvariable=self.nombre, width=22)
        self.nombre_entry.grid(row=0, column=3, padx=10, pady=10)

        apellido_label = Label(data_frame, text="Apellido")
        apellido_label.grid(row=0, column=4, padx=10, pady=10, sticky=E)
        self.apellido_entry = Entry(data_frame, textvariable=self.apellido, width=22)
        self.apellido_entry.grid(row=0, column=5, padx=10, pady=10)

        dni_label = Label(data_frame, text="DNI")
        dni_label.grid(row=0, column=6, padx=10, pady=10, sticky=E)
        self.dni_entry = Entry(data_frame, textvariable=self.dni, width=22)
        self.dni_entry.grid(row=0, column=7, padx=10, pady=10)

        area_label = Label(data_frame, text="Area")
        area_label.grid(row=1, column=0, padx=10, pady=10, sticky=E)
        self.area_entry = Entry(data_frame, textvariable=self.area, width=22)
        self.area_entry.grid(row=1, column=1, padx=10, pady=10)

        cargo_label = Label(data_frame, text="Cargo")
        cargo_label.grid(row=1, column=2, padx=10, pady=10, sticky=E)
        self.cargo_entry = Entry(data_frame, textvariable=self.cargo, width=22)
        self.cargo_entry.grid(row=1, column=3, padx=10, pady=10)

        sueldo_label = Label(data_frame, text="Sueldo bruto")
        sueldo_label.grid(row=1, column=4, padx=10, pady=10, sticky=E)
        self.sueldo_entry = Entry(data_frame, textvariable=self.sueldo, width=22)
        self.sueldo_entry.grid(row=1, column=5, padx=10, pady=10)

        anti_label = Label(data_frame, text="Antiguedad")
        anti_label.grid(row=1, column=6, padx=10, pady=10, sticky=E)
        self.anti_entry = Entry(data_frame, textvariable=self.anti, width=22)
        self.anti_entry.grid(row=1, column=7, padx=10, pady=10)

        # Buttons
        request_employee_button = Button(button_frame, text="Consultar", width=15, command=self.request_employees)
        request_employee_button.grid(row=0, column=1, padx=10, pady=10)

        create_employee_button = Button(button_frame, text="Crear", fg="white", bg="aquamarine4", width=15, command=self.create_employee)
        create_employee_button.grid(row=0, column=2, padx=10, pady=10)

        modify_employee_button = Button(button_frame, text="Modificar", width=15, command=self.modify_employee)
        modify_employee_button.grid(row=0, column=3, padx=10, pady=10)

        erase_employee_button = Button(button_frame, text="Eliminar fila", width=15, command=self.erase_employee)
        erase_employee_button.grid(row=0, column=4, padx=10, pady=10)

        erase_all_button = Button(button_frame, text="Eliminar tabla", fg="white", bg="brown3", width=15, command=self.erase_all)
        erase_all_button.grid(row=0, column=5, padx=10, pady=10)

        reset_fields_button = Button(button_frame, text="Limpiar campos", width=15, command=self.reset_fields)
        reset_fields_button.grid(row=0, column=6, padx=10, pady=10) 

        close_app_button = Button(button_frame, text="Salir", fg="white", bg="dim gray", width=15, command=self.close_app)
        close_app_button.grid(row=0, column=7, padx=10, pady=10) 

 
    def update_row_in_treeview(self, employee_id, updated_values):
        """ 
        Update a specific row in the Treeview with new data.
        """
        # Iterate through the Treeview items and find the one with the matching ID
        for item_id in self.my_tree.get_children():
            if self.my_tree.item(item_id, "text") == employee_id:
                # Update the values of the row
                self.my_tree.item(item_id, values=updated_values)
                break

    
    def delete_row_in_treeview(self, employee_id):
        """
        Delete a specific row in the Treeview.
        """
        # Iterate through the Treeview items and find the one with the matching ID
        for item_id in self.my_tree.get_children():
            if self.my_tree.item(item_id, "text") == employee_id:
                # Delete the row
                self.my_tree.delete(item_id)
                break


    def request_employees(self):
        """
        Queries and displays employees in the view.

        Fetches employee records from the model and populates the tree view.
        Handles OperationalError by showing an error message if no employees exist.
        """
        try:
            self.my_tree.delete(*self.my_tree.get_children())
            employees = self.model.select_employee()
            for employee in employees:
                self.my_tree.insert("", 0, text=employee[0], values=employee[1:])
        except sqlite3.OperationalError as e:
            messagebox.showerror("Error", f"Error querying employee: {e}")


    def create_employee(self):
        """
        Creates a new employee record in the database.

        Validates input fields, shows error messages for invalid inputs or missing fields,
        and inserts the new employee record into the database. Then updates the view and resets the input fields.
        """
        fields = [self.nombre.get(),
                  self.apellido.get(),
                  self.dni.get(),
                  self.area.get(),
                  self.cargo.get(),
                  self.sueldo.get(),
                  self.anti.get()
                  ]
        error_message = self.controller.validate_fields(fields)

        if error_message:
            messagebox.showerror("Validation error:", error_message)
            return
        
        if any(field == "" for field in fields):
            messagebox.showerror("Error", "Fields missing.")
            return
        
        data = (self.nombre_entry.get(),
                self.apellido_entry.get(),
                self.dni_entry.get(),
                self.area_entry.get(),
                self.cargo_entry.get(),
                self.sueldo_entry.get(),
                self.anti_entry.get()
                )
        new_employee_id = self.model.insert_employee(data)
        data_with_id = (str(new_employee_id),) + data
        self.my_tree.insert("", 0, text=data_with_id[0], values=data_with_id[1:])
        self.request_employees()
        self.reset_fields()
        record_info = f'New employee created: {data}'
        send_data(record_info)


    def retrieve_data(self, event):
        """
        Retrieves the data of a selected employee in the view.

        Populates the input fields with the selected employee's data or shows an info message if no data is available.
        """
        selected_rows = self.my_tree.selection()
        if selected_rows:
            selected_row = selected_rows[0]
            data = self.my_tree.item(selected_row)
            row = data["values"]
            if len(row) >= 7:  
                self.nombre.set(row[0])
                self.apellido.set(row[1])
                self.dni.set(row[2])
                self.area.set(row[3])
                self.cargo.set(row[4])
                self.sueldo.set(row[5])
                self.anti.set(row[6])
                self.selected_id.set(data["text"])
            else:
                messagebox.showinfo("Selection", "Selected row does not have the expected data.")
        else:
            pass
    

    def modify_employee(self):
        """
        Updates the data of a selected employee in the database.

        Validates the new data, updates the employee record in the model, and refreshes the view.
        Shows an info message upon successful update or an error message if no record is selected.
        """
        selected_row = self.my_tree.focus()
        if not selected_row:
            messagebox.showerror("Error", "Select a record to update.")
            return
        
        # Retrieve data from the selected row
        data = self.my_tree.item(selected_row)
        if "text" not in data or not data["text"]:
            messagebox.showerror("Error", "Could not get information for the selected record.")
            return

        # Retrieve the employee ID
        empleado_id = data["text"]
        
        new_data = (
            self.nombre.get(),
            self.apellido.get(),
            self.dni.get(),
            self.area.get(),
            self.cargo.get(),
            self.sueldo.get(),
            self.anti.get())
        
        # Validate the new data before updating
        error_message = self.controller.validate_fields(new_data)
        if error_message:
            messagebox.showerror("Validation Error", error_message)
            return
        
        # Combine data for the update
        combined_data = new_data + (empleado_id,)
        # Update the employee record in the model
        self.model.update_employee(combined_data)
        # Update the row in the Treeview
        self.update_row_in_treeview(empleado_id, new_data)
        # Show an info message for a successful update
        messagebox.showinfo(title="Update", message="Data updated successfully.")
        # Reset input fields
        self.reset_fields()


    def erase_employee(self):
        """
        Deletes a selected employee record from the database.
        """
        selected_row = self.my_tree.focus()
        if selected_row:
            # Get the item ID (employee ID) from the selected row
            item_id = self.my_tree.item(selected_row, "text")            
            # Confirm deletion
            confirm = messagebox.askyesno("Delete", self.CONFIRM_DELETE_ROW)
            if confirm:
                self.model.delete_employee(item_id)
                self.delete_row_in_treeview(item_id)
                self.reset_fields()
                messagebox.showinfo(title="Deleting", message="Record deleted")


    def erase_all(self):
        """
        Deletes all employee records from the database.

        Asks for confirmation before clearing all records, resets the view, and recreates the database table.
        """
        alert = messagebox.askyesno("Erase all", "DB will be erased.\nPress Yes to continue.")
        if alert:
            self.my_tree.delete(*self.my_tree.get_children())
            self.model.delete_table()
            self.reset_fields()
            self.model.create_table()
            # self.my_tree.delete(*self.my_tree.get_children())  # Limpia el Treeview
            # self.model.delete_table()
            # self.reset_fields()
            # self.model.create_table()


    def reset_fields(self):
        """
        Resets the input fields in the view to their default state.
        """
        self.nombre_entry.delete(0, END)
        self.apellido_entry.delete(0, END)
        self.dni_entry.delete(0, END)
        self.area_entry.delete(0, END)
        self.cargo_entry.delete(0, END)
        self.sueldo_entry.delete(0, END)
        self.anti_entry.delete(0, END)


    def close_app(self):
        """
        Closes the application.
        """
        self.root.destroy()