# OpenAPI generated server

## Overview
FLASK server generated using Open API generator based on the specs.

## Requirements
Docker

## Usage
To run the server, please execute the following from the root directory:

```
docker compose up --build
```

and open your browser to see swagger ui:

```
http://localhost:8080/ui/
```

# Swagger examples

![изображение](https://github.com/user-attachments/assets/5d5466e4-816b-47d0-8ab9-68b1fee8b9e6)

![изображение](https://github.com/user-attachments/assets/12240a6c-5bd3-436f-8e71-0b5bd4e21bc3)

Testing the request:
![изображение](https://github.com/user-attachments/assets/3933f54f-3a20-443e-a744-809bffec469a)

![изображение](https://github.com/user-attachments/assets/971d8989-42d1-4a4c-9110-e89a7ffe6fd0)

Testing the request:
![изображение](https://github.com/user-attachments/assets/64fce825-e2db-4511-a5fe-1e132abd9a3b)

# Grafana dashboard

## Metrics
1. REQUEST_COUNT, PromQL: sum by (method, endpoint, http_status) (rate(request_count_total[1m]))
2. REQUEST_LATENCY, PromQL: histogram_quantile(0.95, sum(rate(request_latency_seconds_bucket[5m])) by (le, method, endpoint))
3. STATUS_CODE_COUNT, PromQL: sum by (status_code) (rate(status_code_count_total[1m]))
4. CPU_USAGE
5. MEMORY_USAGE

## Description

Uses prometheus-client within the flask app to track all the metrics.
Metrics:

Uses prometheus server in a docker container to gather and store all the
metrics

Uses grafana in a container to display the data from prometheus server.
Grafana dashboard is defined in grafana-dashboard.json file and includes
5 graphs.

Grafana is automatically set up while using

```sh
docker compose up --build
```
## Access

Grafana:

```
http://localhost:3001
```

If you want to directly see the metrics:
```
http://localhost:8080/metrics
```

If you want to directly access Prometheus:
```
http://localhost:9090/
```

## Image

![изображение](https://github.com/user-attachments/assets/58049c60-8bd1-446b-9d39-8514a2d7cfa0)
