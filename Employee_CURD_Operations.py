import sqlite3
import os
import sys


def employee_curd_operation():
    print('For Creating record ENTER : 1 ')
    print('For Updating record ENTER : 2 ')
    print('For Retrieving record ENTER : 3 ')
    print('For Deleting record Enter : 4 ')
    print('FOR EXIT ENTER : 5 ')
    choice = input("SELECT YOUR OPTION : ")
    choice = validate_user_input(choice)
    if choice == "1":
        create_record()
    elif choice == "2":
        update_record()
    elif choice == "3":
        retrieve_record()
    elif choice == "4":
        delete_record()
    elif choice == "5":
        sys.exit(0)
    else:
        print('YOU HAVE ENTERED WRONG CHOICE. SELECT RIGHT OPTION !!!!')
        employee_curd_operation()
    print('IF YOU WANT TO CONTINUE NEXT OPERATION ENTER 1 ELSE 2 :')
    next_opr = input("> ")
    if next_opr == "1":
        employee_curd_operation()
    elif next_opr == "2":
        sys.exit(0)
    else:
        print('You have entered wrong choice. Enter right choice')
        employee_curd_operation()


def employee_update_operation():
    print('For updating FIRSTNAME enter 1 : ')
    print('For updating LASTNAME enter 2 : ')
    print('For updating DOB enter 3 : ')
    print('For updating DEPARTMENT enter 4 : ')


def create_database_tables():
    emp_table = '''
        CREATE TABLE IF NOT EXISTS employee(
        empid TEXT NOT NULL PRIMARY KEY, 
        firstname TEXT NOT NULL, 
        lastname TEXT NOT NULL,
        dob TEXT NOT NULL,
        department TEXT NOT NULL,
        FOREIGN KEY(department) REFERENCES department(dept_name) ON DELETE CASCADE
        )
    '''

    dept_table = '''
        CREATE TABLE IF NOT EXISTS department(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
        dept_name TEXT NOT NULL
        )
    '''

    if not os.path.isfile('testdb.sqlite'):
        conn = sqlite3.connect('testdb.sqlite')
        try:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")

            cursor.execute(emp_table)
            print('created employee table')

            cursor.execute(dept_table)
            print('created department table')

            conn.commit()
        except Exception as e:
            print('oops, error while creating database tables !!!')
            conn.rollback()
            raise e
        finally:
            conn.close()


def create_record():
    create_database_tables()
    print('Create operation started...........')
    print('Please enter the employee id : ')
    empid = input('> ')
    print('Please enter the firstname : ')
    firstname = input('> ')
    print('Please enter the lastname : ')
    lastname = input('> ')
    print('Please enter the date of birth in DDMMYYYY format : ')
    dob = input('> ')
    dob = age_validation(dob)
    print('Please enter the department name : ')
    department = input('> ')

    department_query = '''
            INSERT INTO department (dept_name) VALUES (?)
    '''

    employee_query = '''
            INSERT INTO employee (empid, firstname, lastname, dob, department) VALUES (?, ?, ?, ?, ?)
    '''

    conn = sqlite3.connect('testdb.sqlite')
    try:
        cursor = conn.cursor()

        cursor.execute(department_query, (department,))
        print('created record in department table')

        cursor.execute(employee_query, (empid, firstname, lastname, dob, department))
        print('Successfully created record for employee with EmployeeID : {}'.format(empid))
        conn.commit()
    except Exception as e:
        print('error while creating record in databases !!!')
        conn.rollback()
        raise e
    finally:
        conn.close()
    return True


def age_validation(dob):
    """
    Validation for dateOfBirth
    Parameters:
    dob: employee dateOfBirth
    Returns:
    dob: validated dateOfBirth
    """
    if not len(dob) == 8:
        print('Enter DateOfBirth in DDMMYYYY format only : ')
        dob = input('> ')
        dob = age_validation(dob)
    if not dob.isdigit():
        print('Enter DateOfBirth in DDMMYYYY format only : ')
        dob = input('> ')
        dob = age_validation(dob)
    else:
        try:
            if int(dob[4:]) <= 1994:
                print('Age more then 25 years is not allowed !!!')
                print('Re-enter DateOfBirth')
                dob = input('> ')
                dob = age_validation(dob)
        except Exception as e:
            print('error while validating dob !!!')
            raise e
    return dob

def validate_user_input(user_input):
    """
    Validates user input
    Parameters:
    user_input: input by user
    Returns:
    user_input : validated user input
    """
    if user_input in ('1', '2', '3', '4'):
        return user_input
    else:
        next_input = int(input('Please re-enter valid input'))
        validate_user_input(next_input)
        return next_input


