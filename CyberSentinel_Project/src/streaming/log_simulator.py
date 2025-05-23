# Real-time log generator
# streaming/log_simulator.py

import time
import random
import json


def simulate_log_entry():
    return {
        "src_ip": f"192.168.0.{random.randint(1, 254)}",
        "dst_ip": f"10.0.0.{random.randint(1, 254)}",
        "bytes_sent": random.randint(100, 10000),
        "protocol": random.choice(["TCP", "UDP"]),
        "event_type": random.choice(["access", "login", "upload", "scan"]),
        "timestamp": time.time(),
    }


def stream_logs(callback, interval=1):
    while True:
        log = simulate_log_entry()
        callback(log)
        time.sleep(interval)


if __name__ == "__main__":

    def print_log(log):
        print(json.dumps(log, indent=2))

    stream_logs(print_log)
