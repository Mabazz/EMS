from cx_Freeze import setup, Executable

setup(
    name="Employee Management System",
    version="2.0",
    description="A comprehensive application designed for efficient management of employee information within an organization",
    executables=[Executable("main.py", base="Win32GUI", icon="C:/Users/marti/Documents/EMS/ems_prog/EMS.ico")],
    options={
        'build_exe': {
            'packages': ['model', 'controller', 'view', 'decorators'],
            'include_files': ['README.md'],
        },
    },
)