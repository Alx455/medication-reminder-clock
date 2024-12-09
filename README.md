"# medication-reminder-clock" 

## Setup
1. Create and activate a virtual environment (conda or venv)
2. Install required libraries with "pip install -r requirements.txt"
3. Ensure mysql installation on computer
4. Update DB.py to contain your mysql credentials
```python
    host="localhost",
    user="*Your username*",
    password="*Your password*",
    database="medication_clock"
```
5. Create the database and tables in the "database_table_creation.sql" file
```bash
    # Open the MySQL command-line client
    mysql -u <username> -p

    # Enter your MySQL password when prompted

    # Run the SQL file to create the database and tables
    SOURCE path/to/database_table_creation.sql;

    # Exit the MySQL client
    EXIT;
```