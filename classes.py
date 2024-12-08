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
            if conn and conn.is_connected():
                conn.close()  
                
    def get_all_patients():
        conn = None
        try:
            # Connect to DB
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Get all patients
            cursor.execute("SELECT * FROM patients")
            patients = cursor.fetchall()

            # Convert to Patient objects
            patient_list = [
                Patient(
                    patient_id=row["patient_id"],
                    first_name=row["first_name"],
                    last_name=row["last_name"],
                    age=row["age"],
                    weight_kg=row["weight_kg"]
                ) for row in patients
            ]
            return patient_list
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            if conn and conn.is_connected():
                conn.close()

    def get_patient_by_id(patient_id):
        conn = None
        try:
            # Connect to DB
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Get the patient by ID
            cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
            row = cursor.fetchone()

            if row:
                # Convert to a Patient object
                return Patient(
                    patient_id=row["patient_id"],
                    first_name=row["first_name"],
                    last_name=row["last_name"],
                    age=row["age"],
                    weight_kg=row["weight_kg"]
                )
            else:
                print(f"No patient found with ID {patient_id}.")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            if conn and conn.is_connected():
                conn.close()
                
    def update_patient(patient_id, first_name, last_name, age, weight_kg):
        try:
            # Connect to DB
            conn = get_db_connection()
            cursor = conn.cursor()
        
            cursor.execute("""
                UPDATE patients
                SET first_name = %s, last_name = %s, age = %s, weight_kg = %s
                WHERE patient_id = %s
            """, (first_name, last_name, age, weight_kg, patient_id))
            conn.commit()
            print(f"Patient ID {patient_id} updated successfully!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if conn and conn.is_connected():
                conn.close()    
        

class Medication:
    def __init__(self, medication_id, patient_id, medication_name, dosage, frequency, frequency_unit, notes):
        self.medication_id = medication_id
        self.patient_id = patient_id
        self.medication_name = medication_name
        self.dosage = dosage
        self.frequency = frequency
        if frequency_unit not in FrequencyUnit._value2member_map_:
            raise ValueError(f"Invalid frequency unit: {frequency_unit}")
        self.frequency_unit = frequency_unit
        self.notes = notes

    def to_dict(self):
        return {
            "medication_id": self.medication_id,
            "patient_id": self.patient_id,
            "medication_name": self.medication_name,
            "dosage": self.dosage,
            "frequency": self.frequency,
            "frequency_unit": self.frequency_unit,
            "notes": self.notes
        }
        
    def add_medication(patient_id, medication_name, dosage, frequency, frequency_unit, notes):
        try:
            # Connect to DB
            conn = get_db_connection()
            cursor = conn.cursor()

            # Insert medication data into DB
            cursor.execute("""
                INSERT INTO medications (patient_id, medication_name, dosage, frequency, frequency_unit, notes)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (patient_id, medication_name, dosage, frequency, frequency_unit, notes))
        
            # Commit
            conn.commit()
            print("Medication added successfully!")
    
        except Error as e:
            print(f"Database error: {e}")
        except ValueError as ve:
            print(f"Validation error: {ve}")
        finally:
            # Close connection
            if conn and conn.is_connected():
                conn.close()
                
    def update_medication(medication_id, name, dosage, frequency, frequency_unit, notes):
        try:
            # Connect to DB
            conn = get_db_connection()
            cursor = conn.cursor()

            # Update the medication record in DB
            cursor.execute("""
                UPDATE medications
                SET medication_name = %s,
                    dosage = %s,
                    frequency = %s,
                    frequency_unit = %s,
                    notes = %s
                WHERE medication_id = %s
            """, (name, dosage, frequency, frequency_unit, notes, medication_id))

            # Commit
            conn.commit()

            print("Medication updated successfully!")

        except Exception as e:
            print(f"Error updating medication: {e}")

        finally:
            # Close connection
            if conn and conn.is_connected():
                conn.close()
                
    @staticmethod
    def delete_medication(medication_id):
        try:
            # Connect to DB
            conn = get_db_connection()
            cursor = conn.cursor()

            # Delete the medication record from DB
            cursor.execute("DELETE FROM medications WHERE medication_id = %s", (medication_id,))

            # Commit
            conn.commit()

            print("Medication deleted successfully!")

        except Exception as e:
            print(f"Error deleting medication: {e}")

        finally:
            # Close connection
            if conn and conn.is_connected():
                conn.close()


    def get_medications_by_patient_id(patient_id):
        """Fetch all medications for a given patient ID."""
        conn = None
        try:
            # Connect to DB
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Execute the query to fetch medications by patient ID
            cursor.execute("""
                SELECT medication_id, medication_name, dosage, frequency, frequency_unit, notes
                FROM medications
                WHERE patient_id = %s
            """, (patient_id,))
            medications = cursor.fetchall()

            # Convert each record into a Medication object
            medication_list = [
                Medication(
                    med["medication_id"],
                    patient_id,
                    med["medication_name"],
                    med["dosage"],
                    med["frequency"],
                    med["frequency_unit"],
                    med["notes"]
                )
                for med in medications
            ]

            return medication_list

        except Exception as e:
            print(f"Database error: {e}")
            return []
        finally:
            if conn and conn.is_connected():
                conn.close()