def update_record():
    if not os.path.isfile('testdb.sqlite'):
        print('OOPS...There are no records to update. Please create records : ')
    else:
        print('Update operation started...........')
        print('Please enter the employee id of the employee you want to update record : ')
        empid = input('> ')
        conn = sqlite3.connect('testdb.sqlite')
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT empid FROM employee WHERE empid = ?", (empid,))
            data = cursor.fetchall()
        except Exception as e:
            print('error while checking emp id record from database !!!')
            raise e
        finally:
            conn.close()
        try:
            if len(data) == 0:
                print('Record does not exists for this EmpID in the database !!!')
            else:
                update_record_options(empid)
        except Exception as e:
            print('error in update operation !!!')
            raise e


def update_record_options(empid):
    """
    Different update operations
    empid: employeeID
    """
    employee_update_operation()
    update_choice = input('<')
    if update_choice == "1":
        update_firstname(empid)
    elif update_choice == "2":
        update_lastname(empid)
    elif update_choice == "3":
        update_dob(empid)
    elif update_choice == "4":
        update_department(empid)
    else:
        print('OOPS....YOU HAVE ENTERED WRONG CHOICE. Please select right choice : ')
        update_record_options(empid)


def update_firstname(empid):
    """
    Update firstName operation
    empid: employeeID
    """
    conn = sqlite3.connect('testdb.sqlite')
    print('Enter FIRSTNAME to be update : ')
    entered_firstname = input('> ')
    try:
        cursor = conn.cursor()
        cursor.execute('''UPDATE employee SET firstname = ? WHERE empid = ? ''', (entered_firstname, empid))
        conn.commit()
    except Exception as e:
        print('error while updating FIRSTNAME !!!')
        conn.rollback()
        raise e
    finally:
        conn.close()


def update_lastname(empid):
    """
    Update lastName operation
    empid: employeeID
    """
    conn = sqlite3.connect('testdb.sqlite')
    entered_lastname = input('Enter LASTNAME to be update : ')
    try:
        cursor = conn.cursor()
        cursor.execute('''UPDATE employee SET lastname = ? WHERE empid = ? ''', (entered_lastname, empid))
        conn.commit()
    except Exception as e:
        print('error while updating LASTNAME !!!')
        conn.rollback()
        raise e
    finally:
        conn.close()


def update_dob(empid):
    """
    Update dateOfBirth operation
    empid: employeeID
    """
    conn = sqlite3.connect('testdb.sqlite')
    print('Enter DOB to be update : ')
    entered_dob = input('> ')
    try:
        cursor = conn.cursor()
        cursor.execute('''UPDATE employee SET dob = ? WHERE empid = ? ''', (entered_dob, empid))
        conn.commit()
    except Exception as e:
        print('error while updating DOB !!!')
        conn.rollback()
        raise e
    finally:
        conn.close()


def update_department(empid):
    """
    Update department operation
    empid: employeeID
    """
    conn = sqlite3.connect('testdb.sqlite')
    print('Enter DEPARTMENT to be update : ')
    entered_department = input('> ')

    try:
        cursor = conn.cursor()
        cursor.execute('''UPDATE employee SET department = ? WHERE empid = ? ''', (entered_department, empid))
        conn.commit()
    except Exception as e:
        print('error while updating DEPARTMENT !!!')
        conn.rollback()
        raise e
    finally:
        conn.close()


def retrieve_record():
    if not os.path.isfile('testdb.sqlite'):
        print('OOPS...There are no records to retrieve. Please create records : ')
    else:
        conn = sqlite3.connect('testdb.sqlite')
        print('enter employeeID to be retrieved : ')
        empid = input('> ')
        try:
            cursor = conn.cursor()
            cursor.execute(''' SELECT * FROM employee WHERE empid = ?''', (empid,))
            employee = cursor.fetchone()
            if employee is None:
                print('Record not found in the table for employee with EmployeeID : {}'.format(empid))
            else:
                print('EMPID, FIRSTNAME, LASTNAME, DOB, DEPARTMENT')
                print(employee)
        except Exception as e:
            print('error while retrieve operation !!!')
            conn.rollback()
            raise e
        finally:
            conn.close()


def delete_record():
    if not os.path.isfile('testdb.sqlite'):
        print('OOPS...There are no records to retrieve. Please create records : ')
    else:
        conn = sqlite3.connect('testdb.sqlite')
        print('enter employeeID to be DELETED : ')
        empid = input('> ')
        try:
            cursor = conn.cursor()
            cursor.execute(''' DELETE FROM employee WHERE empid = ?''', (empid,))
            conn.commit()
            print('Successfully deleted employee with EmployeeID : {}'.format(empid))
        except Exception as e:
            print("error in delete operation !!!")
            conn.rollback()
            raise e
        finally:
            conn.close()


def main():
    print('Hi Welcome to Employee Database management!!!!')
    print('Please input the operation you want to perform')
    employee_curd_operation()


if __name__ == "__main__":
    main()
