import pymysql
from pymysql.cursors import DictCursor #To get dictionary-like rows with MySQLdb
from contextlib import contextmanager
from logging_setup import setup_logger

logger = setup_logger('db_helper')

@contextmanager
def get_db_cursor(commit=False):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        database='expense_manager',
        cursorclass = DictCursor # DictCursor for dictionary-like rows
    )
    if connection.open:
        print("Connection Succesful")
    else:
        print("Connection Unsuccesful")

    cursor = connection.cursor(DictCursor)
    yield cursor
    if commit:
        connection.commit()

    cursor.close()
    connection.close()

def fetch_all_records():
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses;")
        expenses = cursor.fetchall()
        for expense in expenses:
            print(expense)

def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses where expense_date= %s ", (expense_date,))
        expenses = cursor.fetchall()
        return expenses

def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with date:{expense_date}, amt:{amount}, category:{category}, notes:{notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) Values (%s, %s, %s,%s)"
        , (expense_date, amount, category, notes)
        )

def delete_expense(expense_date):
    logger.info(f"delete_expense with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "DELETE FROM expenses WHERE expense_date = %s", (expense_date,)
        )

def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary with {start_date}, {end_date}")
    with get_db_cursor(commit=True) as cursor:
        data = cursor.execute(
        '''select category, sum(amount) as total
        from expenses where expense_date 
        between %s and %s
        group by category;''', (start_date, end_date)
        )
        data =cursor.fetchall()
        return data

def fetch_expenses_monthly():
    logger.info("fetch_expenses_monthly")
    with get_db_cursor(commit=True) as cursor:
        data = cursor.execute(
            '''
            SELECT MIN(DATE_FORMAT(expense_date, '%m')) AS month_index ,DATE_FORMAT(expense_date, '%M') AS month,
            SUM(amount) AS total_amount
                FROM expenses
                GROUP BY month
                ORDER BY month_index
            '''
        )
        data = cursor.fetchall()
        return data

if __name__ == "__main__":
    # expenses = fetch_expenses_for_date("2024-09-30")
    # print(expenses)
    # delete_expense("2024-08-25")
    # summary = fetch_expense_summary("2024-08-01","2024-08-05")
    # for record in summary:
    #     print(record)
    monthly_summary = fetch_expenses_monthly()
    for record in monthly_summary:
        print(record)