# Initial dataflow facts (constants assigned to variables)
initial_facts = {
    'x': None,
    'y': None
}

# Flow function for assignment statements
def assign_flow_function(dest, source):
    return {dest: source}

# Flow function for conditional statements
def conditional_flow_function(condition):
    return {}  # No information flows out, because we don't know which branch will be taken

# Flow function for print statements
def print_flow_function(variable):
    return {}  # No information flows out, just an output

# Example program
program = [
    ('x', 'y + 5'),        # x = y + 5
    ('if x > 10:',),       # if x > 10:
    ('print(x)',)          #     print(x)
]

# Analysis using flow functions
facts_at_points = []

current_facts = initial_facts.copy()
for statement in program:
    if statement[0] == 'if x > 10:':
        facts_at_points.append(current_facts.copy())  # Save facts before the conditional
        current_facts = conditional_flow_function('x > 10')
    elif statement[0].startswith('print'):
        facts_at_points.append(current_facts.copy())
        current_facts = print_flow_function(statement[0].split('(')[1].split(')')[0])
    else:
        dest, source = statement
        current_facts.update(assign_flow_function(dest, source))

facts_at_points.append(current_facts.copy())  # Save facts after the last statement

# Print the resulting facts at each program point
for i, facts in enumerate(facts_at_points):
    print(f"Program point {i}: {facts}")

