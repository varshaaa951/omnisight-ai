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

sql = generate_sql(question, schema)

print("\nGenerated SQL:\n")
print(sql)