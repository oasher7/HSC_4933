################################################
# Odelia Asher #oasher@usf.edu                 #
#----------------------------------------------#
################################################

"""We want this script to encrypt data using symmetrical
encryption from the AnonyMate anonymizer function upon
user input.
We also want this script to allow the user to query the
following: Name, DoB, Sex, Blood Type ('blood_group')
"""

# Import libs
import json
import os
from anonymate.anonymizer import Anonymizer
from cryptography.fernet import Fernet

# Create an encryption key
Key_FILE = "encryption.key"

if os.path.exists(Key_FILE):
    with open(Key_FILE, "rb") as f:
        encryption_key = f.read()
else:
    encryption_key = Fernet.generate_key()
    with open(Key_FILE, "wb") as f:
        f.write(encryption_key)

# Initialize Anonymizer
anonymizer = Anonymizer(encryption_key=encryption_key)

# Patient profiles
profiles = [
    {
        'job': 'Agricultural engineer',
        'company': 'Phillips-Johnson',
        'ssn': '055-51-3629',
        'residence': '1107 Brian Coves\nSouth Jessica, UT 66862',
        'current_location': ('-81.6575675', '111.794874'),
        'blood_group': 'B+',
        'website': [
            'https://hurley.com/',
            'http://www.baker.info/',
            'http://silva-jones.com/',
            'https://www.mathews.com/'
        ],
        'username': 'nnelson',
        'name': 'Oscar Newman',
        'sex': 'M',
        'address': '2574 Scott Manors\nPort Aprilfort, MI 13337',
        'mail': 'wgraham@hotmail.com',
        'birthdate': (1927, 1, 19)
    },
    {
        'job': 'Engineer, civil (consulting)',
        'company': 'Guzman Inc',
        'ssn': '457-09-3674',
        'residence': '8014 Lambert Ways Apt. 285\nSouth Briannaside, KS 13217',
        'current_location': ('61.686331', '-42.036583'),
        'blood_group': 'A-',
        'website': [
            'http://gregory-martin.org/',
            'http://tanner.org/',
            'https://www.carr.org/'
        ],
        'username': 'lking',
        'name': 'Jeremy Wilson',
        'sex': 'M',
        'address': '9375 Thomas Alley Suite 536\nNorth Darren, AZ 22956',
        'mail': 'hdeleon@hotmail.com',
        'birthdate': (1996, 10, 12)
    },
    {
        'job': 'Information officer',
        'company': 'Green Inc',
        'ssn': '230-42-2169',
        'residence': 'Unit 6625 Box 0858\nDPO AE 52466',
        'current_location': ('-78.802646', '-47.996111'),
        'blood_group': 'A-',
        'website': [
            'https://www.watkins.com/',
            'http://johnson.org/'
        ],
        'username': 'timothycastro',
        'name': 'Kenneth Rhodes',
        'sex': 'M',
        'address': '7994 Pearson Square\nHannahmouth, FM 16699',
        'mail': 'sonya72@hotmail.com',
        'birthdate': (2003, 6, 15)
    },
    {
        'job': 'Contracting civil engineer',
        'company': 'Smith-Williamson',
        'ssn': '796-76-1297',
        'residence': '0041 Brittany Mountains\nNorth Harryshire, MN 69202',
        'current_location': ('66.422320','107.124001'),
        'blood_group': 'AB+',
        'website': [
            'http://www.nolan.com/'
        ],
        'username': 'debraphillips',
        'name': 'Nicole Richardson',
        'sex': 'F',
        'address': '303 Wong Trafficway Suite 883\nLake Kiara, MN 78039',
        'mail': 'andrew33@gmail.com',
        'birthdate': (2003, 9, 7)
    },
    {
        'job': 'Engineer, technical sales',
        'company': 'Moody-Meza', 'ssn': '574-63-6422',
        'residence': '74438 Moore Fall\nSouth Andrew, GA 64257',
        'current_location': ('38.089195','35.459581'),
        'blood_group': 'A+',
        'website': ['https://brooks-moore.com/'],
        'username': 'xlewis',
        'name': 'Gary Gamble',
        'sex': 'M',
        'address': '9929 Henderson Branch Suite 961\nLake Mary, AL 36478',
        'mail': 'ambercordova@yahoo.com',
        'birthdate': (1968, 8, 19)}
]

# Create a boolean question function for profile encryption
def encrypt_profile_question (question: str) ->bool:
    while True:
        encrypt_decision = input (f"{question} (Y/N): ").strip().upper()
        if encrypt_decision in ('Y', 'YES'):
            return True
        if encrypt_decision in ('N', 'NO'):
            return False

        print ("Invalid input. Please enter 'Y' or 'N'.")

# Ask user if they would like to encrypt patient profiles
encrypt_bool = encrypt_profile_question ("Would you like to encrypt the patient profiles?")

# Write Data if/else logic
if encrypt_bool == True:

    # Print profiles to terminal
    print("Unencrypted profiles:")
    print(profiles)

    # Turn data into string
    data_str = json.dumps(profiles, default=str)

    # Run anonymizer
    encrypted_profiles = anonymizer.encrypt_text(data_str)

    # Show encrypted data to user
    print ('Encrypted profiles:')
    print (encrypted_profiles)

if encrypt_bool == False:
    print (" Profile Encryption Restricted")

# Create a boolean question that allows the user to query: Name, DoB, Sex, or Blood Type
def profile_query (question:str) -> bool:
    while True:
        query_decision = input (f" {question} (Y/N):").strip().upper()
        if query_decision in ('Y', 'YES'):
            return True
        if query_decision in ('N', 'NO'):
            return False

        print ("Invalid input. Please enter 'Y' or 'N'.")

# Ask user if they would like to query a profile
query_selection = profile_query ("Would you like to query a profile?")

# Create a variable for the queries in the profile and the displayed queries
Query_field = ("Name", "DoB", "Sex", "Blood Type")
Query_profile = ("name", "birthdate", "sex", "blood_group")

# Write if logic for the query selection
if query_selection == True:
    print ("Profile Query Selection:")
    for index, item in enumerate(Query_field, start = 1):
        print (f"{index}. {item}")
    query_choice = input ("Please select a query:")
    query_choice = int (query_choice)
    if query_choice >=1 and query_choice <= len(Query_field):
        selected_field = Query_profile[query_choice-1]
        search_value = input (f" Please enter the {Query_field[query_choice-1]} you are looking for:")

        for profile in profiles:
            if str(search_value).lower() in str(profile[selected_field]).lower():
                print ("Profile found:")
                print (profile)
                break

        else:
            print ('No matching profile found.')

    else:
        print ("Invalid query selection.")

if query_selection == False:
    print ("No query selection")

