import os
from flask import Flask, jsonify
from flask_cors import CORS
from models import db, Hospital, Doctors, DoctorHospital


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('config')
    db.init_app(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        greeting = "Hello"
        return greeting

    @app.route('/hospital', methods=['GET'])
    def get_hospital():
        hospital = Hospital.query.all()
        data = [h.format() for h in hospital]

        return jsonify({
            'success': True,
            'hospital': data
        })

    @app.route('/doctors', methods=['GET'])
    def get_doctors():
        doctors = Doctors.query.all()
        data = [doctor.format() for doctor in doctors]

        return jsonify({
            'success': True,
            'doctors': data
        })

    @app.route('/hospital-detail', methods=['GET'])
    def get_hospital_detail():
        hospital_id = Hospital.query.distinct(Hospital.hospital_id).all()
        data = [h_id.get_hospital_detail() for h_id in hospital_id]
        print(data)
        return jsonify({
            'success': True,
            'hospital-detail': data
        })


    return app



if __name__ == '__main__':
    app = create_app()
    app.run()