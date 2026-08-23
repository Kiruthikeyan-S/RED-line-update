# 🩸 Red Line – Blood Donation Platform


Red Line is a blood donation management platform designed to connect **blood donors, patients, hospitals, and emergency blood requests** through a centralized web application.

The main goal of the project is to make it easier to identify potential blood donors and improve communication during urgent blood requirements.

## 📌 Project Overview

During a medical emergency, finding a suitable blood donor quickly can be difficult.

**Red Line** addresses this problem by providing a platform where users can:

* Register as blood donors
* Search for available donors
* Submit blood requests
* Manage donor information
* Connect blood requirements with potential donors
* Use location-based information to identify nearby resources
* Support faster emergency response

The project focuses on improving the coordination between donors and people who need blood.

## ✨ Key Features

### 🩸 Donor Management

* Donor registration
* Blood group information
* Donor details management
* Donor availability tracking

### 🚨 Blood Requests

* Create blood requests
* Specify required blood group
* Manage emergency requirements
* Track blood donation requests

### 📍 Location-Based Donor Discovery

* Identify donors based on location
* Interactive map-based donor visualization
* Connect donors with nearby healthcare requirements

### 🏥 Healthcare Support

* Helps connect blood donors with healthcare facilities
* Provides a centralized platform for blood-related requests

### 💾 Database Management

The application uses databases to store information related to:

* Donors
* Blood donations
* Blood requests
* Application data

## 🛠️ Technologies Used

* **Python**
* **Flask**
* **SQLite**
* **HTML5**
* **CSS3**
* **JavaScript**
* **Maps / Location Services**

## 📂 Project Structure

```text
Red-line-project/
│
├── donor/
│
├── static/
│
├── static_1/
│   └── css/
│
├── static_2/
│   └── image/
│
├── templates/
│
├── app.py
│
├── blood_donations.db
├── blood_requests.db
├── database.db
├── default.db
│
├── red line pro.zip
│
└── README.md
```

## 🔄 Application Workflow

```text
User
  │
  ▼
Red Line Web Application
  │
  ├── Register / Login
  │
  ├── Donor Management
  │
  ├── Blood Request
  │
  ├── Search Donors
  │
  └── Location / Map
         │
         ▼
      SQLite Database
         │
         ▼
  Donor / Blood Request Information
```

## 🎯 Problem Statement

Finding blood donors during emergencies can take significant time.

Traditional methods may depend on:

* Phone calls
* Personal contacts
* Social media posts
* Manual hospital coordination

Red Line provides a centralized system to improve the process of finding and coordinating potential blood donors.

## 💡 Solution

Red Line brings donor information and blood requirements into a single platform.

The system allows users to provide relevant donor and blood-request information so that potential matches can be identified more efficiently.

## 🗺️ Map Integration

One of the main concepts of Red Line is **location-based donor discovery**.

The map functionality can help visualize donor locations and assist users in identifying potential donors or healthcare facilities that are geographically closer to the requirement.

## 🗄️ Database

The project uses **SQLite databases** for local data storage.

Database files in the repository include:

```text
blood_donations.db
blood_requests.db
database.db
default.db
```

These databases support the application's donor, donation, and blood-request data.

## 🚀 How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/Kiruthikeyan-S/Red-line-project.git
```

### 2. Navigate to the project

```bash
cd Red-line-project
```

### 3. Install dependencies

If a `requirements.txt` file is available:

```bash
pip install -r requirements.txt
```

Otherwise, install the required Python packages used by `app.py`.

### 4. Run the Flask application

```bash
python app.py
```

### 5. Open the application

Open the local Flask address shown in the terminal.

## 🎨 User Interface

The project includes:

* Web pages built with HTML
* CSS styling
* Static images
* Interactive web components
* Donor and blood-request interfaces

The UI is designed to make the blood donation process easier to understand and use.

## 🔐 Future Improvements

The project can be further improved by adding:

* User authentication and authorization
* OTP verification
* Real-time donor availability
* Blood-group matching algorithm
* Hospital verification
* Real-time notifications
* SMS / email alerts
* Advanced map and distance calculation
* Admin dashboard
* Cloud database
* REST API
* Mobile application
* Secure deployment

## 🌍 Social Impact

Red Line is designed to support faster blood-donation coordination.

By making donor information and blood requirements easier to connect, the platform has the potential to reduce the time required to find suitable donors during emergencies.

## 👨‍💻 Author

**Kiruthikeyan S**

B.Tech – Artificial Intelligence & Data Science

## 📄 License

This project is created for educational and demonstration purposes.
