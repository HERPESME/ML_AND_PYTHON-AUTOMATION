# src/streaming/kafka_processor.py

import json
from kafka import KafkaConsumer, KafkaProducer
from src.utils.config import (
    KAFKA_BOOTSTRAP_SERVERS,
    LOG_TOPIC,
    ANOMALY_TOPIC,
    ANOMALY_THRESHOLD,
)
from src.utils.logging_config import setup_logging
from src.anomaly_detection.models import AutoencoderModel, parse_log_line

logger = setup_logging("kafka_processor")


class KafkaLogProcessor:
    def __init__(self, kafka_config=None):
        self.topic = kafka_config.get("log_topic", LOG_TOPIC)
        self.anomaly_topic = kafka_config.get("anomaly_topic", ANOMALY_TOPIC)
        self.bootstrap_servers = kafka_config.get(
            "bootstrap_servers", KAFKA_BOOTSTRAP_SERVERS
        )

        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id="cyber_group",
        )

        self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)
        self.autoencoder = AutoencoderModel(input_dim=3)
        logger.info("✅ KafkaLogProcessor initialized.")

    def consume_logs(self):
        for msg in self.consumer:
            log_line = msg.value.decode("utf-8", errors="ignore")
            features = parse_log_line(log_line)

            if features is None:
                continue

            error = self.autoencoder.get_reconstruction_error([features])[0]

            if error > ANOMALY_THRESHOLD:
                logger.warning(
                    f"⚠️ Anomaly detected (error={error:.2f}): {log_line.strip()}"
                )

                anomaly_record = {
                    "log": log_line.strip(),
                    "features": features,
                    "reconstruction_error": float(error),
                }

                self.producer.send(
                    self.anomaly_topic, value=json.dumps(anomaly_record).encode("utf-8")
                )

                # Yield the anomaly to the rest of the pipeline
                yield anomaly_record
