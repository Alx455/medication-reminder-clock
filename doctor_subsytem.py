class Patient:
    def __init__(self, patient_id, name, contact):
        self.patient_id = patient_id
        self.name = name
        self.contact = contact

    def to_dict(self):
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "contact": self.contact
        }

class Medication:
    def __init__(self, medication_id, patient_id, name, dosage, frequency, start_date, end_date, notes):
        self.medication_id = medication_id
        self.patient_id = patient_id
        self.name = name
        self.dosage = dosage
        self.frequency = frequency
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
            "start_date": self.start_date,
            "end_date": self.end_date,
            "notes": self.notes
        }
