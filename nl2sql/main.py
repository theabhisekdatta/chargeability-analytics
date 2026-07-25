from sql_tool import SQLTOOL


llm_sql = SQLTOOL()

question = "Which location has the highest average chargeability?"

sql = llm_sql.generate_sql(question)

print("\nGenerated SQL:")
print(sql)

rows = llm_sql.execute_sql(sql)
print("\nQuery Results:")
for row in rows:
    print(row)