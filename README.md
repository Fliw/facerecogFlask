
# Flask Face Recognition App Setup Guide

This guide will help you set up the Flask Face Recognition application from start to finish.

---

## **1. Clone the Repository**
Download or clone the project to your local machine:
```bash
git clone https://github.com/Fliw/facerecogFlask
cd facerecogFlask
```

---

## **2. Create a Virtual Environment**
Set up a Python virtual environment for the project:
```bash
python3 -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate   # For Windows
```

---

## **3. Install Dependencies**
Install all the required Python packages:
```bash
pip install -r requirements.txt
```

---

## **4. Configure Environment Variables**
Create a `.env` file in the root directory of the project and add the following configurations:
```
MYSQL_HOST=localhost
MYSQL_USER=xxx
MYSQL_PASSWORD=xxx
MYSQL_DB=xxx
MYSQL_PORT=3306
MYSQL_UNIX_SOCKET=xxxx
```

---

## **5. Set Up the Database**
Ensure that MySQL is running and create the required database:
1. Log into MySQL:
   ```bash
   mysql -u root -p
   ```
2. Create the database:
   ```sql
   CREATE DATABASE facerecogDB;
   ```

3. Grant privileges to the database user (if necessary):
   ```sql
   GRANT ALL PRIVILEGES ON facerecogDB.* TO 'root'@'localhost';
   FLUSH PRIVILEGES;
   ```

4. (Optional) Verify the database exists:
   ```sql
   SHOW DATABASES;
   ```

5. Don't Forget to Import the DB from facerecogDB.sql

---

## **6. Run the Application**
Start the Flask development server:
```bash
python app.py
```

The server will start at `http://127.0.0.1:5000`.

---

## **7. Test Database Connection**
Visit the `/test_db` endpoint to verify the database connection:
```
http://127.0.0.1:5000/test_db
```

You should see a JSON response with a list of available databases.

---

## **8. Use the Application**
Use the application for:
- User registration (e.g., `/register`)
- Face recognition endpoints

---

## **Troubleshooting**
If you encounter errors:
1. Check the `.env` file for correct configurations.
2. Ensure MySQL is running:
   ```bash
   sudo /opt/lampp/lampp startmysql
   ```
3. Check for missing dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Review the logs in the console for detailed error messages.

---
