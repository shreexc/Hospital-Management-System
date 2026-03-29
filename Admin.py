from Doctor import Doctor
from Patient import Patient


class Admin:
    """A class that deals with the Admin operations"""
    def __init__(self, username, password, address = ''):
        """
        Args:
            username (string): Username
            password (string): Password
            address (string, optional): Address Defaults to ''
        """

        self.__username = username
        self.__password = password
        self.__address =  address

    def view(self, a_list):
        """
        print a list
        Args:
            a_list (list): a list of printables
        """
        for index, item in enumerate(a_list):
            print(f'{index+1:3}|{item}')

    def login(self) :
        """
        A method that deals with the login
        Raises:
            Exception: returned when the username and the password ...
                    ... don`t match the data registered
        Returns:
            string: the username
        """
    
        print("-----Login-----")
        #Get the details of the admin

        username = input('Enter the username: ')
        password = input('Enter the password: ')

        # check if the username and password match the registered ones
        if username == self.__username and password == self.__password:
            return username
        return False
    
    def print_patient(self):
        print(f'{"ID":<3}|{"Full Name":^30}|{"Doctor`s Full Name":^30}|{"Age":^5}|{"Mobile":^15}|{"Address":^10}|{"Symptoms":^15}')
        print("-" * 115)

    def add_patient_file(self, patients, files="Patient.txt"):
        with open(files, 'w') as file:
            for patient in patients:
                file.write(patient.to_files() + '\n')

    def show_patient(self, files="Patient.txt"):
        patients = []
        try:
            with open(files, 'r') as file:
                for line in file:
                    if line.strip() != "":
                        patients.append(Patient.from_files(line))
        except FileNotFoundError:
            pass
        return patients

    def find_index(self,index,doctors):
        
            # check that the doctor id exists          
        if index in range(0,len(doctors)):
            
            return True

        # if the id is not in the list of doctors
        else:
            return False
        
    def add_del_patient(self, patients):
        print('Choose an option: ')
        print(' 1 - Add a patient')
        print(' 2 - Delete a patient')

        op = input('Input: ')

        if op == '1':
            self.add_patient(patients)

        elif op == '2':
            self.del_patient(patients)

        else: print('Invalid Option')

    def add_doctor(self, doctors, files="Doctor.txt"):
            with open(files, 'w') as file:
                for doctor in doctors:
                    file.write(doctor.to_doc_files() + '\n')
        
    def show_doctor(self, files="Doctor.txt"):
            doct = []

            try:
                with open(files, 'r') as file:
                    for line in file:
                        d = Doctor.from_doc_files(line)
                        if d:
                            doct.append(d)
            except FileNotFoundError:
                open(files, 'w').close()

            return doct
            
    def get_doctor_details(self) :
        """
        Get the details needed to add a doctor
        Returns:
            first name, surname and ...
                            ... the speciality of the doctor in that order.
        """
        first_name = input('Enter the first name: ')
        surname = input('Enter the surname: ')
        speciality = input('Enter the speciality: ')
        return first_name, surname, speciality
    
    def assign_relocate(self, patients, doctors):
        print('Choose an option: ')
        print(' 1 - Assign a doctor')
        print(' 2 - Relocate a doctor')

        op = input('Input: ')
        if op == '1':
            self.assign_doctor_to_patient(patients, doctors)

        elif op == '2':
            self.relocate_doctor(doctors, patients)

        else: print("Invalid option")

    def doctor_management(self, doctors):
        """
        A method that deals with registering, viewing, updating, deleting doctors
        Args:
            doctors (list<Doctor>): the list of all the doctors names
        """

        print("-----Doctor Management-----")

        # menu
        print('Choose the operation: ')
        print(' 1 - Register')
        print(' 2 - View')
        print(' 3 - Update')
        print(' 4 - Delete')

        op = input('Input: ')

        # register
        if op == '1':
            print("-----Register-----")

            # get the doctor details
            print('Enter the doctor\'s details:')
            first_name, surname, speciality = self.get_doctor_details()

            # check if the name is already registered
            name_exists = False
            for doctor in doctors:
                if first_name == doctor.get_first_name() and surname == doctor.get_surname():
                    print('Name already exists.')
                    name_exists = True
                    break

            if not name_exists:
                doctors.append(Doctor(first_name, surname, speciality))
                self.add_doctor(doctors)
                print('Doctor registered.')

            else: print("Doctor not registered.")

        # View
        elif op == '2':
            print("-----List of Doctors-----")
            self.view(doctors)

        # Update
        elif op == '3':
            while True:
                print("-----Update Doctor`s Details-----")
                print('ID |          Full name           |  Speciality')
                self.view(doctors)

                try:
                    index = int(input('Enter the ID of the doctor: ')) - 1
                    if self.find_index(index, doctors):
                
                        break
                        
                    else:
                        print("Doctor not found")

                    
                        # doctor_index is the ID mines one (-1)
                        

                except ValueError: # the entered id could not be changed into an int
                    print('The ID entered is incorrect')

            # menu
            print('Choose the field to be updated:')
            print(' 1 First name')
            print(' 2 Surname')
            print(' 3 Speciality')
            try:
                field_choice = int(input('Input: '))
                doctor_to_update = doctors[index]
                if field_choice == 1:
                    doctor_to_update.set_first_name(input('Enter the new first name: '))
                elif field_choice == 2:
                    doctor_to_update.set_surname(input('Enter the new surname: '))
                elif field_choice == 3:
                    doctor_to_update.set_speciality(input('Enter the new speciality: '))
                else:
                    print('Invalid field choice.')
                    return
                
                self.add_doctor(doctors)
                print("Updated successfully.")

            except ValueError:
                print('The input entered is incorrect.')

        # Delete
        elif op == '4':
            print("-----Delete Doctor-----")
            print('ID |          Full Name           |  Speciality')
            self.view(doctors)

            doctor_index = input('Enter the ID of the doctor to be deleted: ')
            try:
                doctor_index = int(doctor_index) - 1
                if self.find_index(doctor_index, doctors):
                    doctors.pop(doctor_index)
                    self.add_doctor(doctors)
                    print('Doctor deleted.')
                else:
                    print('The id entered was not found.')
            except ValueError:
                print('The id entered is incorrect.')

        else:
            print('Invalid operation chosen. Check your spelling!')

    def add_patient(self, patients):
        print('-----Add patient-----')

        first_name = input('Enter first name: ')
        surname = input('Enter surname: ')
        age = int(input('Enter age: '))
        mobile = int(input("Enter mobile: "))
        address = input('Enter address: ')

        n_patient = Patient(first_name, surname, age, mobile, address)
        patients.append(n_patient)

        self.add_patient_file(patients)
        print("New patient added successfully.")
        

    def del_patient(self, patients, files="Patient.txt"):
        print('-----Delete patient-----')

        if not patients:
            print("Patient doesn't exist")
            return
        
        for i, patient in enumerate(patients, start=1):
            print(f'{i} - {patient.full_name()}')

        while True:
            try:
                opt = int(input('Enter patient ID to remove: '))
                if 1 <= opt <= len(patients):
                    removed = patients.pop(opt - 1)
                    print(f'{removed.full_name()} was removed.')
                    break
                else: print('Invalid ID')
            except ValueError:
                print('Enter a valid ID')
        self.add_patient_file(patients, files)    

    def view_patient(self, patients):
        """
        print a list of patients
        Args:
            patients (list<Patients>): list of all the active patients
        """
        print("-----View Patients-----")
        print('ID |        Full Name        |     Doctor`s Full Name     | Age |     Mobile     | Address |   Symptoms   ')
        self.view(patients)

    def patient_family(self, patients):

        if len(patients) == 0:
            print("No patients available")
            return
        
        family = {}

        for patient in patients:
            full_name = patient.full_name()
            surname = patient.surname()

            if surname not in family:
                family[surname] = []
                family[surname].append(patient)
        print("-----View patients of same family-----")

        for surname, members in family.items():
            print(f"\nFamily Surname: {surname}")
            print('ID |        Full Name        |     Doctor`s Full Name     | Age |     Mobile     | Address |   Symptoms   ')
            self.view(members)

    def assign_doctor_to_patient(self, patients, doctors):
        """
        Allow the admin to assign a doctor to a patient
        Args:
            patients (list<Patients>): the list of all the active patients
            doctors (list<Doctor>): the list of all the doctors
        """
        print("-----Assign-----")

        print("-----Patients-----")
        print('ID |        Full Name        |     Doctor`s Full Name     | Age |     Mobile     | Address |   Symptoms   ')
        self.view(patients)

        patient_index = input('Please enter the patient ID: ')

        try:
            # patient_index is the patient ID mines one (-1)
            patient_index = int(patient_index) -1

            # check if the id is not in the list of patients
            if patient_index not in range(len(patients)):
                print('The id entered was not found.')
                return # stop the procedures

        except ValueError: # the entered id could not be changed into an int
            print('The id entered is incorrect')
            return # stop the procedures

        print("-----Doctors Select-----")
        print('Select the doctor that fits these symptoms:')
        patients[patient_index].print_symptoms() # print the patient symptoms

        print('--------------------------------------------------')
        print('ID |          Full Name           |  Speciality   ')
        self.view(doctors)
        doctor_index = input('Please enter the doctor ID: ')

        try:
            # doctor_index is the patient ID mines one (-1)
            doctor_index = int(doctor_index) -1

            # check if the id is in the list of doctors
            if self.find_index(doctor_index,doctors)!=False:
                    
                # link the patient to the doctor and vice versa
                patients[patient_index].link(doctors[doctor_index].full_name())
                doctors[doctor_index].add_patient(patients[patient_index])

                print('The patient is now assigned to the doctor.')

            # if the id is not in the list of doctors
            else:
                print('The id entered was not found.')

        except ValueError: # the entered id could not be changed into an in
            print('The id entered is incorrect')
        
        self.add_patient_file(patients)


    def discharge(self, patients, discharge_patients):
        """
        Allow the admin to discharge a patient when treatment is done
        Args:
            patients (list<Patients>): the list of all the active patients
            discharge_patients (list<Patients>): the list of all the non-active patients
        """
        print("-----Discharge Patient-----")

        while True:
            print('ID |        Full Name        |     Doctor`s Full Name     | Age |     Mobile     | Address |   Symptoms   ')
            self.view(patients)
            choice = input('Do you want to discharge a patient (Y/N): ').lower()
            if choice in ('no', 'n'):
                break
            if choice not in ('yes', 'y'):
                print('Please answer by yes or no.')
                continue
            patient_index = input('Please enter the patient ID: ')
            try:
                patient_index = int(patient_index) - 1
                if patient_index in range(len(patients)):
                    discharged_patient = patients.pop(patient_index)
                    discharge_patients.append(discharged_patient)
                    print('Patient discharged.')
                else:
                    print('The id entered was not found.')
            except ValueError:
                print('The id entered is incorrect.')

    def view_discharge(self, discharged_patients):
        """
        Prints the list of all discharged patients
        Args:
            discharge_patients (list<Patients>): the list of all the non-active patients
        """

        print("-----Discharged Patients-----")
        print('ID |        Full Name        |     Doctor`s Full Name     | Age |     Mobile     | Address |   Symptoms   ')
        self.view(discharged_patients)

    def update_details(self):
        """
        Allows the user to update and change username, password and address
        """

        print('Choose the field to be updated:')
        print(' 1 Username')
        print(' 2 Password')
        print(' 3 Address')
        try:
            op = int(input('Input: '))
        except ValueError:
            print('The input entered is incorrect.')
            return

        if op == 1:
            self.__username = input('Enter the new username: ')

        elif op == 2:
            password = input('Enter the new password: ')
            # validate the password
            if password == input('Enter the new password again: '):
                self.__password = password

        elif op == 3:
            self.__address = input('Enter the new address: ')

        else:
            print('Invalid option.')

    def relocate_doctor(self, doctors, patients):
        print('-----Relocate Doctor-----')
        print("-----Patients-----")
        print('ID |        Full Name        |     Doctor`s Full Name     | Age |     Mobile     | Address |   Symptoms   ')
        self.view(patients)

        try:
            patient_ind = int(input('Enter patient ID: ')) -1
            if patient_ind not in range(len(patients)):
                print('Patient not found.')
                return
        except ValueError:
            print('Invalid patiend ID.')
            return
        
        patient = patients[patient_ind]

        old_doctor = patient.get_doctor()
        print(f"\n Current Doctor: {old_doctor}")
        print('-----Doctors-----')
        print('ID |          Full Name           |  Speciality   ')
        self.view(doctors)

        try:
            new_doctor = int(input("Enter new doctor's ID: ")) -1
            if new_doctor not in range(len(doctors)):
                print("Doctor not found")
                return
        except ValueError:
            print("Invalid doctor ID")
            return
        
        n_doctor = doctors[new_doctor]
        
        if old_doctor != 'None':
            for doc in doctors:
                if doc.full_name() == old_doctor:
                    if patient in doc.get_patients():
                        doc.get_patients().remove(patient)
                    break
        
        patient.link(n_doctor.full_name())
        print('The doctor is relocated.')

        self.add_patient_file(patients)

    def add_symptom(self, patients):
        print("-----Add Symptoms-----")
        print('ID |        Full Name        |     Doctor`s Full Name     | Age |     Mobile     | Address |   Symptoms   ')
        self.view(patients)

        try:
            patient = int(input("Enter patient ID: ")) -1
            if patient not in range(len(patients)):
                print('Patient not found.')
                return
        except ValueError:
            print('Invalid patiend ID.')
            return
        
        pat = patients[patient]
        symptom = input('Enter the symptom: ')
        if symptom == "":
            print("Invalid input")
            return
        pat.add_symptoms(symptom)
        print("Symptom added successfully.")


if __name__ == '__main__':
    pass