import os
from flask import Flask, jsonify
from flask_cors import CORS
from models import db, Hospital


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
        print(data)
        return jsonify({
            'success': True,
            'hospital': data
        })

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()