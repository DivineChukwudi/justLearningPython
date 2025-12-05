#  Part  1

userName = input("Enter full name: ")
userAge = input("Enter age: ")
userHeight = input("Enter height in meters: ")

print(type(userName))
print(type(userAge))
print(type(userHeight))

#  Part  2

userAge = int(userAge)
userHeight = float(userHeight)

# years left till 100
yearsLeft = 100 - userAge
print("You will turn 100 in ", yearsLeft, " years.")

#  Part  3

userNameCaps = userName.upper()
print("Your name in uppercase is:", userNameCaps)

userChar = len(userName) - userName.count(' ') 
print("Number of characters in your name (excluding spaces): ", userChar)


checkChar = userName.lower().count('a')
if checkChar > 0:
    print("Your name contains \"a\".")
else:
    print("Your name does not contain \"a\".")


#  Part  4

userWeight = float(input("Enter weight in kg: "))

bmi = round(userWeight / (userHeight ** 2))
print("Your BMI is: ", bmi)

if bmi < 18.5:
    print("You are underweight.")
elif 18.5 <= bmi < 25:
    print("You have a normal weight.")
elif 25 <= bmi < 30:
    print("You are overweight.")
else:
    print("You are obese.")