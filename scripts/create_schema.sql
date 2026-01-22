-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.attendance_audits (
  id bigint NOT NULL DEFAULT nextval('attendance_audits_id_seq'::regclass),
  attendance_id bigint NOT NULL,
  old_status character CHECK (old_status = ANY (ARRAY['P'::bpchar, 'A'::bpchar])),
  new_status character CHECK (new_status = ANY (ARRAY['P'::bpchar, 'A'::bpchar])),
  edited_by bigint,
  edited_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT attendance_audits_pkey PRIMARY KEY (id),
  CONSTRAINT attendance_audits_attendance_id_fkey FOREIGN KEY (attendance_id) REFERENCES public.attendance_records(id),
  CONSTRAINT attendance_audits_edited_by_fkey FOREIGN KEY (edited_by) REFERENCES public.users(id)
);
CREATE TABLE public.attendance_records (
  id bigint NOT NULL DEFAULT nextval('attendance_records_id_seq'::regclass),
  lecture_id bigint NOT NULL,
  student_id bigint NOT NULL,
  status character NOT NULL CHECK (status = ANY (ARRAY['P'::bpchar, 'A'::bpchar])),
  recorded_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT attendance_records_pkey PRIMARY KEY (id),
  CONSTRAINT attendance_records_lecture_id_fkey FOREIGN KEY (lecture_id) REFERENCES public.lectures(id),
  CONSTRAINT attendance_records_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.students(id)
);
CREATE TABLE public.departments (
  id bigint NOT NULL DEFAULT nextval('departments_id_seq'::regclass),
  name text NOT NULL UNIQUE,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT departments_pkey PRIMARY KEY (id)
);
CREATE TABLE public.divisions (
  id bigint NOT NULL DEFAULT nextval('divisions_id_seq'::regclass),
  name text NOT NULL UNIQUE,
  semester smallint NOT NULL CHECK (semester >= 1 AND semester <= 8),
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT divisions_pkey PRIMARY KEY (id)
);
CREATE TABLE public.faculty (
  id bigint NOT NULL DEFAULT nextval('faculty_id_seq'::regclass),
  user_id bigint NOT NULL UNIQUE,
  department text NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT faculty_pkey PRIMARY KEY (id),
  CONSTRAINT faculty_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id)
);
CREATE TABLE public.hods (
  id bigint NOT NULL DEFAULT nextval('hods_id_seq'::regclass),
  user_id bigint NOT NULL UNIQUE,
  department_id bigint,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT hods_pkey PRIMARY KEY (id),
  CONSTRAINT hods_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id),
  CONSTRAINT hods_department_id_fkey FOREIGN KEY (department_id) REFERENCES public.departments(id)
);
CREATE TABLE public.lectures (
  id bigint NOT NULL DEFAULT nextval('lectures_id_seq'::regclass),
  timetable_id bigint NOT NULL,
  lecture_date date NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT lectures_pkey PRIMARY KEY (id),
  CONSTRAINT lectures_timetable_id_fkey FOREIGN KEY (timetable_id) REFERENCES public.timetable_entries(id)
);
CREATE TABLE public.notifications (
  id bigint NOT NULL DEFAULT nextval('notifications_id_seq'::regclass),
  user_id bigint NOT NULL,
  message text NOT NULL,
  seen boolean NOT NULL DEFAULT false,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT notifications_pkey PRIMARY KEY (id),
  CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id)
);
CREATE TABLE public.students (
  id bigint NOT NULL DEFAULT nextval('students_id_seq'::regclass),
  user_id bigint NOT NULL UNIQUE,
  enrollment_no text NOT NULL UNIQUE,
  division_id bigint,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT students_pkey PRIMARY KEY (id),
  CONSTRAINT students_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id),
  CONSTRAINT students_division_id_fkey FOREIGN KEY (division_id) REFERENCES public.divisions(id)
);
CREATE TABLE public.subjects (
  id bigint NOT NULL DEFAULT nextval('subjects_id_seq'::regclass),
  code text NOT NULL UNIQUE,
  name text NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT subjects_pkey PRIMARY KEY (id)
);
CREATE TABLE public.timetable_entries (
  id bigint NOT NULL DEFAULT nextval('timetable_entries_id_seq'::regclass),
  subject_id bigint NOT NULL,
  faculty_id bigint,
  division_id bigint,
  day text NOT NULL,
  slot text NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT timetable_entries_pkey PRIMARY KEY (id),
  CONSTRAINT timetable_entries_subject_id_fkey FOREIGN KEY (subject_id) REFERENCES public.subjects(id),
  CONSTRAINT timetable_entries_faculty_id_fkey FOREIGN KEY (faculty_id) REFERENCES public.faculty(id),
  CONSTRAINT timetable_entries_division_id_fkey FOREIGN KEY (division_id) REFERENCES public.divisions(id)
);
CREATE TABLE public.users (
  id bigint NOT NULL DEFAULT nextval('users_id_seq'::regclass),
  email text NOT NULL UNIQUE,
  password_hash text NOT NULL,
  role text NOT NULL CHECK (role = ANY (ARRAY['Admin'::text, 'HOD'::text, 'Faculty'::text, 'Student'::text])),
  CONSTRAINT users_pkey PRIMARY KEY (id)
);