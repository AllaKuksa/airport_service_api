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
 - Uploading images to Airplanes
 - Creating User by e-mail and password
 - Tickets validation
 - Pagination
 - Throttling
 - Permissions

### Crew List
![Crew List](https://raw.githubusercontent.com/AllaKuksa/airport_service_api/32aaa67a7c0427ac1b737d97256e89abb2fa3535/1_Crew%20List.png)

### Airport List
![Airport List](https://raw.githubusercontent.com/AllaKuksa/airport_service_api/32aaa67a7c0427ac1b737d97256e89abb2fa3535/2_Airport%20List.png)

### Route List
![Route List](https://raw.githubusercontent.com/AllaKuksa/airport_service_api/32aaa67a7c0427ac1b737d97256e89abb2fa3535/3_Route%20List.png)

### Route Details
![Route Details](https://raw.githubusercontent.com/AllaKuksa/airport_service_api/32aaa67a7c0427ac1b737d97256e89abb2fa3535/4_Route%20Details.png)

### Airplane Type List
![Airplane Type](https://raw.githubusercontent.com/AllaKuksa/airport_service_api/32aaa67a7c0427ac1b737d97256e89abb2fa3535/5_Airplane%20type%20List.png)

### Flight List
![Flight List](https://raw.githubusercontent.com/AllaKuksa/airport_service_api/32aaa67a7c0427ac1b737d97256e89abb2fa3535/6_Flight%20List.png)

### Flight Details
![Flight Details](https://raw.githubusercontent.com/AllaKuksa/airport_service_api/32aaa67a7c0427ac1b737d97256e89abb2fa3535/7_Flight%20Detail.png)

### Airplane List
![Airplane List](https://raw.githubusercontent.com/AllaKuksa/airport_service_api/32aaa67a7c0427ac1b737d97256e89abb2fa3535/8_Airplaine%20List.png)

### Order List
![Order List](https://raw.githubusercontent.com/AllaKuksa/airport_service_api/32aaa67a7c0427ac1b737d97256e89abb2fa3535/9_Order%20List.png)

### Ticket List
![Ticket List](https://raw.githubusercontent.com/AllaKuksa/airport_service_api/32aaa67a7c0427ac1b737d97256e89abb2fa3535/10_Ticket%20List.png)

### Ticket Details
![Ticket Details](https://raw.githubusercontent.com/AllaKuksa/airport_service_api/32aaa67a7c0427ac1b737d97256e89abb2fa3535/11_Ticket%20Details.png)

### Creating User
![](https://raw.githubusercontent.com/AllaKuksa/airport_service_api/32aaa67a7c0427ac1b737d97256e89abb2fa3535/12_Creating%20User.png)
