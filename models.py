from sqlalchemy import Column, String, Integer, DateTime, create_engine
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Hospital(db.Model):
    __tablename__ = 'hospital'

    hospital_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    phone = Column(String, nullable=False)
    start_year = Column(DateTime, nullable=False)

    def format(self):
        return {
            'id': self.hospital_id,
            'name': self.name,
            'description': self.description,
            'phone': self.phone,
            'start_year': self.start_year
        }

    def get_hospital_detail(self):
        return {
            'id': self.hospital_id,
            'name': self.name,
            'description': self.description,
            'phone': self.phone,
            'start_year': self.start_year,
            'doctors': [dh.get_doctor() for dh in DoctorHospital.query.filter(
                DoctorHospital.hospital_id == self.hospital_id).all()]
        }



class Doctors(db.Model):
    __tablename__ = 'doctors'

    doctor_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    categories = Column(db.ARRAY(String), nullable=False)
    languages = Column(db.ARRAY(String), nullable=False)
    experience = Column(Integer, nullable=False)

    def format(self):
        return {
            'id': self.doctor_id,
            'name': self.first_name+' '+self.last_name,
            'categories': ''.join(self.categories),
            'languages': ''.join(self.languages),
            'experience': self.experience
        }


class DoctorHospital(db.Model):
    __tablename__ = 'doctor_hospital'

    doctor_hospital_id = Column(Integer, primary_key=True)
    hospital_id = Column(Integer, db.ForeignKey('hospital.hospital_id'), nullable=False)
    doctor_id = Column(String, db.ForeignKey('doctors.doctor_id'), nullable=False)
    start_date = Column(db.DateTime(), nullable=False)
    hospital = db.relationship('Hospital', backref=db.backref('hospital_doctor'))
    doctor = db.relationship('Doctors', backref=db.backref('doctor_hospital'))

    def format(self):
        return {
            'hospital_id': self.hospital_id,
            'hospital_name': self.hospital.name,
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor.first_name+' '+self.doctor.last_name,
            'start_date':self.start_date
        }

    def get_doctor(self):
        return {
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor.first_name+' '+self.doctor.last_name,
            'start_date':self.start_date
        }

