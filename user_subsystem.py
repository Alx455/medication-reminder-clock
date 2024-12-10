import tkinter as tk
from tkinter import messagebox, ttk
import json
from time import strftime
from datetime import datetime, timedelta
import pygame



# Function to read patient_data from JSON file into an array that will store all medications for the patient
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
  
  
# Play alarm audio until user clicks OK on popup message
def alarm():
    pygame.mixer.init()
    # Load alarm sound
    pygame.mixer.music.load("alarm.mp3")
    # Play the alarm sound in a loop
    pygame.mixer.music.play(loops=-1)
    
  
  
def stop_alarm():
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    # Hide the alarm button
    alarm_button.config(state="disabled")
    
    
def update_clock():
    # Get the current date and time
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # parse current datetime to get only time in HH:MM:SS format
    clock_label.config(text=current_datetime.split(' ')[1])
    # Check Next Dose any medication matches the current date and time(medication needs to be taken)
    for med in medications:
        # Ring alarm if medication needs to be taken
        if 'Next Dose' in med and med['Next Dose'] == current_datetime:
            alarm()
            # Update Next Dose of the medication whose alarm rang
            update_next_doses(medications)
            # Update the display of medications to show new Next Dose
            update_text_widget()     
    # Schedule the function to run again after 1 second
    clock_label.after(1000, update_clock)
    
    
# Function to set the Next Dose of all medications when a user first opens the app
def initialize_doses(medications):
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
    
def update_next_doses(medications):
    # Empty array to be returned in order to prevent duplicate data
    updated_medications = []   
    for med in medications:
        try:
            # Get medication frequency and the unit of time
            frequency = med['Frequency']
            unit = med['Frequency Unit']         
            # Get the current date and time
            current_time = datetime.now()         
            if 'Next Dose' in med and med['Next Dose']:
                next_dose_time = datetime.strptime(med['Next Dose'], '%Y-%m-%d %H:%M:%S')
                
                # Update the 'Next Dose' only if it's in the past
                if next_dose_time <= current_time:
                    if unit == 'days':
                        next_time = current_time + timedelta(days=frequency)
                    elif unit == 'hours':
                        next_time = current_time + timedelta(hours=frequency)
                    elif unit == 'minutes':
                        next_time = current_time + timedelta(minutes=frequency)
                    else:
                        raise ValueError(f"Invalid frequency unit: {unit}")
                    
                    med['Next Dose'] = next_time.strftime('%Y-%m-%d %H:%M:%S')           
            # Add to the updated list
            updated_medications.append(med)   
        except KeyError as e:
            print(f"Missing key in medication: {e}")
        except Exception as e:
            print(f"Error processing medication: {e}")
    return updated_medications
 
def update_text_widget():
    text_widget.configure(state="normal")
    # Clear all existing text
    text_widget.delete("1.0", "end")
    for med in medications:
        med_details = (
            f"Medication: {med['Name']}\n"
            f"Dosage: {med['Dosage']}\n"
            f"Frequency: {med['Frequency']} {med['Frequency Unit']}\n"
            f"Next Dose: {med['Next Dose']} \n\n\n"
        )
        text_widget.insert("end", med_details)
    text_widget.configure(state="disabled")   
    


medications = read_patient_data("patient_data.json")
# File does not initially have a next dose fields, the first call of this function
# calculates the next dose based on the exact time that the app is first opened
medications = initialize_doses(medications)


# Create the main window
root = tk.Tk()
root.title("Medication Clock")

root.rowconfigure(0, weight=2)
root.columnconfigure(0, weight=2)
root.rowconfigure(1, weight=2)
root.columnconfigure(1, weight=2)
root.rowconfigure(2, weight=2)
root.columnconfigure(2, weight=2)
root.rowconfigure(3, weight=1)
root.columnconfigure(3, weight=1)
root.columnconfigure(4, weight=1)

# Create a label to display the clock
clock_label = tk.Label(root, font=('Arial', 48), fg='black')
clock_label.grid(row=0, column=0, rowspan=1, columnspan=3, sticky="nsew", padx=5, pady=5)


# Create a frame to place the medications list text field
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
# Scrollbar to scroll through medicaitons
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
text_widget.configure(yscrollcommand=scrollbar.set)

alarm_button = tk.Button(
    root,
    text="Pill\nCompartment",
    font=('Arial', 14),
    fg='white',
    bg='red',
    command=stop_alarm,
    width=6,
    height=3,
)
alarm_button.grid(row=2, column=2, padx=10, pady=10, sticky="ns")

root.minsize(900, 300)


# Start clock and run
update_clock()
root.mainloop()