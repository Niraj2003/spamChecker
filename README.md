# Project Setup and API Documentation

## Prerequisites
Before starting, ensure you have the following installed on your machine:
- **Python 3.x**: Ensure you have the latest version of Python 3 installed.
- **pip**: Python package installer.
- **virtualenv**: For creating isolated Python environments.

## Step-by-Step Setup Instructions

### 1. Unzip the Project Folder
Unzip the provided folder to a convenient location on your local machine.

### 2. Create and Activate a Virtual Environment
Open a terminal or command prompt and navigate to the project directory. Then, create and activate a virtual environment with the following commands:

**For Windows:**
```sh
cd path\to\unzipped\folder
python -m venv venv
venv\Scripts\activate
```

For macOS and Linux:

```sh
cd path/to/unzipped/folder
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Project Dependencies
Once the virtual environment is activated, install the required dependencies using pip:

```sh
pip install -r requirements.txt
```

### 4. Configure the Database
Run the following commands to set up the database and apply migrations:

```sh
python manage.py makemigrations
python manage.py migrate
```

### 5. Populate the Database with Sample Data
You can populate the database with sample data using the custom management command provided:

``` sh
python manage.py populate_contacts
```

### 6. Run the Development Server
Start the Django development server:

```sh
python manage.py runserver
```

Open your web browser and navigate to http://127.0.0.1:8000 to ensure the server is running.

# API Endpoints Documentation

## User Registration
**Endpoint:** `/api/register/` <br>
**Method:** `POST` <br>
**Request:**
```json
{
    "name": "Niraj",
    "phone_number": "9960641238",
    "email": "nirajamr03@gmail.com",
    "password": "password"
}
```
**Response:**
```json
{
    "name": "Niraj",
    "phone_number": "9960641238",
    "email": "nirajamr03@gmail.com",
}
```

## User Login
**Endpoint:** `/api/login/` <br>
**Method:** `POST` <br>
**Request:**
```json
{
    "phone_number": "9960641238",
    "password": "password"
}
```
**Response:**
```json
{
    "name": "Niraj",
    "phone_number": "9960641238",
    "email": "nirajamr03@gmail.com",
}
```

## Mark Spam
**Endpoint:** `/api/spam/` <br>
**Method:** `POST` <br>
**Authentication**: Yes <br>
**Request:**
```json
{
    "phone_number": "4895631786"
}
```
**Response:**
```json
{
    "phone_number": "4895631786",
    "spam_count": 1
}
```

## Search Contacts
**Endpoint:** `/api/search/type=<type>&query<query>` <br>
**Authentication:** Yes  
**Method:** `GET` <br>
**Parameters:**

| Key   | Value                  | Examples             |
|-------|------------------------|----------------------|
| type  | `name` or `phone_number`| "name" or "phone_number" |
| query | `search_term`          | "Nir" or "99"         |


