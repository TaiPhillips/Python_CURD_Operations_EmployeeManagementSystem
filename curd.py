import sqlite3
import os
import sys
import datetime


def welcome_message():
    """
    welcome message for the CURD operations
    """
    print(""" 

     |-------------------------------------------------------------|
     |=============================================================| 
     |==== Hi Welcome to Employee Database management	System ======|
     |=============================================================|
     |-------------------------------------------------------------|
     
        """)


def employee_curd_operation():
    """
    different employee and department CURD operations
    """
    print('Enter 1 : To Create Record ')
    print('Enter 2 : To Update Record ')
    print('Enter 3 : To Retrieve Record ')
    print('Enter 4 : To Delete Record ')
    print('Enter 5 : To EXIT ')
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
    continue_operation()


def continue_operation():
    """
    checks if user wants to proceed with other operations
    """
    print('\n IF YOU WANT TO CONTINUE NEXT OPERATION ENTER 1 ELSE 2 :')
    next_opr = input("> ")
    if next_opr == "1":
        employee_curd_operation()
    elif next_opr == "2":
        sys.exit(0)
    else:
        print('You have entered wrong choice. Enter right choice')
        continue_operation()


def employee_update_operation():
    """
    options for different update operations
    """
    print('Enter 1 : To update FIRSTNAME ')
    print('Enter 2 : To update LASTNAME ')
    print('Enter 3 : To update DOB ')
    print('Enter 4 : To update DEPARTMENT ')


def create_database_tables():
    """
    creation of database tables
    """
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
    """
    creates record in employee and department tables
    """
    create_database_tables()
    print('Create operation started...........')
    empid = add_employee_id(False)
    firstname = add_firstname()
    lastname = add_lastname()
    dob = add_dob()
    dob = age_validation(dob)
    department = add_department()

    department_query = '''
            INSERT INTO department (dept_name) VALUES (?)
    '''

    employee_query = '''
            INSERT INTO employee (empid, firstname, lastname, dob, department) VALUES (?, ?, ?, ?, ?)
    '''

    value_in_department_table = check_value_in_department_table(department)
    conn = sqlite3.connect('testdb.sqlite')
    try:
        cursor = conn.cursor()
        if value_in_department_table is False:
            cursor.execute(department_query, (department,))
            print('created record in department table')

        cursor.execute(employee_query, (empid, firstname, lastname, dob, department))
        conn.commit()
        print('Successfully created record for employee with EmployeeID : {}'.format(empid))
        f = open("log.txt", "a+")
        try:
            currenttime = datetime.datetime.now().strftime("%I:%M%p %B %d, %Y")
            f.write(currenttime+' : '+'Added new record with EmployeeID -> {}'.format(empid)+' \n')
        except Exception as e:
            print('error while updating into log file !!!')
            raise e
        finally:
            f.close()
    except Exception as e:
        print('error while creating record in databases !!!')
        conn.rollback()
        raise e
    finally:
        conn.close()
    return True


def add_employee_id(update=False):
    """
    checks if employeeID already exists and if not adds
    Parameters:
    update: True if update else create
    Returns:
    empid: EmployeeID of the employee
    """
    print('Enter EmployeeID : ')
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
        if update==False:
            if len(data) != 0:
                print('OOPS.. entered EmployeeID is ALREADY EXISTS... Please re-enter :')
                new_empid = add_employee_id(False)
                return new_empid
            else:
                if empid in ("", None) or empid.isspace():
                    print('Invalid value for EmployeeID. Please re-enter valid value : ')
                    new_empid = add_employee_id(False)
                    return new_empid
                else:
                    return empid
        else:
            if empid in ("", None) or empid.isspace():
                print('Invalid value for EmployeeID. Please re-enter valid value : ')
                new_empid = add_employee_id(True)
                return new_empid
            else:
                return empid
    except Exception as e:
        raise e


def add_firstname():
    """
    checks valid firstname and returns it
    Returns:
    firstname : validated firstname
    """
    print('Enter Firstname : ')
    firstname = input('> ')
    if firstname in ("", None) or firstname.isspace():
        print('Invalid value for Firstname. Please re-enter valid value : ')
        new_firstname = add_firstname()
        return new_firstname
    else:
        return firstname


def add_lastname():
    """
    checks valid lastname and returns it
    Returns:
    lastname : validated lastname
    """
    print('Enter Lastname : ')
    lastname = input('> ')
    if lastname in ("", None) or lastname.isspace():
        print('Invalid value for Lastname. Please re-enter valid value : ')
        new_lastname = add_lastname()
        return new_lastname
    else:
        return lastname


