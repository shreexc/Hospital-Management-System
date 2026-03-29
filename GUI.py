import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from Admin import Admin
from Patient import Patient
from Doctor import Doctor


class HMS_GUI:
    def __init__(self, root, admin):
        self.root = root
        self.root.title("Hospital Management System (HMS)")
        self.root.geometry("1100x650")
        self.root.resizable(False, False)

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.font_main = ("Segoe UI", 11)
        self.font_title = ("Segoe UI", 16, "bold")

        self.admin = admin
        self.doctors = []
        self.patients = []
        self.discharged_patients = []

        self.login_frame = ttk.Frame(self.root, padding=20)
        self.main_frame = ttk.Frame(self.root, padding=10)

        self.build_login_ui()
        self.login_frame.pack(fill="both", expand=True)

    def build_login_ui(self):
        for w in self.login_frame.winfo_children():
            w.destroy()

        title = ttk.Label(self.login_frame, text="Admin Login", font=self.font_title)
        title.pack(pady=20)

        form = ttk.Frame(self.login_frame)
        form.pack(pady=10)

        ttk.Label(form, text="Username:", font=self.font_main).grid(row=0, column=0, sticky="e", padx=10, pady=10)
        ttk.Label(form, text="Password:", font=self.font_main).grid(row=1, column=0, sticky="e", padx=10, pady=10)

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        user_entry = ttk.Entry(form, textvariable=self.username_var, font=self.font_main, width=25)
        pass_entry = ttk.Entry(form, textvariable=self.password_var, font=self.font_main, width=25, show="*")

        user_entry.grid(row=0, column=1, padx=10, pady=10)
        pass_entry.grid(row=1, column=1, padx=10, pady=10)

        btn = ttk.Button(self.login_frame, text="Login", command=self.try_login)
        btn.pack(pady=15)

        user_entry.focus()

    def try_login(self):
        u = self.username_var.get().strip()
        p = self.password_var.get().strip()

        if u == "" or p == "":
            messagebox.showerror("Error", "Please enter username and password.")
            return

        if u == self.admin._Admin__username and p == self.admin._Admin__password:
            self.login_frame.pack_forget()
            self.load_data()
            self.build_main_ui()
            self.main_frame.pack(fill="both", expand=True)
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")

    def load_data(self):
        try:
            self.doctors = self.admin.show_doctor("Doctor.txt")
        except Exception:
            self.doctors = []

        try:
            self.patients = self.admin.show_patient("Patient.txt")
        except Exception:
            self.patients = []

        self.discharged_patients = []

    def save_all(self):
        try:
            self.admin.save_doctor_file(self.doctors, "Doctor.txt")
        except Exception:
            pass
        try:
            self.admin.add_patient_file(self.patients, "Patient.txt")
        except Exception:
            pass

    def build_main_ui(self):
        for w in self.main_frame.winfo_children():
            w.destroy()

        header = ttk.Label(self.main_frame, text="Hospital Management System (HMS)", font=self.font_title)
        header.pack(pady=10)

        body = ttk.Frame(self.main_frame)
        body.pack(fill="both", expand=True)

        left = ttk.Frame(body)
        left.pack(side="left", fill="y", padx=10)

        right = ttk.Frame(body)
        right.pack(side="right", fill="both", expand=True, padx=10)

        ttk.Label(left, text="Choose the operation:", font=self.font_main).pack(pady=8)

        btns = [
            ("1 - Register/View/Update/Delete Doctor", self.gui_doctor_management),
            ("2 - Add/Delete Patients", self.gui_patient_add_delete),
            ("3 - View Patients", self.gui_view_patients),
            ("4 - View Patient's Family", self.gui_view_family),
            ("5 - Add Patient's Symptom", self.gui_add_symptom),
            ("6 - Discharge Patient", self.gui_discharge_patient),
            ("7 - View Discharged Patient", self.gui_view_discharged),
            ("8 - Assign/Relocate Doctor to a Patient", self.gui_assign_relocate),
            ("9 - Update Admin Details", self.gui_update_admin),
            ("10 - Quit", self.gui_quit),
        ]

        for text, cmd in btns:
            ttk.Button(left, text=text, command=cmd, width=35).pack(pady=5)

        ttk.Label(right, text="Output / List", font=self.font_main).pack(anchor="w")

        self.output = tk.Text(right, height=28, font=self.font_main, wrap="none")
        self.output.pack(fill="both", expand=True)

        self.refresh_output_patients()

    def clear_output(self):
        self.output.delete("1.0", tk.END)

    def refresh_output_patients(self):
        self.clear_output()
        self.output.insert(tk.END, "-----View Patients-----\n")
        self.output.insert(tk.END, "ID | Full Name | Doctor's Full Name | Age | Mobile | Address | Symptoms\n")
        self.output.insert(tk.END, "-" * 90 + "\n")

        if not self.patients:
            self.output.insert(tk.END, "No patients found.\n")
            return

        for i, p in enumerate(self.patients, start=1):
            symptoms = getattr(p, "_Patient__symptoms", [])
            self.output.insert(
                tk.END,
                f"{i:2} | {p.full_name():20} | {p.get_doctor():20} | {p.patient_age():3} | {p.mobile_number():12} | {p.patient_address():10} | {symptoms}\n"
            )

    def refresh_output_doctors(self):
        self.clear_output()
        self.output.insert(tk.END, "-----List of Doctors-----\n")
        self.output.insert(tk.END, "ID | Full Name | Speciality\n")
        self.output.insert(tk.END, "-" * 60 + "\n")

        if not self.doctors:
            self.output.insert(tk.END, "No doctors found.\n")
            return

        for i, d in enumerate(self.doctors, start=1):
            self.output.insert(tk.END, f"{i:2} | {d.full_name():20} | {d.get_speciality():15}\n")

    def gui_doctor_management(self):
        choice = simpledialog.askstring(
            "Doctor Management",
            "Choose:\n1 - Register\n2 - View\n3 - Update\n4 - Delete"
        )
        if not choice:
            return

        if choice == "1":
            fn = simpledialog.askstring("Register Doctor", "Enter first name:")
            sn = simpledialog.askstring("Register Doctor", "Enter surname:")
            sp = simpledialog.askstring("Register Doctor", "Enter speciality:")
            if not fn or not sn or not sp:
                messagebox.showerror("Error", "All fields required.")
                return

            for d in self.doctors:
                if d.get_first_name() == fn and d.get_surname() == sn:
                    messagebox.showerror("Error", "Doctor already exists.")
                    return

            self.doctors.append(Doctor(fn, sn, sp))
            self.save_all()
            messagebox.showinfo("Success", "Doctor registered.")
            self.refresh_output_doctors()

        elif choice == "2":
            self.refresh_output_doctors()

        elif choice == "3":
            if not self.doctors:
                messagebox.showerror("Error", "No doctors available.")
                return

            self.refresh_output_doctors()
            idx = simpledialog.askinteger("Update Doctor", "Enter doctor ID:")
            if idx is None or idx < 1 or idx > len(self.doctors):
                messagebox.showerror("Error", "Invalid ID.")
                return

            d = self.doctors[idx - 1]
            field = simpledialog.askstring("Update Doctor", "Update:\n1 - First name\n2 - Surname\n3 - Speciality")
            if not field:
                return

            if field == "1":
                new = simpledialog.askstring("Update", "Enter new first name:")
                if new:
                    d.set_first_name(new)
            elif field == "2":
                new = simpledialog.askstring("Update", "Enter new surname:")
                if new:
                    d.set_surname(new)
            elif field == "3":
                new = simpledialog.askstring("Update", "Enter new speciality:")
                if new:
                    d.set_speciality(new)
            else:
                messagebox.showerror("Error", "Invalid option.")
                return

            self.save_all()
            messagebox.showinfo("Success", "Doctor updated.")
            self.refresh_output_doctors()

        elif choice == "4":
            if not self.doctors:
                messagebox.showerror("Error", "No doctors available.")
                return

            self.refresh_output_doctors()
            idx = simpledialog.askinteger("Delete Doctor", "Enter doctor ID:")
            if idx is None or idx < 1 or idx > len(self.doctors):
                messagebox.showerror("Error", "Invalid ID.")
                return

            removed = self.doctors.pop(idx - 1)
            self.save_all()
            messagebox.showinfo("Deleted", f"Deleted: {removed.full_name()}")
            self.refresh_output_doctors()

        else:
            messagebox.showerror("Error", "Invalid option.")

    def gui_patient_add_delete(self):
        choice = simpledialog.askstring("Patients", "Choose:\n1 - Add Patient\n2 - Delete Patient")
        if not choice:
            return

        if choice == "1":
            fn = simpledialog.askstring("Add Patient", "Enter first name:")
            sn = simpledialog.askstring("Add Patient", "Enter surname:")
            age = simpledialog.askinteger("Add Patient", "Enter age:")
            mob = simpledialog.askstring("Add Patient", "Enter mobile:")
            addr = simpledialog.askstring("Add Patient", "Enter address:")
            if not fn or not sn or age is None or not mob or not addr:
                messagebox.showerror("Error", "All fields required.")
                return

            p = Patient(fn, sn, age, mob, addr)
            self.patients.append(p)
            self.save_all()
            messagebox.showinfo("Success", "Patient added.")
            self.refresh_output_patients()

        elif choice == "2":
            if not self.patients:
                messagebox.showerror("Error", "No patients available.")
                return

            self.refresh_output_patients()
            idx = simpledialog.askinteger("Delete Patient", "Enter patient ID:")
            if idx is None or idx < 1 or idx > len(self.patients):
                messagebox.showerror("Error", "Invalid ID.")
                return

            removed = self.patients.pop(idx - 1)
            self.save_all()
            messagebox.showinfo("Deleted", f"Deleted: {removed.full_name()}")
            self.refresh_output_patients()

        else:
            messagebox.showerror("Error", "Invalid option.")

    def gui_view_patients(self):
        self.refresh_output_patients()

    def gui_view_family(self):
        if not self.patients:
            messagebox.showerror("Error", "No patients available.")
            return

        surname = simpledialog.askstring("Patient Family", "Enter surname to view family:")
        if not surname:
            return

        family = [p for p in self.patients if p.surname().lower() == surname.lower()]

        self.clear_output()
        self.output.insert(tk.END, f"-----View patient's family: {surname}-----\n")
        self.output.insert(tk.END, "ID | Full Name | Doctor's Full Name | Age | Mobile | Address | Symptoms\n")
        self.output.insert(tk.END, "-" * 90 + "\n")

        if not family:
            self.output.insert(tk.END, "No family members found.\n")
            return

        for i, p in enumerate(family, start=1):
            symptoms = getattr(p, "_Patient__symptoms", [])
            self.output.insert(
                tk.END,
                f"{i:2} | {p.full_name():20} | {p.get_doctor():20} | {p.patient_age():3} | {p.mobile_number():12} | {p.patient_address():10} | {symptoms}\n"
            )

    def gui_add_symptom(self):
        if not self.patients:
            messagebox.showerror("Error", "No patients available.")
            return

        self.refresh_output_patients()
        idx = simpledialog.askinteger("Add Symptom", "Enter patient ID:")
        if idx is None or idx < 1 or idx > len(self.patients):
            messagebox.showerror("Error", "Invalid ID.")
            return

        symptom = simpledialog.askstring("Add Symptom", "Enter symptom:")
        if not symptom:
            return

        self.patients[idx - 1].add_symptoms(symptom)
        self.save_all()
        messagebox.showinfo("Success", "Symptom added.")
        self.refresh_output_patients()

    def gui_discharge_patient(self):
        if not self.patients:
            messagebox.showerror("Error", "No patients available.")
            return

        self.refresh_output_patients()
        idx = simpledialog.askinteger("Discharge Patient", "Enter patient ID to discharge:")
        if idx is None or idx < 1 or idx > len(self.patients):
            messagebox.showerror("Error", "Invalid ID.")
            return

        discharged = self.patients.pop(idx - 1)
        self.discharged_patients.append(discharged)
        self.save_all()
        messagebox.showinfo("Success", f"Discharged: {discharged.full_name()}")
        self.refresh_output_patients()

    def gui_view_discharged(self):
        self.clear_output()
        self.output.insert(tk.END, "-----Discharged Patients-----\n")
        self.output.insert(tk.END, "ID | Full Name | Doctor's Full Name | Age | Mobile | Address | Symptoms\n")
        self.output.insert(tk.END, "-" * 90 + "\n")

        if not self.discharged_patients:
            self.output.insert(tk.END, "No discharged patients.\n")
            return

        for i, p in enumerate(self.discharged_patients, start=1):
            symptoms = getattr(p, "_Patient__symptoms", [])
            self.output.insert(
                tk.END,
                f"{i:2} | {p.full_name():20} | {p.get_doctor():20} | {p.patient_age():3} | {p.mobile_number():12} | {p.patient_address():10} | {symptoms}\n"
            )

    def gui_assign_relocate(self):
        choice = simpledialog.askstring("Assign/Relocate", "Choose:\n1 - Assign doctor\n2 - Relocate doctor")
        if not choice:
            return

        if not self.patients:
            messagebox.showerror("Error", "No patients available.")
            return

        if not self.doctors:
            messagebox.showerror("Error", "No doctors available.")
            return

        self.refresh_output_patients()
        pid = simpledialog.askinteger("Patient", "Enter patient ID:")
        if pid is None or pid < 1 or pid > len(self.patients):
            messagebox.showerror("Error", "Invalid patient ID.")
            return

        self.refresh_output_doctors()
        did = simpledialog.askinteger("Doctor", "Enter doctor ID:")
        if did is None or did < 1 or did > len(self.doctors):
            messagebox.showerror("Error", "Invalid doctor ID.")
            return

        patient = self.patients[pid - 1]
        doctor = self.doctors[did - 1]

        if choice == "1":
            patient.link(doctor.full_name())
            doctor.add_patient(patient)
            self.save_all()
            messagebox.showinfo("Success", "Doctor assigned.")
            self.refresh_output_patients()

        elif choice == "2":
            old = patient.get_doctor()
            if old != "None":
                for d in self.doctors:
                    if d.full_name() == old:
                        if patient in d.get_patients():
                            d.get_patients().remove(patient)
                        break
            patient.link(doctor.full_name())
            doctor.add_patient(patient)
            self.save_all()
            messagebox.showinfo("Success", "Doctor relocated.")
            self.refresh_output_patients()

        else:
            messagebox.showerror("Error", "Invalid option.")

    def gui_update_admin(self):
        choice = simpledialog.askstring("Update Admin", "Update:\n1 - Username\n2 - Password\n3 - Address")
        if not choice:
            return

        if choice == "1":
            new_u = simpledialog.askstring("Update Username", "Enter new username:")
            if new_u:
                self.admin._Admin__username = new_u
                messagebox.showinfo("Success", "Username updated.")
        elif choice == "2":
            new_p = simpledialog.askstring("Update Password", "Enter new password:")
            if new_p:
                self.admin._Admin__password = new_p
                messagebox.showinfo("Success", "Password updated.")
        elif choice == "3":
            new_a = simpledialog.askstring("Update Address", "Enter new address:")
            if new_a:
                self.admin._Admin__address = new_a
                messagebox.showinfo("Success", "Address updated.")
        else:
            messagebox.showerror("Error", "Invalid option.")

    def gui_quit(self):
        self.root.destroy()
