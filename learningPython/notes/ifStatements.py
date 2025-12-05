# an if statemnt is a block of code that exeutes intructions if a condition is true
#order of if statements matter, the first one that is true will execute
age = int(input("Age: "))

if age >= 18:
    print('You are legally allowed to vote')
elif age < 0:
    print('You sure you alive punk?')
else:
    print('No voting for you BUB!!')