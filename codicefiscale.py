import csv

def load_codici():
    codici = {}
    with open('lista-codici.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2:  # Ensure the row has at least two columns
                codici[row[0]] = row[1]
    return codici

mydict = load_codici()


def calculate_codice_fiscale(surname, name, birthyear, birthmonth, birthday, sex, birthplace, birthprov):
    vowels = ['A', 'E', 'I', 'O', 'U']
    
    surname = surname.upper()
    surname_consonants = [c for c in surname if c not in vowels][:3]
    surname = surname_consonants

    name = name.upper()
    name_consonants = [c for c in name if c not in vowels]
    name_consonants = [name_consonants[0], name_consonants[2], name_consonants[3]]
    name = name_consonants

    birthyear = str(birthyear)[2:]

    if birthmonth == 1:
        birthmonth = 'A'
    elif birthmonth == 2:
        birthmonth = 'B'
    elif birthmonth == 3:
        birthmonth = 'C'
    elif birthmonth == 4:
        birthmonth = 'D'
    elif birthmonth == 5:
        birthmonth = 'E'
    elif birthmonth == 6:
        birthmonth = 'H'
    elif birthmonth == 7:
        birthmonth = 'L'
    elif birthmonth == 8:
        birthmonth = 'M'
    elif birthmonth == 9:
        birthmonth = 'P'
    elif birthmonth == 10:
        birthmonth = 'R'
    elif birthmonth == 11:
        birthmonth = 'S'
    elif birthmonth == 12:
        birthmonth = 'T'
    
    birthday = str(birthday)
    if sex == 'F':
        birthday += 40

    birthprov, birthplace = get_birthplace(birthplace, birthprov)

    verification_bit = get_verification_bit(surname, name, birthyear, birthmonth, birthday, birthplace, birthprov)
    return birthplace, birthprov


def get_birthplace(birthplace, birthprov):
    birthplace = birthplace.upper()
    birthprov = birthprov.upper()

    if birthplace == 'Y':
        birthprov = 'Z' + mydict[birthprov]
        return birthprov, birthprov
    else:
        birthplace = mydict[birthplace]
        return birthprov, birthplace
    
def get_verification_bit(surname, name, birthyear, birthmonth, birthday, birthplace, birthprov):
    #define later
    return None

def input_data():
    surname = input("Enter your surname: ")
    name = input("Enter your name: ")
    birthyear = int(input("Enter your birth year: "))
    birthmonth = int(input("Enter your birth month: "))
    birthday = int(input("Enter your birth day: "))
    birthplace = input("Do you live in Italy? (Y/N): ")
    if birthplace == 'Y':
        birthprov = input("Enter your birth province: ")
    else:
        birthprov = ''
        birthplace = input("Enter your birth Country: ")        

    calculate_codice_fiscale(surname, name, birthyear, birthmonth, birthday, birthplace, birthprov)

get_birthplace('Roma', 'RM')
