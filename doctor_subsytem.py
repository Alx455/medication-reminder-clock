
from enum import Enum
from DB import get_db_connection


class FrequencyUnit(Enum):
    DAYS = "days"
    HOURS = "hours"
    MINUTES = "minutes"


class Patient:
    def __init__(self, patient_id, first_name, last_name, age, weight_kg):
        self.patient_id = patient_id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.weight_kg = weight_kg
        

    def to_dict(self):
        return {
            "patient_id": self.patient_id,
            "first_name": self.first_name,
            "last_name:": self.last_name,
            "age": self.age,
            "weight_kg": self.weight_kg
        }

class Medication:
    def __init__(self, medication_id, patient_id, name, dosage, frequency, frequency_unit, start_date, end_date, notes):
        self.medication_id = medication_id
        self.patient_id = patient_id
        self.name = name
        self.dosage = dosage
        self.frequency = frequency
        if frequency_unit not in FrequencyUnit._value2member_map_:
            raise ValueError(f"Invalid frequency unit: {frequency_unit}")
        self.frequency_unit = frequency_unit
        self.start_date = start_date
        self.end_date = end_date
        self.notes = notes

    def to_dict(self):
        return {
            "medication_id": self.medication_id,
            "patient_id": self.patient_id,
            "name": self.name,
            "dosage": self.dosage,
            "frequency": self.frequency,
            "frequency_unit": self.frequency_unit,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "notes": self.notes
        }
        
        
        
        
def test_connection():
    try:
        conn = get_db_connection()
        if conn.is_connected():
            print("Connection to the database was successful!")
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
    finally:
        if conn.is_connected():
            conn.close()
            print("Database connection closed.")

test_connection()