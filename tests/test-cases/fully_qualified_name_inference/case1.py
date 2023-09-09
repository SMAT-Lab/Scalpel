from random import choices

data = [41, 50, 29]
random_choices = choices(data, k=len(data))
print(random_choices)
all(random_choices)
any(random_choices)
