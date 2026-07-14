import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from ai import generate_sql

schema = """
Table customers
id integer
name text
email text

Table orders
id integer
customer_id integer
amount numeric
order_date date
"""

question = "How many customers do we have?"

result = generate_sql(question, schema)

print("\n========== SQL VALIDATION ==========\n")

if result["success"]:

    print("SQL Validation : PASSED\n")
    print("Generated SQL:\n")
    print(result["sql"])

else:

    print("SQL Validation : FAILED\n")
    print("Reason:")
    print(result["error"])
    print("\nExecution stopped for security reasons.")