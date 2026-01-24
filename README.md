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
| Super Admin | `Admin@edu.com` | `Admin@1212` |

### Demo College (Engineering)
| Role          | Email                 | Password              |
| ------------- | --------------------- | --------------------- |
| College Admin | `admin@college.edu`   | `AdminPassword123!`   |
| HOD           | `hod@college.edu`     | `HodPassword123!`     |
| Faculty       | `faculty@college.edu` | `FacultyPassword123!` |
| Student       | `student@college.edu` | `StudentPassword123!` |

> **Note**: For new users, use the **Sign Up** page. Registration requires selecting a college (created by Super Admin). New accounts are "Pending" until approved by their respective superior (HOD approves Faculty, Faculty approves Students).

## 📂 Project Structure

*   `attendance_system/`
    *   `blueprints/`: Route controllers for each role.
    *   `models/`: Data classes and persistence logic.
    *   `services/`: PDF parsing, Calendar logic, Search service (BST).
    *   `templates/`: Jinja2 HTML templates.
    *   `static/`: CSS, JS, and Images.
    *   `db_manager.py`: Database connection and execution utilities.
*   `seed_db.py`: Database migration and seeding script.
*   `diagnose_login.py`: Utility to test DB connectivity.

## 🤝 Contribution
Authored by **Dhruvil Thummar**.