# calculator_tool.py

import re
import operator

# Supported operations
OPERATIONS = {
    'add': operator.add,
    'plus': operator.add,
    'sum': operator.add,
    '+': operator.add,

    'subtract': operator.sub,
    'minus': operator.sub,
    '-': operator.sub,

    'multiply': operator.mul,
    'times': operator.mul,
    '*': operator.mul,

    'divide': operator.truediv,
    'divided': operator.truediv,
    '/': operator.truediv,
}

# Core function
def calculate(expression: str):
    expression = expression.lower()

    # Extract numbers and operation
    numbers = re.findall(r'\d+(?:\.\d+)?', expression)
    operator_word = next((word for word in OPERATIONS if word in expression), None)

    if len(numbers) != 2 or not operator_word:
        return " I can only calculate simple math with two numbers and one operation."

    num1, num2 = float(numbers[0]), float(numbers[1])
    try:
        result = OPERATIONS[operator_word](num1, num2)
        if result.is_integer():
            result = int(result)
        return f" The result is: {result}"
    except ZeroDivisionError:
        return " Division by zero is not allowed."
    except Exception as e:
        return f" Calculation error: {str(e)}"
