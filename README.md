# Database Final Project - Backend API Server with mysql 
## Environment

Ubuntu 22.04
mysql  Ver 8.0.37-0ubuntu0.23.10.2 for Linux on aarch64 ((Ubuntu))
Please ensure you have MySQL before starting the following step.
Remember to fill in your information in .env file.

## Step
1. Create database.
    *  `sudo mysql -u root -p`
    *  `CREATE DATABASE {{ your_db_name }};`
    *  `SET global local_infile=true;`
    *  `SHOW global variables LIKE 'local_infile';`
    *  `\q`
2. Create tables and load data.
    * `sudo mysql --local_infile=1 -u root -p {{ your_db_name }} < create_table.sql`
3. Download flask
    * `sudo apt update`
    * `sudo apt install python3-flask`
4. Check whether flask is downloaded
    * `python3 -m flask --version`
5. Run app by  
    *  `python3 app.py`
    or
    * `export FLASK_APP=app.py` then `flask run `

The app will be run on http://127.0.0.1:5000 by default.

## Application Introduction
The application allows users to organize and browse Steam games through a structured grouping system, offering personalized game recommendations, user reviews, and ratings. It enables users to join chat rooms in different groups for real-time conversations. The system uses database management to efficiently handle game information, user interactions, and recommendations.
