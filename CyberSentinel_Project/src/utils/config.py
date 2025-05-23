# src/utils/config.py
# Hardcoded RL config variables for now
STATE_SIZE = 2  # e.g., [number of anomalies, average score]
ACTION_SIZE = 2  # e.g., [Ignore, Escalate]
EPSILON_DECAY = 0.995
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
LOG_TOPIC = "cyber_logs"
ANOMALY_TOPIC = "cyber_anomalies"
ANOMALY_THRESHOLD = 0.1  # Adjust based on real data
