CREATE TABLE users (
	user_mail VARCHAR(255) PRIMARY KEY, -- user e-mail as primary key is widely used in many sites
	first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
	is_male BOOLEAN NOT NULL,
	birth_date DATE NOT NULL,
	weight_kg NUMERIC(5,2) NOT NULL, -- up to 999.99 kg (a little over the top)
	height_m NUMERIC(3,2) NOT NULL, -- up to 9.99 m (a little over the top)
	bmi NUMERIC(3,1) NOT NULL -- up to 99.9 (a little over the top)
);

SELECT * FROM users;