# DJANGO API TEMPLATE
## AUTHOR: 
[WilAzDev](https://github.com/WilAzDev)
## DATE:
NOT PUBLISHED
## DESCRIPTION: 
A simple Django API template for building RESTful APIs.
## VERSION: 1.0.0
## INCLUDES:
- **authentication app** for user authentication
- **authorization app** for user authorization

## GETTING STARTED
### Prerequisites
- Python 3.12+
### Installation
1. Clone the repository: 
```bash
git clone https://github.com/WilAzDev/django-api
```
2. Create a new virtual environment:
```bash
python -m venv venv
```
3. Install the required packages:
```bash
pip install -r requirements.txt
```
4. Copy the .env.example doc:
- Microsoft :
```bash
copy .env.example .env
```
- Linux/Mac :
```bash
cp .env.example .env
```
5. Update the .env file with your database credentials
6. Run the command to create a secret key:
```bash
python manage.py generate_secret_key
```
7. (optional) if you want to use a differente db engine instead of sqlite, you may:
- for PostgreSQL
```bash 
pip install psycopg2-binary
``` 
- for MySQL 
```bash
pip install mysqlclient
```
- **Note**: You'll need to uncomment the corresponding database settings in the settings.py file.
- **Note**: You'll need to change your database settings in the .env file accordingly
8. Run the migrations:
```bash
python manage.py migrate
```
### Running the API
1. Run the development server:
```bash
python manage.py runserver
```
2. Access the API at [apir_url](`http://localhost:8000`)
### Testing the API
1. Run the tests:
```bash
python manage.py test -v 0
```
