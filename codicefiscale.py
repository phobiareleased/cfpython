import csv

def load_codici():
    codici = {}
    with open('lista-codici.csv', mode='r') as infile:
        reader = csv.reader(infile, delimiter=';')  # Specify the correct delimiter
        for row in reader:
            if len(row) >= 2:  # Ensure the row has at least two columns
                codici[row[0].upper()] = row[1].upper()  # Store keys and values in uppercase
    return codici

mydict = load_codici()

def get_birthplace(birthplace):
    birthplace = birthplace.upper()

    if birthplace in mydict:
        return mydict[birthplace]
    else:
        print(f"Error: '{birthplace}' not found in mydict")
        return None

def calculate_codice_fiscale(surname, name, birthyear, birthmonth, birthday, sex, birthplace):
    vowels = ['A', 'E', 'I', 'O', 'U']
    
    surname = surname.upper()
    surname_consonants = [c for c in surname if c not in vowels][:3]
    surname = surname_consonants

    name = name.upper()
    name_consonants = [c for c in name if c not in vowels]
    name_consonants = [name_consonants[0], name_consonants[2], name_consonants[3]]
    name = name_consonants

    birthyear = str(birthyear)[2:]

    birthmonth = str(birthmonth)
    month_mapping = {
        '1': 'A',
        '2': 'B',
        '3': 'C',
        '4': 'D',
        '5': 'E',
        '6': 'H',
        '7': 'L',
        '8': 'M',
        '9': 'P',
        '10': 'R',
        '11': 'S',
        '12': 'T'
    }
    birthmonth = month_mapping.get(birthmonth, '')
    
    if sex == 'F':
        birthday += 40
    birthday = str(birthday)

    birthplace = get_birthplace(birthplace)

    surname = ''.join(surname)
    name = ''.join(name)

    return surname + name + str(birthyear) + str(birthmonth) + str(birthday) + str(birthplace)

    
def get_verification_bit(surname, name, birthyear, birthmonth, birthday, birthplace, birthprov):
    #define later
    return None

def input_data():
    surname = input("Enter your surname: ")
    name = input("Enter your name: ")
    birthyear = int(input("Enter your birth year: "))
    birthmonth = int(input("Enter your birth month: "))
    birthday = int(input("Enter your birth day: "))
    sex = input("Enter your sex (M/F): ")
    italy = input("Do you live in Italy? (Y/N): ")
    if italy == 'Y' or italy == 'y':
        birthplace = input("Enter your the Province you were born in: ")
    else:
        birthplace = input("Enter the country you were born in: ") 
         

    result = calculate_codice_fiscale(surname, name, birthyear, birthmonth, birthday, sex, birthplace)
    print(result)

if __name__ == '__main__':
    input_data()
