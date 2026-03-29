class Patient:
    """Patient class"""

    def __init__(self, first_name, surname, age, mobile, address):
        """
        Args:
            first_name (string): First name
            surname (string): Surname
            age (int): Age
            mobile (string): the mobile number
            address (string): address
        """
        self.__first_name = first_name
        self.__surname = surname
        self.__age = age
        self.__mobile = mobile
        self.__address = address
        self.__doctor = 'None'
        self.__symptoms = []

    def full_name(self):
        """Returns full name (first name and surname of a patient)."""
        return f'{self.__first_name} {self.__surname}'
    
    def surname(self): # for family by surname
        return self.__surname
    
    def patient_age(self):
        return f'{self.__age}'
    
    def mobile_number(self):
        return f'{self.__mobile}'
    
    def patient_address(self):
        return f'{self.__address}'

    def get_doctor(self):
        """Returns the doctor of the patient."""
        return self.__doctor

    def link(self, doctor):
        """Args: doctor(string): the doctor full name"""
        self.__doctor = doctor

    def print_symptoms(self):
        """Prints all the symptoms of the patient."""
        if not self.__symptoms:
            print('No symptoms recorded.')
        else:
            for symptom in self.__symptoms:
                print(f'  - {symptom}')

    def add_symptoms(self, symptom):
        self.__symptoms.append(symptom)

    def to_files(self):
        symptoms_text = ",".join(self.__symptoms)
        return f"{self.__first_name}|{self.__surname}|{self.__age}|{self.__mobile}|{self.__address}|{self.__doctor}|{symptoms_text}"

    @staticmethod
    def from_files(line):
        parts = line.strip().split("|")

        first_name = parts[0]
        surname = parts[1]
        age = int(parts[2])
        mobile = parts[3]
        address = parts[4]
        doctor = parts[5]
        symptoms_text = parts[6] if len(parts) > 6 else ""

        p = Patient(first_name, surname, age, mobile, address)
        p.link(doctor)

        if symptoms_text != "":
            for s in symptoms_text.split(","):
                if s.strip() != "":
                    p.add_symptoms(s.strip())

        return p

    def __str__(self):
        symptoms_text = ", ".join(self.__symptoms) if self.__symptoms else "[]"
        return (f"{self.full_name():<20} | " f"{str(self.__doctor):<20} | "
                f"{self.__age:<7} | " f"{self.__mobile:<11} | "
                f"{self.__address:<8} | " f"{symptoms_text:<12}")