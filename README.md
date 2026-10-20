🥗 Diet Planning Management System

📌 Project Overview

The Diet Planning Management System is a web-based application developed using Python Flask and MySQL. It helps users obtain diet recommendations based on their health information, BMI, selected disease, and dietary goals. The system provides daily, weekly, and monthly diet plans, water intake recommendations, and nutrition information. It also includes an admin dashboard to monitor user activities and manage user messages.

✨ Features

- 🔐 User Registration, Login, and Logout
- 🧑‍⚕️ User Health Information Management
- ⚖️ Automatic BMI Calculation and Analysis
- 🥗 Personalized Diet Plan Recommendations
- 📅 Daily, Weekly, and Monthly Diet Plans
- 💧 Water Intake Recommendations
- 🥑 Nutritional Information, Including Calories, Protein, Carbohydrates, and Fat (where available)
- 📩 User-to-Admin Messaging
- 💬 Admin Reply Management
- 📊 Admin Dashboard with User, Report, Message, and Diet Request Counts
- 🗄️ MySQL Database Integration
- 🎨 Animated Food Background and Glass-Effect Interface

🛠️ Technologies Used

- Frontend: HTML5, CSS3
- Backend: Python, Flask
- Database: MySQL
- Database Tool: MySQL Workbench
- Template Engine: Jinja2

📦 Project Modules

1. Login and Logout Module – Provides account access and session management.
2. User Health Information Module – Collects and stores user health details.
3. Diet Plan Generation Module – Displays diet recommendations for different durations.
4. BMI and Diet Analysis Module – Calculates BMI and provides basic diet-related guidance.
5. Message Module – Allows users to send messages to the administrator.
6. Admin Monitoring and Reply Module – Displays dashboard statistics and supports message management.

🗂️ Project Structure

Diet-Planning-Management-System/
│
├── app.py
├── requirements.txt
├── README.md
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── home.html
│   ├── result.html
│   ├── admin.html
│   └── admin_messages.html
│
├── static/
│   └── css/
│       └── style.css
│
└── database.sql

Note: The structure above is an example. Adjust the filenames to match the files in your repository.

⚙️ Installation and Setup

1. Install Python and MySQL

Install Python and MySQL Server. MySQL Workbench can be used to execute SQL queries and manage the database.

2. Clone the Repository

git clone https://github.com/YOUR-USERNAME/Diet-Planning-Management-System.git

Replace "YOUR-USERNAME" with your GitHub username.

3. Open the Project Folder

cd Diet-Planning-Management-System

4. Install Python Dependencies

pip install -r requirements.txt

5. Create the MySQL Database

Open MySQL Workbench and execute:

CREATE DATABASE diet_system;

Import or execute the SQL statements required to create and populate the project's tables.

6. Configure the Database Connection

Update the MySQL connection settings in "app.py" to match your local MySQL configuration.

Security note: Do not publish your real database password or Flask secret key in a public repository. Use environment variables for sensitive configuration.

7. Run the Application

python app.py

Open your browser and visit:

http://127.0.0.1:5000/

🗄️ Database Tables

The project may include the following tables, depending on the features configured in your database:

- "users"
- "user_inputs"
- "suggestions"
- "weekly_diet"
- "weekly_diet_detailed"
- "diet_requests"
- "diet_rules"
- "messages"

📸 Screenshots

Add screenshots of your actual application to demonstrate its functionality.

Recommended screenshots:

- Login and Registration Pages
- User Health Information Page
- Daily Diet Plan
- Weekly Diet Plan
- Monthly Diet Plan
- BMI and Diet Analysis Report
- Admin Dashboard
- Admin Messages and Replies

🚀 Future Enhancements

- AI-assisted diet recommendations
- Advanced nutrition tracking
- Food preference and allergy management
- Progress tracking and diet history
- Mobile application integration
- Doctor or nutritionist consultation support

📚 References

1. Python: https://www.python.org/
2. Flask Documentation: https://flask.palletsprojects.com/
3. MySQL Documentation: https://dev.mysql.com/doc/

🎓 Project Purpose

This project was developed as an academic project to demonstrate database management, web application development, user information management, and personalized diet plan presentation using Python Flask and MySQL.

---

Developed by: Narmatha
