from services.python_executor import python_executor

code = """
print("Hello Athena")
print(10 + 20)
"""

result = python_executor.execute(code)

print(result)