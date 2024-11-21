# OpenAPI generated server

## Overview
FLASK server generated using Open API generator based on the specs.

## Requirements
Python 3.5.2+

## Usage
To run the server, please execute the following from the root directory:

```
pip3 install -r requirements.txt
python3 -m openapi_server
```

and open your browser to see swagger ui:

```
http://localhost:8080/ui/
```

## Running with Docker

To run the server on a Docker container, please execute the following from the root directory:

```bash
# building the image
docker build -t openapi_server .

# starting up a container
docker run -p 8080:8080 openapi_server
```
# Swagger examples

![изображение](https://github.com/user-attachments/assets/5d5466e4-816b-47d0-8ab9-68b1fee8b9e6)

![изображение](https://github.com/user-attachments/assets/12240a6c-5bd3-436f-8e71-0b5bd4e21bc3)

Testing the request:
![изображение](https://github.com/user-attachments/assets/3933f54f-3a20-443e-a744-809bffec469a)

![изображение](https://github.com/user-attachments/assets/971d8989-42d1-4a4c-9110-e89a7ffe6fd0)

Testing the request:
![изображение](https://github.com/user-attachments/assets/64fce825-e2db-4511-a5fe-1e132abd9a3b)


