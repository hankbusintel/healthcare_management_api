import os
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from models import db, Hospital, Doctors, DoctorHospital
from auth.auth import AuthError, requires_auth



def get_current_page(query, page_no):
    start = (page_no-1)*10
    end = start+10
    #count = len([q.id for q in query])
    return query[start:end]


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('config')
    db.init_app(app)
    CORS(app)
    #with app.app_context():
        #db.create_all()

    @app.route('/')
    def get_greeting():
        greeting = """Hello, welcome to the main page of the healthcare_management api,
        please refer to the README.MD while testing the API.
        """
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
            page = request.args.get('page', 1, type=int)
            hospital = Hospital.query.all()
            query = get_current_page(hospital, page)
        except:
            abort(422)
        data = [h.format() for h in query]
        if not data:
            abort(404)
        return jsonify({
            'success': True,
            'hospital': data
        })

    @app.route('/doctors', methods=['GET'])
    def get_doctors():
        try:
            page = request.args.get('page', 1, type=int)
            doctors = Doctors.query.all()
            query = get_current_page(doctors, page)
        except:
            abort(422)
        data = [doctor.format() for doctor in query]
        if not data:
            abort(404)
        return jsonify({
            'success': True,
            'doctors': data
        })

    @app.route('/hospital-detail', methods=['GET'])
    @requires_auth('get:MyApp')
    def get_hospital_detail():
        try:
            page = request.args.get('page', 1, type=int)
            hospital_id = Hospital.query.distinct(Hospital.hospital_id).all()
            data = [h_id.get_hospital_detail() for h_id in hospital_id]
        except:
            abort(422)
        current_page = get_current_page(data, page)
        if not current_page:
            abort(404)
        return jsonify({
            'success': True,
            'hospital-detail': current_page
        })


    @app.route('/doctors', methods=['POST'])
    @requires_auth('post:MyApp')
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
    @requires_auth('patch:MyApp')
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
    @requires_auth('delete:MyApp')
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

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Failed to verify authentication token."
        }), 400

    @app.errorhandler(401)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized access or token expired."
        }), 401

    @app.errorhandler(403)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Permission not found in token."
        }), 403

    @app.errorhandler(AuthError)
    def authentification_failed(AuthError):
        return jsonify({
            "success": False,
            "error": AuthError.status_code,
            "message": AuthError.error['description']
        }), 401

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8080, debug=True)