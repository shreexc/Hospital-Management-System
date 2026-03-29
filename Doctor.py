class Doctor:
    """A class that deals with the Doctor operations"""

    def __init__(self, first_name, surname, speciality):
        """
        Args:
            first_name (string): First name
            surname (string): Surname
            speciality (string): Doctor`s speciality
        """

        self.__first_name = first_name
        self.__surname = surname
        self.__speciality = speciality
        self.__patients = []
        self.__appointments = []


    def full_name(self):
        """Returns full name (first name and surname of a doctor)."""
        return f'{self.__first_name} {self.__surname}'

    def get_first_name(self):
        """Returns the first name of the doctor."""
        return self.__first_name

    def set_first_name(self, new_first_name):
        """Updates the first name of the doctor."""
        self.__first_name = new_first_name

    def get_surname(self):
        """Returns the surname of the doctor."""
        return self.__surname

    def set_surname(self, new_surname):
        """Updates the surname of the doctor."""
        self.__surname = new_surname

    def get_speciality(self):
        """Returns the speciality of the doctor."""
        return self.__speciality

    def set_speciality(self, new_speciality):
        """Updates the speciality of the doctor."""
        self.__speciality = new_speciality

    def add_patient(self, patient):
        self.__patients.append(patient)
    
    def get_patients(self):
        return self.__patients
    
    def to_doc_files(self):
        return f"{self.get_first_name()}|{self.get_surname()}|{self.get_speciality()}"
    
    @staticmethod
    def from_doc_files(line):
        line = line.strip()
        if not line:
            return None
        
        sp = line.split('|')
        if len(sp) < 3:
            return None
        
        first_name = sp[0]
        surname = sp[1]
        speciality = sp[2]

        return Doctor(first_name, surname, speciality)

    def __str__(self) :
        return f'{self.full_name():^30}|{self.__speciality:^15}'
