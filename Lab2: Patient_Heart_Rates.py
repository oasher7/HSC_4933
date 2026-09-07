#################################################################################
#Odelia Asher # oasher@usf.edu
#################################################################################

""" A script that allows for someone to enter a patient number,
retrieve all patient stats, or retrieve specific patient stats.
This script should prompt the user for each input,
and utilize functions and arguments (*args) to allow for reproducability.
"""

# This dictionary contains the patients names and their heart rate samples
heart_rate_samples = {
    "J. Alvarez": [72,74,78],
    "M. Chen": [80,82],
    "R. Okafor": [65,68,70,66],
    "S. Patel": [90,95,92,88, 91],
    "T. Nguyen": [77,79],
    "L. Kowalski": [68,70,69],
    "D. Osei": [98, 101, 95, 99],
    "A. Whitfield": [74, 76, 75, 73],
}

# This function prompts the user to input the first initial of a patient's name
def patient_first_name_initial():
    first_name_initial  = input ("Please enter the patient's first name initial:")
    return first_name_initial.upper()

# This function prompts the user to input the last name of a patient
def patient_last_name():
    last_name = input ("Please enter the patient's last name:")
    return last_name.title()

# This function combines the patient's first name initial and last name
def patient_name (first_name_initial, last_name):
    patient_name = first_name_initial + "." + " " + last_name
    return patient_name

# This function retrieves a patient's heart rate samples based on the name entered by the user
# If the patient's name is not found, the function returns None
def heart_rate_sample(patient_name):
    if patient_name in heart_rate_samples:
        return heart_rate_samples[patient_name]
    else:
        return None

# This function assigns each patient in the dictionary a unique number, starting from 1 instead of 0
def patient_list():
    for number, patient in enumerate(heart_rate_samples, start = 1):
        print (number, patient)

# This function allows a user to select multiple patients
# by entering the patient numbers displayed on the list
# The function then displays the selected patients' names and their corresponding heart rate samples
def specific_patients(*args):
    patients = list(heart_rate_samples.keys())

    for number in args:
        patient = patients [number-1]
        print (patient, heart_rate_samples[patient])

# This function allows a user to view all patients' names and their corresponding heart rate samples
def all_patients_stats():
    for patients, samples in heart_rate_samples.items():
        print (patients, samples)

# This function provides a list of choices that allows a user to select
# how they want to view a patient's heart rate samples

def patient_selection():
    print ("1. Single patient")
    print ("2. Multiple patients")
    print ("3. All Patients")

    patient_choice = input("Please select an option:")
    return patient_choice

# This variable stores the user's menu selection
choice = patient_selection()
# This loop prevents the user from continuing to the next step
# if they enter an invalid selection
while choice != "1" and choice != "2" and choice != "3":
    print ("Please select a valid option:")
    choice = patient_selection()

# If a user selects option 1, which is single patient, the if statement prompts the
# user to enter the patient's first initial, followed by the patient's last name
# If the patient's name is found, their heart rate samples are displayed
# If the patient's name is not found, the function returns None
if choice == "1":
    first_initial = patient_first_name_initial()
    last_name = patient_last_name()
    name = patient_name(first_initial, last_name)

    if heart_rate_sample(name) is None:
        print ("Patient not found")
    else:
        print (heart_rate_sample(name))

# If a user selects option 2, which is multiple patients, the function displays
# a list of patients with their assigned unique patient number and prompts the
# user to enter patient numbers that they would like to see
elif choice == "2":
    patient_list()
    patient_numbers = input ("Please enter the patient numbers you would like to view:")
    patient_numbers = patient_numbers.split(",")
    patient_numbers = [int(number.strip())for number in patient_numbers]

# If a user enters a patient number that is not within the given range
# the user is prompted to enter the patients' number again
    while any(number <1 or number > len(heart_rate_samples) for number in patient_numbers):
        print ("Please select valid patient numbers")
        patient_numbers = input("Please enter the patient numbers you would like to view:")
        patient_numbers = patient_numbers.split(",")
        patient_numbers = [int(number.strip()) for number in patient_numbers]
    specific_patients (*patient_numbers)

# If a user selects option 3, which is all patients, a list of patients
# with the heart rate samples is displayed
elif choice == "3":
    all_patients_stats()