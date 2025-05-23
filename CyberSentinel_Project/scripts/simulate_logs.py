import json
import time
import random
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


def generate_log():
    return {
        "timestamp": time.time(),
        "src_ip": f"192.168.1.{random.randint(1, 255)}",
        "dst_ip": f"10.0.0.{random.randint(1, 255)}",
        "protocol": random.choice(["TCP", "UDP"]),
        "bytes_sent": random.randint(50, 5000),
        "event_type": random.choice(["login", "scan", "file_access", "ping"]),
    }


if __name__ == "__main__":
    while True:
        log = generate_log()
        producer.send("cyber_logs", value=log)
        print(f"Sent log: {log}")
        time.sleep(1)
