from classes import Patient, Medication
import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# Window to add a new patient
def add_patient_screen():
    add_patient_window = tk.Toplevel(root)
    add_patient_window.title("Add New Patient")

    tk.Label(add_patient_window, text="First Name").grid(row=0, column=0, padx=10, pady=5)
    entry_first_name = tk.Entry(add_patient_window)
    entry_first_name.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(add_patient_window, text="Last Name").grid(row=1, column=0, padx=10, pady=5)
    entry_last_name = tk.Entry(add_patient_window)
    entry_last_name.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(add_patient_window, text="Age").grid(row=2, column=0, padx=10, pady=5)
    entry_age = tk.Entry(add_patient_window)
    entry_age.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(add_patient_window, text="Weight (kg)").grid(row=3, column=0, padx=10, pady=5)
    entry_weight = tk.Entry(add_patient_window)
    entry_weight.grid(row=3, column=1, padx=10, pady=5)

    # Function to save entered patient information into DB
    def save_patient():
        # Retrieve info from entry fields
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        age = entry_age.get()
        weight = entry_weight.get()

        # Check that all fields are populated
        if not all([first_name, last_name, age, weight]):
            messagebox.showerror("Error", "All fields are required.")
            return

        # Ensure age and weight are valid numbers
        try:
            age = int(age)
            weight = float(weight)
        except ValueError:
            messagebox.showerror("Error", "Age must be an integer and Weight must be a number.")
            return

        # Add patient to DB through Patient class
        try:
            Patient.add_patient(first_name, last_name, age, weight)
            messagebox.showinfo("Success", "Patient added successfully!")
            add_patient_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Button calls save patient function
    btn_save = tk.Button(add_patient_window, text="Save Patient", command=save_patient)
    btn_save.grid(row=4, column=0, columnspan=2, pady=10)

    # Button closes the add patient window
    btn_close = tk.Button(add_patient_window, text="Close", command=add_patient_window.destroy)
    btn_close.grid(row=5, column=0, columnspan=2, pady=5)


