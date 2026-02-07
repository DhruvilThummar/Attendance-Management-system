# Attendify - Smart Attendance Management System

**Attendify** is a robust, role-based web application designed to streamline attendance tracking for educational institutions. It features real-time logging, automated reporting, and a multi-tenant architecture supporting multiple colleges.

## 🚀 Key Features

*   **Multi-Tenancy Support**: Manage multiple colleges/institutions from a single instance.
*   **Role-Based Access Control (RBAC)**: secure dashboards for:
    *   **Super Admin**: Global management of colleges.
    *   **College Admin**: Manage users, subjects, and timetables for their college.
    *   **HOD (Head of Department)**: Analytics and faculty approvals.
    *   **Faculty**: Mark attendance and view defaulters.
    *   **Student**: View personal attendance stats and alerts.
*   **Smart Automation**:
    *   **Timetable Parsing**: Upload a PDF timetable to auto-generate schedules.
    *   **Lecture Generation**: Auto-generates daily lecture slots based on the weekly timetable.
    *   **Defaulter Detection**: Automatically flags students below the attendance threshold (e.g., 75%).
    *   **BST Search**: Optimized student search using Binary Search Trees.
*   **Analytics & Reports**:
    *   Visual charts for attendance trends (Matplotlib).
    *   PDF Report generation for official records.
*   **User Friendly UI**: Responsive, glassmorphism-inspired design with Dark Mode footer.

## 🛠️ Tech Stack

*   **Backend**: Python, Flask
*   **Database**: MySQL (using `mysql-connector-python`)
*   **Frontend**: HTML5, CSS3, JavaScript (Bootstrap 5)
*   **Utilities**: 
    *   `pdfplumber` (PDF Parsing)
    *   `reportlab` (PDF Generation)
    *   `matplotlib` (Data Visualization)

## ⚙️ Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/DhruvilThummar/Attendance-Management-system.git
    cd Attendance-Management-system
    ```

2.  **Set up Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -e .
    ```

4.  **Configure Environment**
    Create a `.env` file in the root directory:
    ```ini
    DATABASE_URL=mysql://root:password@localhost:3306/attendance_db
    SECRET_KEY=your_secret_key_here
    ```

5.  **Initialize Database**
    Run the seeding script to create tables and populate initial data:
    ```bash
    python seed_db.py
    ```

6.  **Run the Application**
    ```bash
    flask run
    ```
    Access the app at `http://localhost:5000`.

## 🔐 Default Credentials

The system comes pre-seeded with the following accounts for testing.

### Super Admin (Global Scope)
| Role        | Email           | Password     |
| ----------- | --------------- | ------------ |
| Super Admin | `Admin@edu.com` | `Admin@123` |

### Demo College (Engineering)
| Role          | Email                 | Password              |
| ------------- | --------------------- | --------------------- |
| College Admin | `admin@college.edu`   | `Admin@123`   |
| HOD           | `hod@college.edu`     | `hod@123`     |
| Faculty       | `faculty@college.edu` | `faculty@123` |
| Student       | `student@college.edu` | `student@123!` |

> **Note**: For new users, use the **Sign Up** page. Registration requires selecting a college (created by Super Admin). New accounts are "Pending" until approved by their respective superior (HOD approves Faculty, Faculty approves Students).

## 📂 Project Structure

```
attendance_system
├──models
│   ├──__init__.py
│   ├──academic_calendar.py
│   ├──attendance.py
│   ├──college.py
│   ├──department.py
│   ├──division.py
│   ├──faculty.py
│   ├──lecture.py
│   ├──parent.py
│   ├──proxy_lecture.py
│   ├──student.py
│   ├──subject.py
│   ├──timetable.py
│   └──user.py
├──routes
│   ├──__init__.py
│   ├──auth.py
│   ├──college.py
│   ├──faculty.py
│   ├──hod.py
│   ├──main.py
│   ├──parent.py
│   ├──student.py
│   └──superadmin.py
├──services
│   ├──chart_helper.py
│   └──data_helper.py
├──static
│   ├──css
│   │   ├──auth.css
│   │   ├──college-dashboard.css
│   │   ├──faculty.css
│   │   ├──profile.css
│   │   ├──register-form.css
│   │   └──style.css
│   ├──img
│   │   ├──logos
│   │   │   └──attendify.svg
│   │   └──Gemini_Generated_Image_u1vmhru1vmhru1vm.png
│   └──js
│   │   ├──auth.js
│   │   ├──college-dashboard.js
│   │   ├──login.js
│   │   ├──profile.js
│   │   ├──register.js
│   │   ├──scripts.js
│   │   └──session-manager.js
├──templates
│   ├──college
│   │   ├──components
│   │   │   ├──footer.html
│   │   │   └──nav.html
│   │   ├──attendance-analytics.html
│   │   ├──cbase.html
│   │   ├──dashboard.html
│   │   ├──departments.html
│   │   ├──divisions.html
│   │   ├──faculty.html
│   │   ├──profile.html
│   │   ├──settings.html
│   │   └──students.html
│   ├──components
│   │   ├──chart.html
│   │   ├──footer.html
│   │   └──navbar.html
│   ├──faculty
│   │   ├──components
│   │   │   ├──footer.html
│   │   │   ├──nav.html
│   │   │   └──profile_card.html
│   │   ├──analytics.html
│   │   ├──attendance.html
│   │   ├──dashboard.html
│   │   ├──fbase.html
│   │   ├──profile.html
│   │   ├──reports.html
│   │   └──timetable.html
│   ├──hod
│   │   ├──components
│   │   │   ├──footer.html
│   │   │   └──nav.html
│   │   ├──attendance.html
│   │   ├──dashboard.html
│   │   ├──faculty.html
│   │   ├──hbase.html
│   │   ├──profile.html
│   │   ├──subjects.html
│   │   └──timetable.html
│   ├──parent
│   │   ├──components
│   │   │   ├──footer.html
│   │   │   └──nav.html
│   │   ├──attendance.html
│   │   ├──dashboard.html
│   │   ├──pbase.html
│   │   └──profile.html
│   ├──student
│   │   ├──components
│   │   │   ├──footer.html
│   │   │   └──nav.html
│   │   ├──attendance.html
│   │   ├──dashboard.html
│   │   ├──profile.html
│   │   └──sbase.html
│   ├──superadmin
│   │   ├──components
│   │   │   ├──footer.html
│   │   │   └──nav.html
│   │   ├──analytics.html
│   │   ├──college_details.html
│   │   ├──colleges.html
│   │   ├──dashboard.html
│   │   ├──departments.html
│   │   ├──faculty.html
│   │   ├──profile.html
│   │   ├──students.html
│   │   ├──subase.html
│   │   └──users.html
│   ├──about.html
│   ├──base.html
│   ├──contact.html
│   ├──home.html
│   ├──login.html
│   └──register.html
├──utils
│   ├──__init__.py
│   └──simple_hash.py
├──__init__.py
├──app.py
└──schema.sql
```

## 🤝 Contribution
Authored by **Dhruvil Thummar**