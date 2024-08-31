# ThreeCuriousCoders
Travel Veda Web Application developed for Hackera 2024 at Sanjay Ghodawat University, Kolhapur
# Travel Veda: Dynamic Travel Itinerary Planner

## Overview
Travel Veda is a web application designed to help users plan their travel itineraries dynamically, based on preferences, budget, and real-time data. This guide provides step-by-step instructions to set up the project on your local machine.

## Prerequisites
Before you begin, ensure you have the following installed:
- **Python 3.8+**
- **MySQL Server**
- **pip** (Python package installer)
- **Git** (for version control)
- **Google Maps API Key**

## Setup Instructions

### 1. Clone the Repository
First, clone the repository to your local machine using Git.

```bash
git clone https://github.com/yourusername/travel-veda.git
cd travel-veda
# Create a virtual environment
python3 -m venv venv

### 2. Activate the virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

### 3. Install Required Dependencies
       Install all necessary Python packages listed in requirements.txt
pip install -r requirements.txt

### 4. Setup MySQL Database
Start your MySQL server.
Create a new database called travelveda.
Import the SQL script provided in the database/ directory to set up the database schema.

# Log in to MySQL (replace 'root' and 'password' with your MySQL credentials)
mysql -u root -p

# Create the database
CREATE DATABASE travelveda;

# Exit MySQL
exit

# Import the schema
mysql -u root -p travelveda < database/travelveda_schema.sql


### 5. Update Configuration Files
Rename the .env.example file to .env.
Open the .env file and configure the following environment variables:

FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your_secret_key
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=travelveda
GOOGLE_MAPS_API_KEY=your_google_maps_api_key


### 6. Run Database Migrations (if any)
Ensure your database is up to date.
flask db upgrade
### 7. Start the Flask Development Server
Run the Flask development server to start the application.
flask run
### 8. Access the Application
Open your web browser and go to:
http://127.0.0.1:5000
### 9.Explore the Application
Sign Up: Create a new account.
Log In: Log in with your credentials.
Dashboard: Access the main dashboard where you can create and manage your itineraries.
Map Integration: View your itinerary on a map using Google Maps.
Expense Tracking: Keep track of your travel expenses.
Social Sharing: Share your travel plans with others.
### Additional Notes
If you encounter any issues, ensure that all dependencies are installed and that the MySQL server is running correctly.
The project uses mysql.connector for database interactions, and all configuration is done through the .env file.
The app is designed for a local development environment. For production deployment, additional configurations may be required.

### License
This project is licensed under the MIT License. See the LICENSE file for more details.


Make sure to replace placeholder values like `yourusername`, `your_secret_key`, `your_mysql_password`, and `your_google_maps_api_key` with the actual values used in your project. Once you've added this to your `README.md`, it will provide a clear and detailed setup guide for anyone wanting to run your Travel Itinerary Web App.
