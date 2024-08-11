# Shared_Exercise_Platform

## Backend Environment Setup

### 1. Python Environment
Ensure that Python version 3.10.12 is installed. After installing Python, navigate to the backend directory and install the required libraries listed in `requirements.txt`. The Django installation can be done as follows:

```sh
pip install django
pip install djangorestframework
pip install djangorestframework-simplejwt
```

### 2. Aliyun API and OSS Libraries
Install the libraries required to access Aliyun API and the OSS dependencies with the specified versions:
```sh
pip install aliyun-python-sdk-core==2.13.10
pip install aliyun-python-sdk-green==3.6.6
pip install oss2
```

### 3. Install Redis
To install Redis, run the following command:
```sh
sudo apt install redis-server
```

### 4. Install MySQL
To install MySQL, run the following commands:
```sh
sudo apt install mysql-server
sudo apt install mysql-client
pip install django-redis
```

### 5. MySQL Configuration
After installing MySQL, enable password authentication and create the database `test`:
```sh
sudo mysql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'mysql123';
FLUSH PRIVILEGES;
mysql -u root -p  # Password is 'mysql123'
CREATE DATABASE test;
```

### 6. Start Redis Service
Start the Redis service process with:
```sh
sudo systemctl start redis-server
```

### 7. Initialize Database and Start Server
Execute the following commands to initialize the database and start the server, listening on the local IPv6 port 80:
```sh
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

### 8. Nginx Configuration
To use the backend with the frontend, configure Nginx to reverse proxy requests to `/api/v1/` to `http://[::1]:8000`. Refer to the [Nginx official documentation](https://nginx.org/en/docs/) for detailed instructions.

### Note
For enhanced security after public deployment, the backend does not enable cross-origin resource sharing (CORS) by modifying response headers. Ensure that the frontend and backend are running in the same origin to avoid access issues due to the same-origin policy enforced by browsers.