import csv

# Import the codici catastali from the csv file
def load_codici():
    codici = {}
    with open('lista-codici.csv', mode='r') as infile:
        reader = csv.reader(infile, delimiter=';')  # Specify the correct delimiter
        for row in reader:
            if len(row) >= 2:  # Ensure the row has at least two columns
                codici[row[0].upper()] = row[1].upper()  # Store keys and values in uppercase
    return codici

mydict = load_codici()

# Search for the birthplace in the dictionary
def get_birthplace(birthplace):
    birthplace = birthplace.upper()

    if birthplace in mydict:
        return mydict[birthplace]
    else:
        print(f"Error: '{birthplace}' no Country or Province found in database")
        exit()

def calculate_codice_fiscale(surname, name, birthyear, birthmonth, birthday, sex, birthplace):

    vowels = ['A', 'E', 'I', 'O', 'U']

    surname = list(filter(str.isalpha, surname.upper()))  # Filter out non-alphabetic characters and convert to uppercase
    name = list(filter(str.isalpha, name.upper()))  # Filter out non-alphabetic characters and convert to uppercase

    # Iterate over the surname and name to create two seperate arrays of ordered consonants and vowels
    surname_consonants = [char for char in surname if char not in vowels]
    surname_vowels = [char for char in surname if char in vowels]
    name_consonants = [char for char in name if char not in vowels]
    name_vowels = [char for char in name if char in vowels]

    # Calculate the surname code
    if len(surname_consonants) >= 3:
        surname = surname_consonants[:3]
    elif len(surname_consonants) == 2 and len(surname_vowels) >= 1:
        surname = surname_consonants + surname_vowels[:1]
    elif len(surname_consonants) == 1 and len(surname_vowels) >= 2:
        surname = surname_consonants + surname_vowels[:2]
    elif len(surname) < 3:
        surname = surname + 'X' * (3 - len(surname))

    # Calculate the name code
    if len(name_consonants) >= 4:
        name = name_consonants[0] + name_consonants[2] + name_consonants[3]
    elif len(name_consonants) == 3:
        name = name_consonants 
    elif len(name_consonants) == 2 and len(name_vowels) >= 1:
        name = name_consonants + name_vowels[:1]
    elif len(name_consonants) == 1 and len(name_vowels) >= 2:
        name = name_consonants + name_vowels[:2]
    elif len(name_consonants) == 0 and len(name_vowels) >= 3:
        name = name_vowels[:3]
    elif len(name) < 3:
        name = name + 'X' * (3 - len(name))
    
    birthyear = str(birthyear)[2:]

    birthmonth = str(birthmonth)

    month_mapping = {
        '1': 'A','2': 'B','3': 'C','4': 'D','5': 'E','6': 'H',
        '7': 'L','8': 'M','9': 'P','10': 'R','11': 'S','12': 'T'
    }

    birthmonth = month_mapping.get(birthmonth, '')
    
    if sex == 'F' or sex == 'f':
        birthday += 40
    
    if birthday < 10:
        birthday = '0' + str(birthday)
    
    birthday = str(birthday)

    birthplace = get_birthplace(birthplace)

    surname_code = ''.join(surname)
    name_code = ''.join(name)

    return surname_code + name_code + str(birthyear) + str(birthmonth) + str(birthday) + str(birthplace)

    
def get_verification_bit(codice_fiscale_incomplete):
    odd_mapping = {
        '0': 1, '1': 0, '2': 5, '3': 7, '4': 9, '5': 13, '6': 15, '7': 17, '8': 19, '9': 21,
        'A': 1, 'B': 0, 'C': 5, 'D': 7, 'E': 9, 'F': 13, 'G': 15, 'H': 17, 'I': 19, 'J': 21,
        'K': 2, 'L': 4, 'M': 18, 'N': 20, 'O': 11, 'P': 3, 'Q': 6, 'R': 8, 'S': 12, 'T': 14,
        'U': 16, 'V': 10, 'W': 22, 'X': 25, 'Y': 24, 'Z': 23
    }
    
    even_mapping = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9,
        'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19,
        'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25
    }
    
    remainder_mapping = {
        0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J',
        10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T',
        20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'
    }
    
    codice_fiscale_incomplete = codice_fiscale_incomplete.upper()  # Ensure the codice fiscale is uppercase

    odd_sum = 0
    even_sum = 0
    
    for index, char in enumerate(codice_fiscale_incomplete):
        if index % 2 == 0:  # Treat index 0 as odd, index 1 as even, etc.
            odd_sum += odd_mapping[char]
        else:  # Treat index 1 as even, index 2 as odd, etc.
            even_sum += even_mapping[char]
    
    total_sum = odd_sum + even_sum
    remainder = total_sum % 26 # Calculate the remainder of the total sum divided by 26
    verification_bit = remainder_mapping[remainder] # Retrieve the verification bit from the remainder mapping
    
    return verification_bit

def input_data():
    surname = input("Enter your surname: ")
    name = input("Enter your name: ")

    birthyear = int(input("Enter your birth year: "))
    birthmonth = int(input("Enter your birth month: "))
    birthday = int(input("Enter your birth day: "))

    sex = input("Enter your sex (M/F): ")

    italy = input("Were you born in Italy? (Y/N): ")
    if italy == 'Y' or italy == 'y':
        birthplace = input("Please enter the Province you were born in: ")
    else:
        birthplace = input("Please enter the Country you were born in: ")

    codice_fiscale_incomplete = calculate_codice_fiscale(surname, name, birthyear, birthmonth, birthday, sex, birthplace)
    verification_bit = get_verification_bit(codice_fiscale_incomplete)
    codice_fiscale = codice_fiscale_incomplete + verification_bit

    print(codice_fiscale)

if __name__ == '__main__':
    input_data()
