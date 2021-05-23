from sqlalchemy import Column, String, Integer, DateTime, create_engine
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI, DEBUG
import json
import os

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
            'categories': self.categories,
            'languages': self.languages,
            'experience': self.experience
        }