import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime, timedelta
import pygame

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

def alarm():
    pygame.mixer.init()
    # Load alarm sound
    pygame.mixer.music.load("alarm.mp3")
    # Play the alarm sound in a loop
    pygame.mixer.music.play(loops=-1)
    
    # Activate the light
    light_label.config(bg='red')

    # Show the messagebox
    response = messagebox.askyesno("Medication Reminder", f"Time to take: {med['Name']} (Dosage: {med['Dosage']})\nDo you want to snooze?")

    if response:
        snooze()
    else:
        # Stop the alarm and deactivate the light when the user clicks "OK"
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        light_label.config(bg='white')
  
def snooze():
    # Stop the alarm and deactivate the light
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    light_label.config(bg='white')

    # Snooze for 5 minutes
    snooze_time = datetime.now() + timedelta(minutes=5)
    med['Next Dose'] = snooze_time.strftime('%Y-%m-%d %H:%M:%S')
    update_text_widget()

def update_clock():
    # Get the current time in HH:MM:SS format
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # parse current time to get only time and not date
    clock_label.config(text=current_datetime.split(' ')[1])  # Show only HH:MM:SS
    
    # Check if the current time matches any "Next Dose" in medications
    for med in medications:
        if 'Next Dose' in med and med['Next Dose'] == current_datetime:
            # Notify user about the medication
            alarm()
            update_doses(medications)
            update_text_widget()
            
    # Schedule the function to run again after 1 second
    clock_label.after(1000, update_clock)
    
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

def update_doses(medications):
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
# calculates the next dose based on the exact time that this funciton is called below
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
root.rowconfigure(3, weight=1)
root.columnconfigure(3, weight=1)

# Create a label to display the time
clock_label = tk.Label(root, font=('Arial', 48), fg='black')
clock_label.grid(row=0, column=0, rowspan=1, columnspan=3, sticky="nsew", padx=5, pady=5)

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
# Scrollbar to scroll through medications
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
text_widget.configure(yscrollcommand=scrollbar.set)

# Add a light label
light_label = tk.Label(root, text="Light", font=('Arial', 24), fg='black', bg='white')
light_label.grid(row=1, column=0, rowspan=1, columnspan=3, sticky="nsew", padx=5, pady=5)

# Start clock and run
update_clock()
root.mainloop()
