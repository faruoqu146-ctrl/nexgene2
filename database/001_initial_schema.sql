CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(320) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    display_name VARCHAR(120),
    date_of_birth VARCHAR(10),
    sex_at_birth VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS observation_types (
    id SERIAL PRIMARY KEY,
    code VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    unit VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS observations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    observation_type_id INTEGER NOT NULL REFERENCES observation_types(id),
    numeric_value DOUBLE PRECISION,
    text_value TEXT,
    boolean_value BOOLEAN,
    recorded_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT observation_one_value CHECK (
        (CASE WHEN numeric_value IS NOT NULL THEN 1 ELSE 0 END) +
        (CASE WHEN text_value IS NOT NULL THEN 1 ELSE 0 END) +
        (CASE WHEN boolean_value IS NOT NULL THEN 1 ELSE 0 END) = 1
    )
);

INSERT INTO observation_types (code, name, unit) VALUES
('sleep_duration', 'Sleep duration', 'hours'),
('sleep_quality', 'Sleep quality', NULL),
('energy', 'Energy', NULL),
('mood', 'Mood', NULL),
('stress', 'Stress', NULL),
('focus', 'Focus', NULL),
('activity_duration', 'Activity duration', 'minutes'),
('weight', 'Weight', 'kg'),
('heart_rate', 'Heart rate', 'bpm'),
('hrv', 'Heart rate variability', 'ms'),
('blood_pressure_systolic', 'Blood pressure systolic', 'mmHg'),
('blood_pressure_diastolic', 'Blood pressure diastolic', 'mmHg'),
('glucose', 'Glucose', 'mg/dL'),
('temperature', 'Temperature', 'C')
ON CONFLICT (code) DO NOTHING;