def add_dob():
    """
    checks valid date of birth and returns it
    Returns:
    dob : validated date of birth
    """
    print('Enter DateOfBirth : ')
    dob = input('> ')
    if dob in ("", None) or dob.isspace():
        print('Invalid value for DateOfBirth. Please re-enter valid value : ')
        new_dob = add_dob()
        return new_dob
    else:
        return dob


def add_department():
    """
    checks valid department name and returns it
    Returns:
    department : validated department name
    """
    print('Enter Department : ')
    department = input('> ')
    if department in ("", None) or department.isspace():
        print("Invalid value for Department. Please re-enter valid value : ")
        new_department = add_department()
        return new_department
    else:
        return department


def age_validation(dob):
    """
    validation for dateOfBirth
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
            if int(dob[4:]) >= 1994:
                print('Age less than 25 years is not allowed !!!')
                print('Re-enter DateOfBirth')
                dob = input('> ')
                dob = age_validation(dob)
        except Exception as e:
            print('error while validating dob !!!')
            raise e
    return dob


def validate_user_input(user_input):
    """
    validates user input
    Parameters:
    user_input: input by user
    Returns:
    user_input : validated user input
    """
    if user_input in ('1', '2', '3', '4', '5'):
        return user_input
    else:
        next_input = input('Please re-enter valid input : ')
        validate_user_input(next_input)
        return next_input


def update_record():
    """
    update record operation
    """
    if not os.path.isfile('testdb.sqlite'):
        print('OOPS...There are no records to update. Please create records : ')
    else:
        print('Update operation started...........')
        print('Need EmployeeID of the employee you want to update : ')
        empid = add_employee_id(True)
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
    different update operations
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
    update firstName operation
    empid: employeeID
    """
    conn = sqlite3.connect('testdb.sqlite')
    print('Enter FIRSTNAME to update : ')
    entered_firstname = input('> ')
    try:
        cursor = conn.cursor()
        cursor.execute('''UPDATE employee SET firstname = ? WHERE empid = ? ''', (entered_firstname, empid))
        conn.commit()
        f = open("log.txt", "a+")
        try:
            currenttime = datetime.datetime.now().strftime("%I:%M%p %B %d, %Y")
            f.write(currenttime+' : '+'Updated FIRSTNAME for employee with EmployeeID -> {}'.format(empid)+' \n')
        except Exception as e:
            print('error while updating into log file !!!')
            raise e
        finally:
            f.close()
    except Exception as e:
        print('error while updating FIRSTNAME !!!')
        conn.rollback()
        raise e
    finally:
        conn.close()


def update_lastname(empid):
    """
    update lastName operation
    empid: employeeID
    """
    conn = sqlite3.connect('testdb.sqlite')
    entered_lastname = input('Enter LASTNAME to update : ')
    try:
        cursor = conn.cursor()
        cursor.execute('''UPDATE employee SET lastname = ? WHERE empid = ? ''', (entered_lastname, empid))
        conn.commit()
        f = open("log.txt", "a+")
        try:
            currenttime = datetime.datetime.now().strftime("%I:%M%p %B %d, %Y")
            f.write(currenttime+' : '+'Updated LASTNAME for employee with EmployeeID -> {}'.format(empid)+' \n')
        except Exception as e:
            print('error while updating into log file !!!')
            raise e
        finally:
            f.close()
    except Exception as e:
        print('error while updating LASTNAME !!!')
        conn.rollback()
        raise e
    finally:
        conn.close()


def update_dob(empid):
    """
    update dateOfBirth operation
    empid: employeeID
    """
    conn = sqlite3.connect('testdb.sqlite')
    print('Enter DOB to update : ')
    entered_dob = input('> ')
    try:
        cursor = conn.cursor()
        cursor.execute('''UPDATE employee SET dob = ? WHERE empid = ? ''', (entered_dob, empid))
        conn.commit()
        f = open("log.txt", "a+")
        try:
            currenttime = datetime.datetime.now().strftime("%I:%M%p %B %d, %Y")
            f.write(currenttime+' : '+'Updated DOB for employee with EmployeeID -> {}'.format(empid)+' \n')
        except Exception as e:
            print('error while updating into log file !!!')
            raise e
        finally:
            f.close()
    except Exception as e:
        print('error while updating DOB !!!')
        conn.rollback()
        raise e
    finally:
        conn.close()


