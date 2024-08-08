# Airport API
API service for airport management written on DRF
___
## Installing using GitHub
Install PostgresSQL and create db

1. `git clone https://github.com/AllaKuksa/airport_service_api.git`
2. `cd airport_API`
3. `python -m venv venv`
4. `source venv/bin/activate`
5. `pip install -r requirements.txt`
6. Set the following environment variables:
   ```sh
   DB_HOST=<your db hostname>
   DB_NAME=<your db name>
   DB_USER=<your db username>
   DB_PASSWORD=<your db user password>
   SECRET_KEY=<your secret key>
7. `python manage.py makemigrations`
8. `python manage.py migrate`
9. `python manage.py runserver`
___
## Run with docker
Docker should be installed
- `docker-compose build`
- `docker-compose up`
___
## Getting access
Docker should be installed
 - `create user  /api/user/register/`
 - `get access token  /api/user/token/`
### DB Structure:
![image](https://raw.githubusercontent.com/AllaKuksa/airport_service_api/develop/airport.png)
### Features
 - JWT authenticated
 - Admin panel /admin/
 - Documentation is located at /api/schema/swagger-ui/
 - Managing orders and tickets
 - Creating Crews
 - Creating Airports
 - Creating Routes with Airports
 - Creating Airplanes with Airplanes types
 - Creating Flights with Airplanes and Routes
 - Filtering Flights, Airports, Airplanes, Tickets
 - Creating User by e-mail and password
 - Tickets validation
 - Pagination
 - Throttling
 - Permissions

Cre List
