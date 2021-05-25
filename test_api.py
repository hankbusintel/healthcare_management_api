import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, Customer, Admin
from app import create_app
from models import db, Doctors, Hospital, DoctorHospital


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
    db.app = app
    db.init_app(app)
    db.create_all()


class HealthcareTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)
        self.customer = {"Authorization": "Bearer {}".format(Customer)}
        self.admin = {"Authorization": "Bearer {}".format(Admin)}
        self.create = {
            "first_name": "Happy",
            "last_name": "Monday",
            "categories": ["sleep","medicine"],
            "experience": 7,
            "languages": ["English","Spanish"]
        }
        self.patch = {
            "first_name": "Jack",
            "last_name": "R",
            "categories": ["sleep","medicine"],
            "experience": 4,
            "languages": ["English","Spanish"]
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            #self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_doctors(self):
        res = self.client().get('/doctors')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['doctors']))

    def test_error_all_doctors(self):
        res = self.client().get('/doctors?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_all_hospital(self):
        res = self.client().get('/hospital')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['hospital']))

    def test_error_all_hospital(self):
        res = self.client().get('/hospital?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_auth_error_hospital_detail(self):
        res = self.client().get('/hospital-detail')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header not found')

    def test_hospital_detail(self):
        res = self.client().get('/hospital-detail', headers=self.customer)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['hospital-detail']))
    
    def test_error_pagination_hospital_detail(self):
        res = self.client().get('/hospital-detail?page=2', headers=self.customer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_auth_error_delete_doctor(self):
        res = self.client().delete('/doctors/19', headers=self.customer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

        res = self.client().delete('/doctors/19')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header not found')

    def test_not_found_delete_doctor(self):
        res = self.client().delete('/doctors/2', headers=self.admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    




    def test_auth_error_create_doctor(self):
        res = self.client().post('/doctors', json=self.create)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header not found')

        res = self.client().post('/doctors', headers=self.customer, json=self.create)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_422_error_create_doctor(self):
        create = self.create
        create['last_name'] = None
        res = self.client().post('/doctors', headers=self.admin, json=self.create)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
    def test_404_patch_doctors(self):
        res = self.client().patch('/doctors/19', headers=self.admin, json=self.patch)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        
    def test_auth_error_patch_doctors(self):
        res = self.client().patch('/doctors/19', json=self.patch)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header not found')

        res = self.client().patch('/doctors/19', headers=self.customer, json=self.patch)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')
    


    def test_3_delete_doctor(self):
        doctor = Doctors.query \
            .filter(
            Doctors.first_name == self.patch['first_name'],
            Doctors.last_name == self.patch['last_name']
        ) \
            .one_or_none()
        res = self.client().delete('/doctors/{}'.format(doctor.doctor_id),
                                   headers=self.admin
                                   )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)



    def test_1_create_doctor(self):
        res = self.client().post('/doctors', headers=self.admin, json=self.create)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['doctor']))


    def test_2_patch_doctors(self):
        doctor = Doctors.query \
            .filter(
            Doctors.first_name == self.create['first_name'],
            Doctors.last_name == self.create['last_name']
        ).one_or_none()
        res = self.client().patch('/doctors/{}'.format(doctor.doctor_id),
                                  headers=self.admin,
                                  json=self.patch
                                  )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['doctor']))





