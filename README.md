# Student Profile

A web application for managing and viewing student profiles for ESPAM FORMATION UNIVERSITY. The project provides features for searching, filtering, and exporting student information, along with an admin dashboard and user authentication.

## Features

- **Student and Staff Management**: View detailed student and staff profiles, including photos and personal information.
- **Search and Filter**: Quickly search and filter students by name or academic level.
- **Bulk Actions**: Select all or individual students by level for group actions.
- **Export**: Export student details (e.g., to PDF) for administrative use.
- **Admin Dashboard**: Admin and staff dashboards for managing users and records.
- **Responsive UI**: User-friendly interface with dynamic navigation and theming.
- **Authentication**: Secure login for staff and admins, with password validation.

## Technologies Used

- **Backend**: Python (Django)
- **Frontend**: HTML, CSS, JavaScript
- **UI Libraries**: Bootstrap, Font Awesome

## Project Structure

- `studentprofile/` – Django project with core settings and application logic.
- `templates/` – HTML templates for different pages like student details, admin dashboard, and index.
- `static/` – Static assets (CSS, JavaScript, images).
- `staticfiles/` – Collected static files for deployment.
- `static/js/script.js` – Main frontend logic for search, selection, and UI interactions.
- `staticfiles/admin/js/` – Admin panel JavaScript (sidebar, theme, core helpers).

## Setup and Installation

1. **Clone the repository:**
   ```
   git clone https://github.com/EmmanuelAyanleye/Student-Profile.git
   cd Student-Profile
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Apply migrations:**
   ```
   python manage.py migrate
   ```

4. **Run the development server:**
   ```
   python manage.py runserver
   ```

5. **Access the app:**
   - Open [http://localhost:8000](http://localhost:8000) in your browser.

## Usage

- Log in as an admin or staff member.
- Use the dashboard to search, filter, and manage student profiles.
- Export student details as needed.
- Access different modules via the navigation sidebar.

## Contribution

Contributions are welcome! Please open an issue or submit a pull request for improvements or bug fixes.

## License

- Font Awesome icons used under the [SIL OFL 1.1](https://scripts.sil.org/OFL) and [MIT License](https://github.com/encharm/Font-Awesome-SVG-PNG).
- See the `staticfiles/admin/img/README.txt` for more details.
