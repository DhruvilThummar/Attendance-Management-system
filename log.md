Contribution Log

How to add an entry (keep it brief):
1. Name - Date / Time - Contribution (2-3 lines, max 5-6 lines)

-----------------------------------------------------------
1. Dhruvil Thummar & Om Meruliya - 03 Jan 2026
   - Initialized Data Base and Crete Data Base.

2. Dhruvil Thummar - 03 Feb 2026
   - Updated registration flow with modal-based role selection and role-specific fields.
   - Consolidated auth styles/scripts into shared assets and added comments across templates.
   - Improved validation logic, added student semester field, and cleaned unused assets.

3. Dhruvil Thummar - 04 Feb 2026
   - Created comprehensive college dashboard with responsive sidebar (desktop fixed + mobile offcanvas).
   - Implemented 2-column division card layout responsive across all devices (mobile: 1 col, tablet/desktop: 2 col).
   - Added college admin routes: /collegedashboard, /college/departments, /college/divisions, /college/faculty, /college/students, /college/attendance-analytics, /college/settings.
   - Fixed duplicate route definitions and created missing college/settings.html template.
   - Implemented department selector with localStorage persistence and navigation menu visibility toggle.

4. Dhruvil Thummar - 04 Feb 2026
   - Fixed CSS nested media queries and column width conflicts in college-dashboard.css.
   - Resolved offcanvas sidebar empty navigation display issue - simplified flex layout rules.
   - Removed duplicate /collegedashboard route that was causing Flask AssertionError.
   - Tested all college routes - app running successfully on http://127.0.0.1:5000