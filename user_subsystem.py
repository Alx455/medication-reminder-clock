from classes import Patient, Medication
import tkinter as tk
from tkinter import messagebox, ttk
import json
import os


def read_patient_data(json_file):
    try:
        # Open and load the JSON file
        with open(json_file, 'r') as file:
            data = json.load(file)

        # Extract the Medications array from the JSON
        medications = data.get("Medications", [])
        
        # Print or return the medications array
        return medications

    except FileNotFoundError:
        print(f"Error: The file {json_file} does not exist.")
        return []
    except json.JSONDecodeError:
        print(f"Error: The file {json_file} is not a valid JSON.")
        return []
    
    
medications = read_patient_data("patient_data.json")
print("Medications:", medications)