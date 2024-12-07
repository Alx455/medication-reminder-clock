from classes import Patient, Medication
import tkinter as tk
from tkinter import messagebox

def add_patient_screen():
    """Open the 'Add Patient' screen."""
    add_window = tk.Toplevel(root)
    add_window.title("Add New Patient")

    tk.Label(add_window, text="First Name").grid(row=0, column=0, padx=10, pady=5)
    entry_first_name = tk.Entry(add_window)
    entry_first_name.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Last Name").grid(row=1, column=0, padx=10, pady=5)
    entry_last_name = tk.Entry(add_window)
    entry_last_name.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Age").grid(row=2, column=0, padx=10, pady=5)
    entry_age = tk.Entry(add_window)
    entry_age.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Weight (kg)").grid(row=3, column=0, padx=10, pady=5)
    entry_weight = tk.Entry(add_window)
    entry_weight.grid(row=3, column=1, padx=10, pady=5)

    def save_patient():
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        age = entry_age.get()
        weight = entry_weight.get()

        if not all([first_name, last_name, age, weight]):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            age = int(age)
            weight = float(weight)
        except ValueError:
            messagebox.showerror("Error", "Age must be an integer and Weight must be a number.")
            return

        try:
            Patient.add_patient(first_name, last_name, age, weight)  # Call the add_patient method
            messagebox.showinfo("Success", "Patient added successfully!")
            add_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    btn_save = tk.Button(add_window, text="Save Patient", command=save_patient)
    btn_save.grid(row=4, column=0, columnspan=2, pady=10)

    btn_close = tk.Button(add_window, text="Close", command=add_window.destroy)
    btn_close.grid(row=5, column=0, columnspan=2, pady=5)


def lookup_patient_screen():
    """Open the 'Lookup Patient' screen."""
    lookup_window = tk.Toplevel(root)
    lookup_window.title("Lookup Patient by ID")

    tk.Label(lookup_window, text="Enter Patient ID").grid(row=0, column=0, padx=10, pady=5)
    entry_patient_id = tk.Entry(lookup_window)
    entry_patient_id.grid(row=0, column=1, padx=10, pady=5)

    def lookup_patient():
        patient_id = entry_patient_id.get()
        if not patient_id:
            messagebox.showerror("Error", "Please enter a Patient ID.")
            return

        try:
            patient_id = int(patient_id)
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
            patient = cursor.fetchone()
            conn.close()

            if patient:
                details = (
                    f"Patient ID: {patient['patient_id']}\n"
                    f"First Name: {patient['first_name']}\n"
                    f"Last Name: {patient['last_name']}\n"
                    f"Age: {patient['age']}\n"
                    f"Weight: {patient['weight_kg']} kg"
                )
                messagebox.showinfo("Patient Details", details)
            else:
                messagebox.showinfo("Not Found", f"No patient found with ID {patient_id}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    btn_lookup = tk.Button(lookup_window, text="Lookup", command=lookup_patient)
    btn_lookup.grid(row=1, column=0, columnspan=2, pady=10)

    btn_close = tk.Button(lookup_window, text="Close", command=lookup_window.destroy)
    btn_close.grid(row=2, column=0, columnspan=2, pady=5)


# Main Screen
root = tk.Tk()
root.title("Patient Management System")

tk.Label(root, text="Welcome to the Patient Management System", font=("Arial", 16)).pack(pady=20)

btn_add_patient = tk.Button(root, text="Add a Patient", width=20, command=add_patient_screen)
btn_add_patient.pack(pady=10)

btn_lookup_patient = tk.Button(root, text="Lookup Patient by ID", width=20, command=lookup_patient_screen)
btn_lookup_patient.pack(pady=10)

btn_exit = tk.Button(root, text="Exit", width=20, command=root.quit)
btn_exit.pack(pady=20)

root.mainloop()