#test functions to retrieve country code
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

# Test the function
result = get_birthplace('ROMA')
print(f"Result: {result}")
