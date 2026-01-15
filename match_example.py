# Example using match to check against predefined lists

fruits = ['apple', 'banana', 'orange', 'grape']
vegetables = ['carrot', 'broccoli', 'spinach', 'potato']
colors = ['red', 'blue', 'green', 'yellow']

def categorize_item(item):
    match item:
        case item if item in fruits:
            return f"{item} is a fruit"
        case item if item in vegetables:
            return f"{item} is a vegetable"
        case item if item in colors:
            return f"{item} is a color"
        case _:
            return f"{item} is not in any predefined list"

# Test examples
print(categorize_item('apple'))    # apple is a fruit
print(categorize_item('carrot'))   # carrot is a vegetable
print(categorize_item('red'))     # red is a color
print(categorize_item('computer')) # computer is not in any predefined list