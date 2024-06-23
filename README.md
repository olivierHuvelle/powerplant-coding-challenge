# Installing the application 

## Prerequisites

Make sure you have Python 3 installed on your machine. You can check your Python version using the following command:
```sh
python3 --version
```
## Installation with venv 
### Clone the repo 
git clone https://github.com/olivierHuvelle/powerplant-coding-challenge.git
cd <repository-directory>

### Create virtual environment
```sh
python3 -m venv venv
```

### Activate the venv 
On Unix system 
```sh
source venv/bin/activate
```
On windows :'(
```sh
venv\Scripts\activate
```

### Install the dependencies 
```sh
pip install -r requirements.txt
```

## Run the application with the venv 
### Activate the venv 
Confer supra 

### Run main.py 
```sh
python main.py 
```

### Go to the url localhost:8888/docs to use swagger ui :)

## Installation with docker 
### Clone the repo 
git clone https://github.com/olivierHuvelle/powerplant-coding-challenge.git
cd <repository-directory>

### Check docker installation 
```sh
 docker --version
```
install it if necessary 

### Build the image 
```sh
  docker build -t powerplant-app . # or any name you'd prefer of course 
```
### Create a container 
```sh
 docker run -d -p 8888:8888 --name powerplant-app powerplant-app
```
### check if the container is running 
```sh
docker ps
```
### Access the application 
```sh
go to http://localhost:8888/docs 
```

### run the tests 
```sh 
docker run --rm -e RUN_TESTS=true powerplant-app
```