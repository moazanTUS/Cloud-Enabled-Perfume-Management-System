# Cloud-Enabled-Perfume-Management-System
This project is a web-based application for managing perfume inventory, built with Flask and integrated with an SQLite database. It features CRUD functionality, search capabilities, and modern deployment tools like Docker.

Key Components
Backend (app.py):

Flask application with SQLAlchemy for ORM.
Implements:
CRUD operations for perfumes.
Routing for frontend integration.
Key routes interact with the Perfume model:
Attributes: id, name, brand, scent, price, quantity.
Frontend (templates directory):

HTML templates for various actions:
show_all.html: Displays all perfume records.
new.html: Adds new perfume entries.
update2.html: Updates perfume details.
search.html: Enables searching perfumes by attributes.
increment_quantity.html: Handles stock adjustments.


Technologies Used
Backend: Python, Flask, SQLAlchemy.
Frontend: HTML, CSS.
Database: SQLite.
Deployment: Docker

Features
CRUD Functionality:
Add, update, delete, and view perfumes.
Search and Filter:
Search perfumes by attributes like name, brand, or scent.
Stock Management:
Increment or decrement stock quantities.
Responsive Frontend:
Styled templates with custom CSS and icons.
