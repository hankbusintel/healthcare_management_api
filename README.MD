**Project Description**

This is a prototype of a healthcare management api, it contains doctors and 
hospital infomation that can be used by web / Mobile / Desktop application. 
The api implemented the auth0 authentication for different role groups.


**Local Installation Instruction**
(1) Create two database named: healthcare_management, healthcare_management_test
(2) Type the following in terminal:
psql healthcare_management < create_table.psql
psql healthcare_management_test 
(3) Run app.py file to run the application
(4) Run test_api.py to run test cases


**API Documentation**
Domain name: https://hmpuapi.herokuapp.com/
HTTP REQUEST
Authentication: Bearer JWT

*End Point*
GET /doctors
Description: Get doctor's infomation.
Json response:
{
    "doctors": [
    {
    "categories": "{...}",
    "experience": ...,
    "id": ...,
    "languages": "{...}",
    "name": ...
    },
    ...
    ],
"success": true
}

GET /hospital
Description: Get hospital info
Json response
{
    "hospital": [
        {
            "description": ...,
            "id": 1,
            "name": ...,
            "phone": ...,
            "start_year": ...
        },
        ...
    ],
    "success": true
}

GET /hospital-detail
Description: Get detail information from hospital(Including doctors who are working
in the hospital)
Json response

{
    "hospital-detail": [{
        "description": "A good hospital",
        "doctors": [
            {
            "doctor_hospital_id": ...,
            "doctor_id": ...,
            "doctor_name": ...,
            "start_date": "Thu, 05 Jan 2012 00:00:00 GMT"
            },
            ...
        ],
        "id": ...,
        "name": ...,
        "phone": ...,
        "start_year": ...
        },
        ...
    }],
    "success": true
}

PATCH /doctors/<int:doctor_id>
Description: Update existing doctor
Payload:
{
    "first_name": ...,
    "last_name": ...,
    "categories": [...],
    "experience": ...,
    "languages": [...]
}

Json Response:
{
    "doctor": {
    "categories": "{...}",
    "experience": ...,
    "id": ...,
    "languages": "{...}",
    "name": ...
    },
    "success": true
}

POST /doctors
Description: Create a new doctor.
Payload:
{
    "first_name": ...,
    "last_name": ...,
    "categories": [...],
    "experience": ...,
    "languages": [...]
}

Json Response:
{
    "doctor": {
    "categories": ...,
    "experience": ...,
    "id": ...,
    "languages": ...,
    "name": ...
    },
    "success": true
}

DELETE /doctors/<int:doctor_id>
Description: Delete doctor from the system.
Json Response:
{
    "doctor": {
    "categories": ...,
    "experience": ...,
    "id": ...,
    "languages": "{...}",
    "name": ...
    },
    "success": true
}
