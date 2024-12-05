# OpenAPI generated server

## Overview
FLASK server generated using Open API generator based on the specs. Uses PostgreSQL as a db for actual data.

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
The entire dashboard settings file with PromQL can be found in ./grafana/provisioning/dashboards/grafana-dashboard.json

1. REQUEST_COUNT, PromQL: sum by (method, endpoint, http_status) (rate(request_count_total[1m]))
2. REQUEST_LATENCY, PromQL: histogram_quantile(0.95, sum(rate(request_latency_seconds_bucket[5m])) by (le, method, endpoint))
3. STATUS_CODE_COUNT, PromQL: sum by (status_code) (rate(status_code_count_total[1m]))
4. CPU_USAGE
5. MEMORY_USAGE

## Description

Uses prometheus-client within the flask app to track all the metrics.
Uses pull model and gets the data from ../metrics endpoint automatically (described in prometheus.yml file). Metrics are being pulled from python-server:8080 (in the basic case: localhost/8080).

Uses prometheus server in a docker container to gather and store all the
metrics

Uses grafana in a container to display the data from prometheus server.
Grafana dashboard is defined in grafana-dashboard.json file and includes
5 graphs.

Grafana is automatically set up with configuration files while using

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

![изображение](https://github.com/user-attachments/assets/0be58030-b8f9-4277-8d41-e02b1310775e)

PromQL examples:
```PromQL
rate(request_count_total[1m])
sum by (method, endpoint, http_status) (rate(request_count_total[1m]))
sum by (status_code) (rate(status_code_count_total[1m]))
histogram_quantile(0.95, sum(rate(request_latency_seconds_bucket[5m])) by (le, method, endpoint))
```

# Logging

## Description

Implements logs using files with promtail + Grafana Loki.

Logs are saved to a docker volume shared wiith a promtail server in
another container. Promtail pushes logs to the Loki server instance.
After that Grafana provides dashboards over those logs in Loki.

.env file is used to configure external ports
promtail-config.yml is used to configure promtail, including push link:
```
http://loki:3100/loki/api/v1/push 
```
loki-config.yml is used to configure loki.

Grafana and Loki are automatically set up with configuration files while using

```sh
docker compose up --build
```

## Access

Loki:

```
http://localhost:3100
```

Promtail metrics:
```
http://localhost:9080
```

## Image

Additional dashboards can be created to allow search for specific log instances or categories.
LogQL is used to provide certain queries. 

For example (can be found in ./grafana/provisioning/dashboards/loki-dashboard.json):
```LogQL
"{job=\"varlogs\"} |= `DELETE` |= \"DEBUG\" | logfmt --strict"
```

![изображение](https://github.com/user-attachments/assets/e6837d8b-2260-4f9b-b52e-ff5f779857b5)

# Traces

Traces are managed using Grafana Tempo and are sent to it's instance using OpenTelemetry. Spans are created to showcase the time it takes to complete different parts of a request.

## Access

Tempo is running using gRPC, it's port is 4317 to push data using gRPC. Pushing using HTTP is also available, though not used. The port is 4318.

To retrieve data from Tempo
```
http://localhost:3200
```

## Image

Dashboards are provided to anylize traces:

![image](https://github.com/user-attachments/assets/57d99cba-2f5b-40ef-8833-1ab898a6847a)

TraceQL examples:
```TraceQL
{traceDuration > 4ms} | count() > 3
{resource.service.name="articles-api" && duration>10ms}
```

Here is an example of a trace:

![изображение](https://github.com/user-attachments/assets/c6fa26ec-02cd-4134-878f-f4430117c537)

# CI/CD

Created 3 CI/CD workflows:
1. Test the API
2. Push image to dockerhub
3. Deploy (an imitation)

