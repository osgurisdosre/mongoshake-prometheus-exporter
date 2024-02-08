import time
import asyncio
import prometheus_client
from prometheus_client import Gauge, start_http_server
import aiohttp
import os

# Remove Python default measurements from registry    
prometheus_client.REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.GC_COLLECTOR)

# List of URLs to scrape
URL_LIST=os.environ["URL_LIST"].split(",")
# Scrape interval
SCRAPE_INTERVAL=int(os.environ["SCRAPE_INTERVAL"])

# Prometheus metric names
metric_prefix = "mongoshake"
prom_metrics = {
    "logs_get": Gauge(metric_prefix + "_logs_get", "Number of logs (get)",["replset", "url"]),
    "logs_repl": Gauge(metric_prefix + "_logs_repl", "Number of logs (repl)",["replset", "url"]),
    "logs_success": Gauge(metric_prefix + "_logs_success", "Number of successful logs",["replset", "url"]),
    "tps": Gauge(metric_prefix + "_tps", "Transactions per second",["replset", "url"]),
    "replication_latency": Gauge(metric_prefix + "_replication_latency", "Replication_latency in MS",["replset", "url"])
}

# Fetch url data
async def fetch_metrics(url, prom_metrics):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={"Accept": "application/json"}) as response:
            if response.status == 200:
                data = await response.json(content_type=None)
                update_prometheus_metrics(data, prom_metrics, url)
            else:
                print(f"Failed to fetch data from {url}: {response.status}")

# Print metrics in webserver 
def update_prometheus_metrics(data, prom_metrics, url):
    # Custom metrics
    data_copy = data
    lsn_ack_ts = int(data_copy["lsn_ack"]["ts"])
    lsn_ts = int(data_copy["lsn"]["ts"])
    replset = data_copy["replset"]
    replication_latency = lsn_ts - lsn_ack_ts
    data_copy["replication_latency"] = replication_latency

    # Set metrics
    for key, value in prom_metrics.items():
        value.labels(replset,url).set(data_copy[key])

async def main():
    # Start Prometheus HTTP server
    start_http_server(8000)

    # Start app
    while True:
        await asyncio.gather(*[fetch_metrics(url, prom_metrics) for url in URL_LIST])

        # Wait for 5 scrape interval
        await asyncio.sleep(SCRAPE_INTERVAL)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Received KeyboardInterrupt. Exiting.")