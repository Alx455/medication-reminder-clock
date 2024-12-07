from enum import Enum
from DB import get_db_connection
from mysql.connector import Error


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
        
    def add_patient(first_name, last_name, age, weight_kg):
        conn = None
        try:
            # Connect to the DB
            conn = get_db_connection()
            cursor = conn.cursor()

            # Insert patient data into DB
            cursor.execute("""
                INSERT INTO patients (first_name, last_name, age, weight_kg)
                VALUES (%s, %s, %s, %s)
            """, (first_name, last_name, age, weight_kg))

            # Commit
            conn.commit()
            print("Patient added successfully!")
        
        except Error as e:
            print(f"Database error: {e}")
        
        finally:
            # Safely close the connection if it was opened
            if conn.is_connected():
                conn.close()        
        

class Medication:
    def __init__(self, medication_id, patient_id, medication_name, dosage, frequency, frequency_unit, start_date, end_date, notes):
        self.medication_id = medication_id
        self.patient_id = patient_id
        self.medication_name = medication_name
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
            "medication_name": self.medication_name,
            "dosage": self.dosage,
            "frequency": self.frequency,
            "frequency_unit": self.frequency_unit,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "notes": self.notes
        }
        
    def add_medication(patient_id, medication_name, dosage, frequency, frequency_unit, start_date, end_date, notes):
        conn = None
        try:
            # Connect to DB
            conn = get_db_connection()
            cursor = conn.cursor()

            # Insert medication data into DB
            cursor.execute("""
                INSERT INTO medications (patient_id, medication_name, dosage, frequency, frequency_unit, start_date, end_date, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (patient_id, medication_name, dosage, frequency, frequency_unit, start_date, end_date, notes))
        
            # Commit
            conn.commit()
            print("Medication added successfully!")
    
        except Error as e:
            print(f"Database error: {e}")
        except ValueError as ve:
            print(f"Validation error: {ve}")
        finally:
            # Close connection
            if conn.is_connected():
                conn.close()

        
        
        
