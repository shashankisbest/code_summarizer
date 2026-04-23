import ast


'''
this module is a parser for python language....
why not others? because the grammer is python's grammer

'''
code = "a = b + c"
tree1 = ast.parse(code)

print(tree1)

code = """
def factorial(a):    #it is a function definition
    if a == 1 or a == 0: return 0
    return a * factorial(a-1)
"""

tree2 = ast.parse(code)
print(type(tree2))

print(ast.dump(tree2, indent=4))
print("--"*10)

for node in ast.walk(tree1):
    print(type(node).__name__)

print("--"*10)


for node in ast.walk(tree2):
    if isinstance(node, ast.FunctionDef):
        args = [arg.arg for arg in node.args.args]
        print(f"Function: {node.name}, Args: {args}")

