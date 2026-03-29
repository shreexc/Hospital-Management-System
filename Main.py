# Imports
from Admin import Admin
from Doctor import Doctor
from Patient import Patient
import tkinter as tk
from GUI import HMS_GUI

def main():
    """
    the main function to be ran when the program runs
    """

    # Initialising the actors
    admin = Admin('admin','123','B1 1AB') # username is 'admin', password is '123'
    doctors = admin.show_doctor()
    patients = admin.show_patient()
    discharged_patients = []

    root = tk.Tk()
    app = HMS_GUI(root, admin)
    root.mainloop()

    # keep trying to login tell the login details are correct
    while True:
        if admin.login():
            running = True # allow the program to run
            break
        else:
            print('Incorrect username or password.')

    while running:
        # print the menu
        print('Choose the operation:')
        print(' 1- Register/view/update/delete doctor')
        print(' 2- Add/delete patients')
        print(' 3- View patients')
        print(" 4- View patient's family")
        print(" 5- Add patient's symptom")
        print(" 6- Discharge patient")
        print(' 7- View discharged patient')
        print(' 8- Assign/Relocate doctor to a patient')
        print(' 9- Update admin details')
        print(' 10- Quit')

        # get the option
        op = input('Option: ')

        if op == '1':
            # 1- Register/view/update/delete doctor
            admin.doctor_management(doctors)
        
        elif op == '2':
            admin.add_del_patient(patients)
        
        elif op == '3':
            admin.view_patient(patients)

        elif op == '4':
            admin.patient_family(patients)

        elif op == '5':
            admin.add_symptom(patients)

        elif op == '6':
            # 2- View or discharge patients
            admin.discharge(patients, discharged_patients)

        elif op == '7':
            # 3 - view discharged patients
            admin.view_discharge(discharged_patients)

        elif op == '8':
            # 4- Assign doctor to a patient
            admin.assign_relocate(patients, doctors)

        elif op == '9':
            # 5- Update admin detais
            admin.update_details()

        elif op == '10':
            # 6 - Quit
            print('Goodbye.')
            break

        else:
            # the user did not enter an option that exists in the menu
            print('Invalid option. Try again')

if __name__ == '__main__':
    main()