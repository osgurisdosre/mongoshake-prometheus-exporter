# MongoShake Prometheus Exporter

The MongoShake Prometheus Exporter is a Python application designed to collect metrics from MongoShake and export them to Prometheus. This application is ideal for use in a Docker container environment.

## Requirements

Make sure you have the following requirements before running the application:

- Python 3.x installed
- Docker installed

## Metrics

The following metrics are exported:

- `logs_get`: Number of logs (get)
- `logs_repl`: Number of logs (repl)
- `logs_success`: Number of successful logs
- `tps`: Transactions per second
- `replication_latency`: Replication_latency in miliseconds (ms)

### Usage

To run the MongoShake Prometheus Exporter, you can use Docker. Make sure to set two mandatory environment variables:

- `URL_LIST`: A list of URLs to be queried by the MongoShake Prometheus Exporter.
- `SCRAPE_INTERVAL`: The interval of time in which the application will query the endpoint.

#### Example Usage

```bash

docker run -p 8000:8000 -p 9100:9100 -p 9200:9200 -e SCRAPE_INTERVAL="5" -e URL_LIST="http://host.docker.internal:9100/repl,http://host.docker.internal:9200/repl" mongoshake-prometheus-exporter

curl http://localhost:8000/metrics/
# HELP mongoshake_logs_get Number of logs (get)
# TYPE mongoshake_logs_get gauge
mongoshake_logs_get{replset="mongoshake-01"",url="http://host.docker.internal:9100/repl"} 1.071287933e+09
mongoshake_logs_get{replset="mongoshake-02"",url="http://host.docker.internal:9200/repl"} 1.071282287e+09
# HELP mongoshake_logs_repl Number of logs (repl)
# TYPE mongoshake_logs_repl gauge
mongoshake_logs_repl{replset="mongoshake-01"",url="http://host.docker.internal:9100/repl"} 1.77653929e+08
mongoshake_logs_repl{replset="mongoshake-02"",url="http://host.docker.internal:9200/repl"} 1.77652651e+08
# HELP mongoshake_logs_success Number of successful logs
# TYPE mongoshake_logs_success gauge
mongoshake_logs_success{replset="mongoshake-01"",url="http://host.docker.internal:9100/repl"} 1.77653929e+08
mongoshake_logs_success{replset="mongoshake-02"",url="http://host.docker.internal:9200/repl"} 1.77652651e+08
# HELP mongoshake_tps Transactions per second
# TYPE mongoshake_tps gauge
mongoshake_tps{replset="mongoshake-01"",url="http://host.docker.internal:9100/repl"} 223.0
mongoshake_tps{replset="mongoshake-02"",url="http://host.docker.internal:9200/repl"} 286.0
# HELP mongoshake_replication_latency Replication_latency in MS
# TYPE mongoshake_replication_latency gauge
mongoshake_replication_latency{replset="mongoshake-01"",url="http://host.docker.internal:9100/repl"} 257.0
mongoshake_replication_latency{replset="mongoshake-02"",url="http://host.docker.internal:9200/repl"} 4.294966415e+09