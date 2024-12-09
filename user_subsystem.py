from classes import Patient, Medication
import tkinter as tk
from tkinter import messagebox, ttk
import json
from time import strftime
from datetime import datetime, timedelta



def read_patient_data(json_file):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
        # Get medications from file, default to empty list if no medications exist
        medications = data.get("Medications", [])
        return medications
    except FileNotFoundError:
        print(f"Error: The file {json_file} does not exist.")
        return []
    except json.JSONDecodeError:
        print(f"Error: The file {json_file} is not a valid JSON.")
        return []
    
def update_clock():
    # Get the current time in HH:MM:SS format
    current_time = strftime('%H:%M:%S')
    # Update label
    clock_label.config(text=current_time)
    
    # Schedule the function to run again after 1 second
    clock_label.after(1000, update_clock)
    
def update_next_dose(medications):
    # Empty array to be returned in order to prevent duplicate data
    updated_medications = []
    
    for med in medications:
        try:
            # Get medication frequency and the unit of time
            frequency = med['Frequency']
            unit = med['Frequency Unit']
            
            # Get the current date and time
            current_time = datetime.now()
            
            # Calculate the next date and time based on unit of frequency
            if unit == 'days':
                next_time = current_time + timedelta(days=frequency)
            elif unit == 'hours':
                next_time = current_time + timedelta(hours=frequency)
            elif unit == 'minutes':
                next_time = current_time + timedelta(minutes=frequency)
            else:
                raise ValueError(f"Invalid frequency unit: {unit}")
            
            # Add the next time to the medication dictionary
            med['Next Dose'] = next_time.strftime('%Y-%m-%d %H:%M:%S')
            
            # Add to the updated list
            updated_medications.append(med)
        
        except KeyError as e:
            print(f"Missing key in medication: {e}")
        except Exception as e:
            print(f"Error processing medication: {e}")
    
    return updated_medications
    
    
    
    


medications = read_patient_data("patient_data.json")
medications = update_next_dose(medications)


# Create the main window
root = tk.Tk()
root.title("Medication Clock")

root.rowconfigure(0, weight=2)
root.columnconfigure(0, weight=2)
root.rowconfigure(1, weight=2)
root.columnconfigure(1, weight=2)
root.rowconfigure(2, weight=1)
root.columnconfigure(2, weight=1)
root.rowconfigure(3, weight=1)
root.columnconfigure(3, weight=1)

# Create a label to display the time
clock_label = tk.Label(root, font=('Arial', 48), fg='black')
clock_label.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="nsew", padx=5, pady=5)




frame = tk.Frame(root)
frame.grid(row=2, column=0, rowspan=1, columnspan=1, sticky="nsew", padx=10, pady=10)

# Configure the frame's grid
frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)

# Add a Text widget with a scrollbar that contains all medication
text_widget = tk.Text(frame, wrap="word", height=6)
text_widget.grid(row=0, column=0, sticky="nsew")
for med in medications:
    med_details = (
        f"Medication: {med['Name']}\n"
        f"Dosage: {med['Dosage']}\n"
        f"Frequency: {med['Frequency']} {med['Frequency Unit']}\n"
        f"Next Dose: {med['Next Dose']} \n\n\n"
    )
    text_widget.insert("end", med_details)
text_widget.configure(state="disabled")


scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
text_widget.configure(yscrollcommand=scrollbar.set)





# Start clock and run
update_clock()
root.mainloop()