# Window to look through existing patients and to edit/add medications
def lookup_patient_screen():
    lookup_window = tk.Toplevel(root)
    lookup_window.title("Lookup Patient")
    
    lookup_window.grid_rowconfigure(0, weight=1)  # Allow the Treeview row to expand
    lookup_window.grid_rowconfigure(1, weight=0)  # Fixed size for buttons

    # Treeview for displaying the list of patients as a table
    tree = ttk.Treeview(lookup_window, columns=("ID", "First Name", "Last Name", "Age", "Weight"), show="headings")
    # sticky parameter sets table to stick to all edges of the cell, north edge(n), south edge(s), east edge(e) and west edge(w)
    tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    # Display the column names at the top of the table
    tree.heading("ID", text="ID")
    tree.heading("First Name", text="First Name")
    tree.heading("Last Name", text="Last Name")
    tree.heading("Age", text="Age")
    tree.heading("Weight", text="Weight (kg)")

    # Add a vertical scrollbar to the Treeview
    scrollbar = ttk.Scrollbar(lookup_window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=1, column=3, sticky="ns")

    # Edit and Medication buttons (disabled until row is selected)
    btn_edit = tk.Button(lookup_window, text="Edit", state=tk.DISABLED)
    btn_medication = tk.Button(lookup_window, text="Medication", state=tk.DISABLED)
    btn_export = tk.Button(lookup_window, text="Export", state=tk.DISABLED)

    # Function to enable buttons when a row is selected
    def on_tree_select(event):
        selected = tree.selection()
        if selected:
            btn_edit.config(state=tk.NORMAL)
            btn_medication.config(state=tk.NORMAL)
            btn_export.config(state=tk.NORMAL)
    
    # Bind event listener(slecting a row) to the function to enable buttons
    tree.bind("<<TreeviewSelect>>", on_tree_select)

    # Functions for button functionality below. Buttons will be defined after functions such that they can be bound to the functions

    # Populate the Treeview with all patients
    def populate_patient_list():
        try:
            # Get all patients from DB
            patients = Patient.get_all_patients()
            # Clear table of any current entries(important for refreshing info)
            for row in tree.get_children():
                tree.delete(row)
            # Populate table with most recent DB patients list
            for patient in patients:
                tree.insert("", "end", values=(patient.patient_id, patient.first_name, patient.last_name, patient.age, patient.weight_kg))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Edit Button Functionality
    def edit_patient_screen():
        # Ensure a selection is made
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "No patient selected.")
            return

        # item() is built in function that retrieved data from the item passed to it
        # slected[] array stores all rows selected from treeview
        item = tree.item(selected[0])
        patient_id, first_name, last_name, age, weight_kg = item["values"]

        # Open the editing window
        edit_window = tk.Toplevel(lookup_window)
        edit_window.title(f"Edit Patient - ID {patient_id}")

        # Labels and entry fields prepopulated with patient data
        tk.Label(edit_window, text="First Name").grid(row=0, column=0, padx=10, pady=5)
        entry_first_name = tk.Entry(edit_window)
        entry_first_name.insert(0, first_name)
        entry_first_name.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(edit_window, text="Last Name").grid(row=1, column=0, padx=10, pady=5)
        entry_last_name = tk.Entry(edit_window)
        entry_last_name.insert(0, last_name)
        entry_last_name.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(edit_window, text="Age").grid(row=2, column=0, padx=10, pady=5)
        entry_age = tk.Entry(edit_window)
        entry_age.insert(0, age)
        entry_age.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(edit_window, text="Weight (kg)").grid(row=3, column=0, padx=10, pady=5)
        entry_weight = tk.Entry(edit_window)
        entry_weight.insert(0, weight_kg)
        entry_weight.grid(row=3, column=1, padx=10, pady=5)

        # Function to save updated patient data
        def save_patient():
            # Get values from entry fields
            updated_first_name = entry_first_name.get()
            updated_last_name = entry_last_name.get()
            updated_age = entry_age.get()
            updated_weight_kg = entry_weight.get()

            # Ensure all fields are populated
            if not all([updated_first_name, updated_last_name, updated_age, updated_weight_kg]):
                messagebox.showerror("Error", "All fields are required.")
                return

            # Ensure age and weight are numeric values
            try:
                updated_age = int(updated_age)
                updated_weight_kg = float(updated_weight_kg)
            except ValueError:
                messagebox.showerror("Error", "Age must be an integer and Weight must be a number.")
                return

            try:
                # Update patient in the database
                Patient.update_patient(patient_id, updated_first_name, updated_last_name, updated_age, updated_weight_kg)
                # Show message box on successful update
                messagebox.showinfo("Success", "Patient updated successfully!")
                edit_window.destroy()
                # Refresh the Treeview
                populate_patient_list() 
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Save button
        btn_save = tk.Button(edit_window, text="Save Changes", command=save_patient)
        btn_save.grid(row=4, column=0, columnspan=2, pady=10)

        # Close button
        btn_close = tk.Button(edit_window, text="Close", command=edit_window.destroy)
        btn_close.grid(row=5, column=0, columnspan=2, pady=5)


    # Function for the medication screen
    def medication_screen():
        # Ensure a row is selected
        selected = tree.selection()
        if not selected:
            return

        # item() retrieves selected row's data
        # Selected row is stored in an array called selected[], thus why we acces it at selected[0]
        item = tree.item(selected[0])
        # retireve patient data from item array
        patient_id, first_name, last_name, age, weight = item["values"]

        # Open medication window
        med_window = tk.Toplevel(lookup_window)
        # Title medication window with patient name and ID
        med_window.title(f"Medications for {first_name} {last_name} (ID: {patient_id})")

        # Treeview for displaying medications
        med_tree = ttk.Treeview(med_window, columns=("Medication ID", "Name", "Dosage", "Frequency", "Frequency Unit", "Notes"), show="headings")
        # Stick table to all edges
        med_tree.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        # Display the column names at the top of the table
        med_tree.heading("Medication ID", text="Medication ID")
        med_tree.heading("Name", text="Name")
        med_tree.heading("Dosage", text="Dosage")
        med_tree.heading("Frequency", text="Frequency")
        med_tree.heading("Frequency Unit", text="Frequency Unit")
        med_tree.heading("Notes", text="Notes")
    
        # Functions for buttons and table population below

        # Function to populate medication table for the selected patient
        def populate_medications():
            try:
                # Retrieve all medications mathcing patient ID form DB
                medications = Medication.get_medications_by_patient_id(patient_id)
                # Clear tree to reload all medication(important for updates in medication)
                for row in med_tree.get_children():
                    med_tree.delete(row)
                # Populate tree with current medication values
                for med in medications:
                    med_tree.insert("", "end", values=(med.medication_id, med.medication_name, med.dosage, med.frequency, med.frequency_unit, med.notes))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Function to edit a medication
        def edit_medication():
            # Ensure a selection is made
            selected_med = med_tree.selection()
            if not selected_med:
                return

            # Get the selected medication's details
            item = med_tree.item(selected_med[0])
            med_id, name, dosage, frequency, frequency_unit, notes = item["values"]

            # Open window to edit medication
            edit_med_window = tk.Toplevel(med_window)
            edit_med_window.title(f"Edit Medication - ID {med_id}")

            # Labels and entry fields prepopulated with medication data
            tk.Label(edit_med_window, text="Medication Name").grid(row=0, column=0, padx=10, pady=5)
            entry_name = tk.Entry(edit_med_window)
            entry_name.insert(0, name)
            entry_name.grid(row=0, column=1, padx=10, pady=5)

            tk.Label(edit_med_window, text="Dosage").grid(row=1, column=0, padx=10, pady=5)
            entry_dosage = tk.Entry(edit_med_window)
            entry_dosage.insert(0, dosage)
            entry_dosage.grid(row=1, column=1, padx=10, pady=5)

            tk.Label(edit_med_window, text="Frequency").grid(row=2, column=0, padx=10, pady=5)
            entry_frequency = tk.Entry(edit_med_window)
            entry_frequency.insert(0, frequency)
            entry_frequency.grid(row=2, column=1, padx=10, pady=5)
            
            # Dropdown for Frequency Unit (defaulting to the current value)
            tk.Label(edit_med_window, text="Frequency Unit").grid(row=4, column=0, padx=10, pady=5)
            frequency_unit_combobox = ttk.Combobox(edit_med_window, values=["days", "hours", "minutes"], state="readonly")
            frequency_unit_combobox.grid(row=3, column=1, padx=10, pady=5)
            frequency_unit_combobox.set(frequency_unit)

            tk.Label(edit_med_window, text="Notes").grid(row=3, column=0, padx=10, pady=5)
            entry_notes = tk.Entry(edit_med_window)
            entry_notes.insert(0, notes)
            entry_notes.grid(row=4, column=1, padx=10, pady=5)

            # function to update the medication on the DB
            def save_edited_medication():
                # retrieve data from entry fields
                updated_name = entry_name.get()
                updated_dosage = entry_dosage.get()
                updated_frequency = entry_frequency.get()
                updated_frequency_unit = frequency_unit_combobox.get()
                updated_notes = entry_notes.get()

                # Ensure all fields populated
                if not all([updated_name, updated_dosage, updated_frequency, updated_frequency_unit]):
                    messagebox.showerror("Error", "All fields are required.")
                    return

                try:
                    Medication.update_medication(med_id, updated_name, updated_dosage, updated_frequency, updated_frequency_unit, updated_notes)
                    # Show a message box at successful update
                    messagebox.showinfo("Success", "Medication updated successfully!")
                    edit_med_window.destroy()
                    # Refresh the medication list
                    populate_medications()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

            # Save and close button
            btn_save = tk.Button(edit_med_window, text="Save Changes", command=save_edited_medication)
            btn_save.grid(row=5, column=0, columnspan=2, pady=10)

        # Function to delete a medication
        def delete_medication():
            selected_med = med_tree.selection()
            if not selected_med:
                return

            item = med_tree.item(selected_med[0])
            med_id = item["values"][0]

            # Built in tkinter's askyesno returns True if yes is clicked and False if No is clicked
            confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this medication?")
            if confirm:
                try:
                    Medication.delete_medication(med_id)
                    # Show a message box at successful deletion
                    messagebox.showinfo("Success", "Medication deleted successfully!")
                    # Refresh list
                    populate_medications()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                    
                    
        # Function to add new medication
        def add_medication():
            add_med_window = tk.Toplevel(med_window)
            add_med_window.title("Add Medication")

            # Empty fields to enter medication info
            tk.Label(add_med_window, text="Medication Name").grid(row=0, column=0, padx=10, pady=5)
            entry_name = tk.Entry(add_med_window)
            entry_name.grid(row=0, column=1, padx=10, pady=5)

            tk.Label(add_med_window, text="Dosage").grid(row=1, column=0, padx=10, pady=5)
            entry_dosage = tk.Entry(add_med_window)
            entry_dosage.grid(row=1, column=1, padx=10, pady=5)

            tk.Label(add_med_window, text="Frequency").grid(row=2, column=0, padx=10, pady=5)
            entry_frequency = tk.Entry(add_med_window)
            entry_frequency.grid(row=2, column=1, padx=10, pady=5)

            # Dropdown for Frequency Unit
            tk.Label(add_med_window, text="Frequency Unit").grid(row=3, column=0, padx=10, pady=5)
            frequency_unit_combobox = ttk.Combobox(add_med_window, values=["days", "hours", "minutes"], state="readonly")
            frequency_unit_combobox.grid(row=3, column=1, padx=10, pady=5)
            frequency_unit_combobox.set("days")  # Default selection

            tk.Label(add_med_window, text="Notes").grid(row=4, column=0, padx=10, pady=5)
            entry_notes = tk.Entry(add_med_window)
            entry_notes.grid(row=4, column=1, padx=10, pady=5)

            # Function to save medication to DB
            def save_medication():
                # Get values from fields
                name = entry_name.get()
                dosage = entry_dosage.get()
                frequency = entry_frequency.get()
                frequency_unit = frequency_unit_combobox.get()
                notes = entry_notes.get()

                # Ensure all fields populated
                if not all([name, dosage, frequency, frequency_unit]):
                    messagebox.showerror("Error", "Name, Dosage, Frequency, and Frequency Unit are required.")
                    return

                try:
                    Medication.add_medication(patient_id, name, dosage, frequency, frequency_unit, notes)
                    # Show a message box at successful deletion
                    messagebox.showinfo("Success", "Medication added successfully!")
                    add_med_window.destroy()
                    # Refresh medication list
                    populate_medications() 
                except Exception as e:
                    messagebox.showerror("Error", str(e))

            # Button to save medication
            btn_save = tk.Button(add_med_window, text="Save", command=save_medication)
            btn_save.grid(row=5, column=0, columnspan=2, pady=10)
     
           
        # Call function to populate table with medication
        populate_medications() 
            
        # Add, Edit and Delete buttons
        btn_add_med = tk.Button(med_window, text="Add Medication", command=add_medication)
        btn_add_med.grid(row=1, column=0, padx=5, pady=10)

        # Edit and delete are disabled by default(enabled only when row is selected)
        btn_edit_med = tk.Button(med_window, text="Edit Medication", state=tk.DISABLED, command=edit_medication)
        btn_edit_med.grid(row=1, column=1, padx=5, pady=10)

        btn_delete_med = tk.Button(med_window, text="Delete Medication", state=tk.DISABLED, command=delete_medication)
        btn_delete_med.grid(row=1, column=2, padx=5, pady=10)
                    
        # Function to enable buttons when row is selected
        def on_med_tree_select(event):
            selected_med = med_tree.selection()
            if selected_med:
                btn_edit_med.config(state=tk.NORMAL)
                btn_delete_med.config(state=tk.NORMAL)
            else:
                btn_edit_med.config(state=tk.DISABLED)
                btn_delete_med.config(state=tk.DISABLED)

        # Bind event listener(slecting a row) to the function to enable buttons
        med_tree.bind("<<TreeviewSelect>>", on_med_tree_select)

    def export():
        # Ensure a row is selected
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a patient to export data.")
            return

        # Get selected patient's details
        item = tree.item(selected[0])
        patient_id, first_name, last_name, age, weight = item["values"]

        try:
            # Fetch medications for the patient
            medications = Medication.get_medications_by_patient_id(patient_id)

            # Prepare data for JSON
            patient_data = {
                "Patient ID": patient_id,
                "First Name": first_name,
                "Last Name": last_name,
                "Age": age,
                "Weight (kg)": weight,
                "Medications": [
                    {
                        "Medication ID": med.medication_id,
                        "Name": med.medication_name,
                        "Dosage": med.dosage,
                        "Frequency": med.frequency,
                        "Frequency Unit": med.frequency_unit,
                        "Notes": med.notes,
                    }
                    for med in medications
                ],
            }

            # Define file name and save in current directory
            file_name = f"patient_{patient_id}_data.json"
            file_path = os.path.join(os.getcwd(), file_name)

            # Write data to JSON file
            with open(file_path, "w") as json_file:
                json.dump(patient_data, json_file, indent=4)

            messagebox.showinfo("Success", f"Patient data exported successfully to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while exporting data: {str(e)}")

    # call function to populate the table with all patients
    populate_patient_list()

    btn_edit.config(command=edit_patient_screen)
    btn_edit.grid(row=2, column=0, padx=0, pady=0)
    
    btn_medication.config(command=medication_screen)
    btn_medication.grid(row=2, column=1, padx=0, pady=0)
        
    btn_export.config(command=export)
    btn_export.grid(row=2, column=2, padx=0, pady=0)
    
    

    # Close button
    btn_close = tk.Button(lookup_window, text="Close", command=lookup_window.destroy)
    btn_close.grid(row=3, column=0, columnspan=3, pady=5)




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