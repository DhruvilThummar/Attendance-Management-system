
-- Postgres schema for the Attendance Management System.
-- Run with: psql "$DATABASE_URL" -f scripts/create_schema.sql

BEGIN;

-- Optional lookup for departments (referenced by HODs).
CREATE TABLE IF NOT EXISTS departments (
	id          BIGSERIAL PRIMARY KEY,
	name        TEXT NOT NULL UNIQUE,
	created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS users (
	id             BIGSERIAL PRIMARY KEY,
	email          TEXT NOT NULL UNIQUE,
	password_hash  TEXT NOT NULL,
	role           TEXT NOT NULL CHECK (role IN ('Admin', 'HOD', 'Faculty', 'Student')),
	created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS divisions (
	id          BIGSERIAL PRIMARY KEY,
	name        TEXT NOT NULL UNIQUE,
	semester    SMALLINT NOT NULL CHECK (semester BETWEEN 1 AND 8),
	created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS subjects (
	id          BIGSERIAL PRIMARY KEY,
	code        TEXT NOT NULL UNIQUE,
	name        TEXT NOT NULL,
	created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS faculty (
	id           BIGSERIAL PRIMARY KEY,
	user_id      BIGINT NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
	department   TEXT NOT NULL,
	created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS hods (
	id             BIGSERIAL PRIMARY KEY,
	user_id        BIGINT NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
	department_id  BIGINT REFERENCES departments(id) ON DELETE SET NULL,
	created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS students (
	id             BIGSERIAL PRIMARY KEY,
	user_id        BIGINT NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
	enrollment_no  TEXT NOT NULL UNIQUE,
	division_id    BIGINT REFERENCES divisions(id) ON DELETE SET NULL,
	created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS timetable_entries (
	id           BIGSERIAL PRIMARY KEY,
	subject_id   BIGINT NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
	faculty_id   BIGINT REFERENCES faculty(id) ON DELETE SET NULL,
	division_id  BIGINT REFERENCES divisions(id) ON DELETE CASCADE,
	day          TEXT NOT NULL,  -- e.g., Monday
	slot         TEXT NOT NULL,  -- e.g., 09:00-10:00
	created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	CONSTRAINT uniq_division_slot UNIQUE (division_id, day, slot)
);

CREATE TABLE IF NOT EXISTS lectures (
	id            BIGSERIAL PRIMARY KEY,
	timetable_id  BIGINT NOT NULL REFERENCES timetable_entries(id) ON DELETE CASCADE,
	lecture_date  DATE NOT NULL,
	created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	CONSTRAINT uniq_lecture_per_day UNIQUE (timetable_id, lecture_date)
);

CREATE TABLE IF NOT EXISTS attendance_records (
	id           BIGSERIAL PRIMARY KEY,
	lecture_id   BIGINT NOT NULL REFERENCES lectures(id) ON DELETE CASCADE,
	student_id   BIGINT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
	status       CHAR(1) NOT NULL CHECK (status IN ('P', 'A')),
	recorded_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	CONSTRAINT uniq_attendance_per_student UNIQUE (lecture_id, student_id)
);

CREATE TABLE IF NOT EXISTS attendance_audits (
	id             BIGSERIAL PRIMARY KEY,
	attendance_id  BIGINT NOT NULL REFERENCES attendance_records(id) ON DELETE CASCADE,
	old_status     CHAR(1) CHECK (old_status IN ('P', 'A')),
	new_status     CHAR(1) CHECK (new_status IN ('P', 'A')),
	edited_by      BIGINT REFERENCES users(id) ON DELETE SET NULL,
	edited_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS notifications (
	id          BIGSERIAL PRIMARY KEY,
	user_id     BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
	message     TEXT NOT NULL,
	seen        BOOLEAN NOT NULL DEFAULT FALSE,
	created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Helpful indexes for lookups.
CREATE INDEX IF NOT EXISTS idx_students_division ON students(division_id);
CREATE INDEX IF NOT EXISTS idx_faculty_department ON faculty(department);
CREATE INDEX IF NOT EXISTS idx_timetable_division_day ON timetable_entries(division_id, day);
CREATE INDEX IF NOT EXISTS idx_attendance_lecture ON attendance_records(lecture_id);
CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id);

COMMIT;
