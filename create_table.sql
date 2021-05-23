DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS doctor_hospital;
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS hospital;


CREATE TABLE hospital
(
	hospital_id SERIAL,
	name VARCHAR NOT NULL,
	description VARCHAR,
	phone VARCHAR NOT NULL,
	start_year INT NOT NULL,
	CONSTRAINT PK_hospital PRIMARY KEY (hospital_id)
);



CREATE TABLE doctors
(
	doctor_id SERIAL,
	first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
	categories CHARACTER VARYING(256) NOT NULL,
	languages CHARACTER VARYING(256) NOT NULL,
	experience INT NOT NULL,
	CONSTRAINT PK_docter PRIMARY KEY (doctor_id)
);

INSERT INTO doctors
(first_name,last_name,categories,languages,experience)
VALUES
('Hang','Guo','')

CREATE TABLE doctor_hospital
(
	docter_hospital_id SERIAL,
	hospital_id INT NOT NULL,
	doctor_id INT NOT NULL,
	start_date TIMESTAMP,
	CONSTRAINT PK_docter_hospital PRIMARY KEY (docter_hospital_id),
	CONSTRAINT FK_docter_honspital_Doctor FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

CREATE TABLE patients
(
	patient_id SERIAL,
	first_name VARCHAR(50),
	last_name VARCHAR(50),
	birth_date DATE,
	Phone VARCHAR(14),
	CONSTRAINT PK_patient PRIMARY KEY (patient_id)
);

CREATE TABLE appointments
(
	appointment_id SERIAL,
	doctor_id INT,
	patient_id INT,
	patient_comment VARCHAR(500),
	start_time TIMESTAMP,
	end_time TIMESTAMP,
	visit_cost MONEY,
	CONSTRAINT PK_appointment PRIMARY KEY (appointment_id),
	CONSTRAINT FK_appointment_doctor_hostpital FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
	CONSTRAINT FK_appointment_patient FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);

INSERT INTO hospital 
(name, description, phone, start_year)
VALUES
('Hoag','A good hospital','606-330-0123',1999)

