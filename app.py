import os
from flask import Flask, jsonify, request, abort
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

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE'
        )
        return response

    @app.route('/hospital', methods=['GET'])
    def get_hospital():
        try:
            hospital = Hospital.query.all()
            data = [h.format() for h in hospital]
            if not data:
                abort(404)
            return jsonify({
                'success': True,
                'hospital': data
            })
        except:
            abort(422)

    @app.route('/doctors', methods=['GET'])
    def get_doctors():
        try:
            doctors = Doctors.query.all()
            data = [doctor.format() for doctor in doctors]
            if not data:
                abort(404)
            return jsonify({
                'success': True,
                'doctors': data
            })
        except:
            abort(422)

    @app.route('/hospital-detail', methods=['GET'])
    def get_hospital_detail():
        try:
            hospital_id = Hospital.query.distinct(Hospital.hospital_id).all()
            data = [h_id.get_hospital_detail() for h_id in hospital_id]
            if not data:
                abort(404)
            return jsonify({
                'success': True,
                'hospital-detail': data
            })
        except:
            abort(422)

    @app.route('/doctors', methods=['POST'])
    def create_doctor():
        try:
            body = request.get_json()
            if not body:
                abort(400)
            new_doctor = Doctors(
                first_name=body.get('first_name'),
                last_name=body.get('last_name'),
                categories=body.get('categories'),
                languages=body.get('languages'),
                experience=body.get('experience')
            )
            new_doctor.insert()
            return jsonify({
                'success': True,
                'doctor': new_doctor.format()
            })
        except:
            abort(422)

    @app.route('/doctors/<int:doctor_id>', methods=['PATCH'])
    def update_doctor(doctor_id):

        doctor = Doctors.query.get(doctor_id)
        if not doctor:
            abort(404)
        try:
            body = request.get_json()
            doctor.first_name = body.get('first_name')
            doctor.last_name = body.get('last_name')
            doctor.categories = body.get('categories')
            doctor.languages = body.get('languages')
            doctor.experience = body.get('experience')
            print (doctor.experience)
            db.session.commit()

            return jsonify({
                'success': True,
                'doctor': doctor.format()
            })
        except:
            abort(422)

    @app.route('/doctors/<int:doctor_id>', methods=['DELETE'])
    def delete_doctors(doctor_id):

        doctor = Doctors.query.get(doctor_id)
        if not doctor:
            abort(404)
        try:
            doctor.delete()

            return jsonify({
                'success': True,
                'doctor': doctor.format()
            })
        except:
            abort(422)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()