userName = input("Enter full name: ")
userAge = int(input("Enter age: "))
userCountry = input("Enter country of residence: ")
userQuote = input("Enter your favorite quote: ")


retireAge = 65 - userAge

userQuote = userQuote.split()

wordsInQuote = 0
for word in userQuote:
    wordsInQuote += 1

countryUpper = userCountry.upper()


firstName = userName.split()[0]
lastName = userName.split()[-1]


print('____________________________________')
print('           VIRTUAL ID CARD          ')
print('____________________________________')
print("Name                : ", userName)
print("Initials            : ", firstName[0] + lastName[0])
print("Age                 : ", userAge)
print("Country             : ", countryUpper)
print("Years to retire     : ", retireAge)
print("Quote Words         : ", wordsInQuote)
#print("Quote               : ", userQuote)

# Correction for displaying the quote properly
print("Quote               : ", ' '.join(userQuote))
print('____________________________________')



