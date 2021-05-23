DROP TABLE IF EXISTS Appointment;
DROP TABLE IF EXISTS Patient;
DROP TABLE IF EXISTS Doctor_Hospital;
DROP TABLE IF EXISTS Doctor;
DROP TABLE IF EXISTS Hospital;


CREATE TABLE Hospital
(
	hospital_id SERIAL,
	hospital_name VARCHAR NOT NULL,
	description VARCHAR,
	phone VARCHAR NOT NULL,
	start_year INT NOT NULL,
	CONSTRAINT PK_Hospital PRIMARY KEY (hospital_id)
);

CREATE TABLE Doctor
(
	doctor_id SERIAL,
	first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
	categories CHARACTER VARYING(256) NOT NULL,
	languages CHARACTER VARYING(256) NOT NULL,
	experience INT NOT NULL,
	CONSTRAINT PK_Docter PRIMARY KEY (doctor_id)
);


CREATE TABLE Doctor_Hospital
(
	docter_hospital_id SERIAL,
	hospital_id INT NOT NULL,
	doctor_id INT NOT NULL,
	start_date TIMESTAMP,
	CONSTRAINT PK_Docter_Hospital PRIMARY KEY (docter_hospital_id),
	CONSTRAINT FK_Docter_Honspital_Doctor FOREIGN KEY (doctor_id) REFERENCES Doctor(doctor_id)
);

CREATE TABLE Patient
(
	patient_id SERIAL,
	first_name VARCHAR(50),
	last_name VARCHAR(50),
	birth_date DATE,
	Phone VARCHAR(14),
	CONSTRAINT PK_Patient PRIMARY KEY (patient_id)
);

CREATE TABLE Appointment
(
	appointment_id SERIAL,
	doctor_id INT,
	patient_id INT,
	patient_comment VARCHAR(500),
	start_time TIMESTAMP,
	end_time TIMESTAMP,
	visit_cost MONEY,
	CONSTRAINT PK_Appointment PRIMARY KEY (appointment_id),
	CONSTRAINT FK_Appointment_Doctor_Hostpital FOREIGN KEY (doctor_id) REFERENCES Doctor(doctor_id),
	CONSTRAINT FK_Appointment_Patient FOREIGN KEY (patient_id) REFERENCES Patient(patient_id)
)