def update_department(empid):
    """
    update department operation
    empid: employeeID
    """
    conn = sqlite3.connect('testdb.sqlite')
    print('Enter DEPARTMENT to update : ')
    entered_department = input('> ')
    value_in_department_table = check_value_in_department_table(entered_department)
    try:
        cursor = conn.cursor()
        cursor.execute('''UPDATE employee SET department = ? WHERE empid = ? ''', (entered_department, empid))
        if value_in_department_table is False:
            cursor.execute('''INSERT INTO department (dept_name) VALUES (?) ''', (entered_department,))
        conn.commit()
        f = open("log.txt", "a+")
        try:
            currenttime = datetime.datetime.now().strftime("%I:%M%p %B %d, %Y")
            f.write(currenttime+' : '+'Updated DEPARTMENT for employee with EmployeeID -> {}'.format(empid)+' \n')
        except Exception as e:
            print('error while updating into log file !!!')
            raise e
        finally:
            f.close()
    except Exception as e:
        print('error while updating DEPARTMENT !!!')
        conn.rollback()
        raise e
    finally:
        conn.close()


def check_value_in_department_table(entered_department):
    """
    checks department name exists in department table
    Parameters:
    entered_department: user entered department name
    is_exists : True if exists else False
    """
    conn = sqlite3.connect('testdb.sqlite')
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT dept_name FROM department WHERE dept_name = ?", (entered_department,))
        data = cursor.fetchall()
    except Exception as e:
        print('error while checking dept_name record from department table !!!')
        raise e
    finally:
        conn.close()
    try:
        if len(data) == 0:
            return False
        else:
            return True
    except Exception as e:
        raise e


def retrieve_record():
    """
    retrieve record operation
    """
    if not os.path.isfile('testdb.sqlite'):
        print('OOPS...There are no records to retrieve. Please create records : ')
    else:
        conn = sqlite3.connect('testdb.sqlite')
        usr_input = retrieve_input()
        if usr_input == '1':
            print('enter employeeID to retrieve : ')
            empid = input('> ')
            try:
                cursor = conn.cursor()
                cursor.execute(''' SELECT * FROM employee WHERE empid = ?''', (empid,))
                employee = cursor.fetchone()
                if employee is None:
                    print('Record not found for employee with EmployeeID : {}'.format(empid))
                else:
                    print('EMPID, FIRSTNAME, LASTNAME, DOB, DEPARTMENT')
                    print(employee)
            except Exception as e:
                print('error while retrieve operation !!!')
                conn.rollback()
                raise e
            finally:
                conn.close()
        elif usr_input == '2':
            print('enter firstName to retrieve : ')
            fname = input('> ')
            try:
                cursor = conn.cursor()
                cursor.execute(''' SELECT * FROM employee WHERE firstname = ?''', (fname,))
                employee = cursor.fetchall()
                if employee is None:
                    print('Record not found for employee with Firstname : {}'.format(fname))
                else:
                    print('EMPID, FIRSTNAME, LASTNAME, DOB, DEPARTMENT')
                    for emp in employee:
                        print(emp)
            except Exception as e:
                print('error while retrieve operation !!!')
                conn.rollback()
                raise e
            finally:
                conn.close()


def retrieve_input():
    """
    validates user input required for retrieve operation
    Returns:
    user_input: validated user input
    """
    print('Enter 1 : To retrieve record with EmployeeID : ')
    print('Enter 2 : To retrieve record with Firstname : ')
    usr_input = input('> ')
    if usr_input in ("", None) or usr_input.isspace():
        print('re-enter valid input : ')
        new_input = retrieve_input()
        return new_input
    else:
        return usr_input


def delete_record():
    """
    delete record operation
    """
    if not os.path.isfile('testdb.sqlite'):
        print('OOPS...There are no records to retrieve. Please create records : ')
    else:
        conn = sqlite3.connect('testdb.sqlite')
        print('enter employeeID to DELETE : ')
        empid = input('> ')
        try:
            cursor = conn.cursor()
            cursor.execute(''' DELETE FROM employee WHERE empid = ?''', (empid,))
            conn.commit()
            print('Successfully deleted employee with EmployeeID : {}'.format(empid))
            f = open("log.txt", "a+")
            try:
                currenttime = datetime.datetime.now().strftime("%I:%M%p %B %d, %Y")
                f.write(currenttime + ' : ' + 'Deleted record with EmployeeID -> {}'.format(empid)+' \n')
            except Exception as e:
                print('error while updating into log file !!!')
                raise e
            finally:
                f.close()
        except Exception as e:
            print("error in delete operation !!!")
            conn.rollback()
            raise e
        finally:
            conn.close()


def main():
    """
    main execution function
    """
    welcome_message()
    employee_curd_operation()


if __name__ == "__main__":
    main()

