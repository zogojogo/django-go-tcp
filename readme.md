# Entry Task BE MPO

## Introduction
This project is a part of the entry task for the Backend MPO role at Sealabs Digitalent. The task is to create a simple REST API to manage products and categories. Then deploy the API using gunicorn and nginx. For the database, I use MySQL. The API is written in Python using Django framework. I also create a simple TCP server using Golang to handle authentication features.

## API Documentation
The API documentation can be found in the following link: https://documenter.getpostman.com/view/24100576/2s93RNzaSr

## How to run the Applications

### Prerequisites
- Python 2.7
- Golang 1.19
- MySQL

### Install Dependencies
- Install Python dependencies
```
pip install -r python/requirements.txt
```

- Install Golang dependencies
```
cd go && go mod tidy
```

### Run the Applications
Make sure you have Nginx installed and running. Then run the following commands:
- Apply nginx configuration
```
cd ngin && sudo chmod +x enable_config.sh
./enable_config.sh
```

- Run the TCP server
```
cd go && go run main.go
```

- Run the Django server
```
conda activate django_27
cd python && sudo chmod +x start_gunicorn.sh
./start_gunicorn.sh
```
**Note** : Don't forget to fill the configurations in the `.env` file.

## How to run the Tests
- Run the Python tests
```
cd python && coverage run --source=./entry_task -m unittest discover -v
```
**Note**: To check the coverage report, run the following command:
```
coverage report -m
```

- Run the Golang tests
```
cd go && go test -v -cover ./...
```