CLI Utility to calculate Italian Fiscal Code following the directives outlined at https://it.wikipedia.org/wiki/Codice_fiscale

# Algorithm Overview

This follows the algorithm described at https://en.wikipedia.org/wiki/Italian_fiscal_code. It is a 16 digit code that serves to Identify Italian citizens, used for a myriad of services, from the tax office to university logins. 

The first three digits (1-3/16) are calculated by taking the first three consonants of the surname, in case there are not enough it takes the first available vowels, in the same order as the name. Be there less than three letters in the surname (ex. Wu), a simple 'X' replaces the empty digit.
```
    if len(surname_consonants) >= 3:

        surname = surname_consonants[:3]

    elif len(surname_consonants) == 2 and len(surname_vowels) >= 1:

        surname = surname_consonants + surname_vowels[:1]

    elif len(surname_consonants) == 1 and len(surname_vowels) >= 2:

        surname = surname_consonants + surname_vowels[:2]

    elif len(surname) < 3:

        surname = surname + 'X' * (3 - len(surname))
```

To calculate the next three digits (4-6/16) take the first, third and fourth consonants of the first name, be there less than four, the first three are used. If the name has less than 3 consonants, it follows the same rules as above
```
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
```

The next 5 digits (7-11/16) are calculated as follows: for the first two (7-9) take the last two digits of the birth year. 
For the month, the number is transformed into a letter following the map I define in the code below
```
    month_mapping = {

        '1': 'A','2': 'B','3': 'C','4': 'D','5': 'E','6': 'H',

        '7': 'L','8': 'M','9': 'P','10': 'R','11': 'S','12': 'T'

    }
```
For the last two digits of this section (9-11) we take the day of the birthday, if the natural born is male the number remains unchanged, if they are female, add 40 (ex. Albert born on the 9th would have 09, Giovanna born on the same day would have 49).

Moving on to the next four digits (12-15/16), the Belfiore code is used. The Belfiore code is used as _codice catastale_ (registry code), which comprises one letter, then three digits. Each single Italian town (_comune_) has its own code, for foreign countries, the same format is used, but all foreign countries begin with a 'Z'.
For the complete list of the Italian towns' registry codes, see [here](https://web.archive.org/web/20160819012136/http://www.agenziaentrate.gov.it/wps/wcm/connect/321b0500426a5e2492629bc065cef0e8/codicicatastali_comuni_29_11_2010.pdf?MOD=AJPERES&CACHEID=321b500426a5e2492629bc065cef0e8); for the complete list of foreign countries' registry codes see [here](http://www.arcrealestate.it/arc_group_intranet/tabella_stati_esteri.pdf).

The final digit is a check bit. This check bit is calculated by separating the digits obtained so far into two arrays, Odd and Even, starting with index 0 as odd(usually counting in computer science starts at 0, not 1). Once these arrays are obtained they must be translated from alphanumerical digits to numbers, the conversion will be shown in the code later. Once these arrays are converted, all of the digits are summed together. To find the numerical value of the check bit we take this sum and find the remainder when divided by 26 (we use the modulo function for this). Once this value is found it also will be converted to an alphanumerical value following the mapping described below:
```
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

    odd_sum = 0

    even_sum = 0

    for index, char in enumerate(codice_fiscale_incomplete):

        if index % 2 == 0:  # Treat index 0 as odd, index 1 as even, etc.

            odd_sum += odd_mapping[char]

            print(f"Index {index} (odd): char {char}, odd_sum {odd_sum}")

        else:  # Treat index 1 as even, index 2 as odd, etc.

            even_sum += even_mapping[char]

            print(f"Index {index} (even): char {char}, even_sum {even_sum}")

    total_sum = odd_sum + even_sum

    remainder = total_sum % 26

    verification_bit = remainder_mapping[remainder]

    return verification_bit
```

Add all of the digits together and that's it. 

In real-world applications it is possible that two people can have the same codice fiscale, in such edge cases, the Anagrafe or Agenzia delle Entrate may give a codice fiscale that does not conform to the algorithm, these are fully valid codice fiscale, as this generator serves firstly the purpose of being a fun and interesting project to get me back into algorithms.
There are many issues with the way the codice fiscale is generated, such as the fact that every 100 years people with different birthdays may have the same code, and that the check bit is not fully robust as it does not cover all typing mistakes (ex. MR*YW*LM80A01H501H and MR*WY*LM80A01H501H are both valid with the same check bit).
