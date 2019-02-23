### Project Title
The project is "Employee Management System". Which deals with creation and maintenance of employee and department 
records with the ability to add, edit and delete the data from the system.

### Getting Started
Copy the 'employee' project on your IDE. The lib folder consists of file 'curd' where the execution begins.
After execution new files 'testdb.sqlite' and 'log.txt' files will be generated in the same lib folder.

### Prerequisites
Following software/modules required to run the project.
1. Python3
2. sqlite3

Other modules used are as follows,
1. os
2. sys
3. datetime

### Running Project
To run the project go to file 'curd' and run as script. The execution begins from the main() function, which internally
calls other functions.

While running user will be prompted for the type of execution he wants. Based on user input the different operations
will be performed.

Different operations supported are as follows,
1. Record creation both in 'employee' and 'department' tables.
2. Record update for all employee attributes but except 'EmployeeID' as it is unique.
3. Retrieve record based on 'EmployeeID' as well as 'Firstname'
4. Deletion of record and which accordingly updates both tables.

### Technical details
1. Project is built with IDE Pycharm
2. It is compatible with all OS.
3. 'testdb.sqlite' and 'log,txt' files will be generated after execution.
   'testdb.sqlite' -> It is sql db file to create and store records.
   'log.txt' -> It is log file to keep track of all operations.
Note : 'testdb.sqlite' and 'log.txt' files will remain always after creation until explicitly deleted.

### References
Websites referred:
1. https://www.python.org/
2. https://www.python.org/dev/peps/pep-0008/
2. https://www.pythoncentral.io/introduction-to-sqlite-in-python/
3. http://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html

Books referred:
1. Dive into python3 by Mark Pilgrim
2. Core Python Programming by P. Nageshwara Rao
3. Learning python by Lutz M

###
Author
Shashidhar Yalagi