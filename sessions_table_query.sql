CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
	user_mail VARCHAR(255) NOT NULL,
	start_time TIMESTAMP NOT NULL,
    total_time_s NUMERIC NOT NULL,
    total_steps INTEGER NOT NULL,
    avg_hr_bpm INTEGER NOT NULL,
    max_hr_bpm INTEGER NOT NULL,
    min_hr_bpm INTEGER NOT NULL,
    avg_bp_sys_mmHg INTEGER NOT NULL,
    max_bp_sys_mmHg INTEGER NOT NULL,
    min_bp_sys_mmHg INTEGER NOT NULL,
    avg_bp_dia_mmHg INTEGER NOT NULL,
    max_bp_dia_mmHg INTEGER NOT NULL,
    min_bp_dia_mmHg INTEGER NOT NULL,
    max_ox INTEGER NOT NULL,
    avg_ox INTEGER NOT NULL,
    min_ox INTEGER NOT NULL,
    temperature_C NUMERIC(5,2) NOT NULL,
	city VARCHAR(20) NOT NULL,
    weather_status VARCHAR(50) NOT NULL
);

SELECT * FROM sessions;