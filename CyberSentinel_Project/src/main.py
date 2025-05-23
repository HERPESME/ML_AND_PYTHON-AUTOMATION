import os
import sys
import time

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils.config_loader import load_config
from src.utils.logging_config import setup_logging
from src.anomaly_detection.models import detect_anomalies
from src.rl_agent.dqn_agent import DQNAgent
from src.llm_assistant.assistant import AlertAssistant
from src.streaming.kafka_processor import KafkaLogProcessor
from src.human_interface.web_interface import alert_approval_ui
from src.siem_output.formatter import format_for_siem


def main():
    # Load configuration
    config = load_config("config/config.yaml")

    # Setup logging with a proper logger name
    logger = setup_logging("CyberSentinelMain")

    logger.info("🚀 CyberSentinel system starting...")

    # Initialize components
    rl_agent = DQNAgent()
    assistant = AlertAssistant()
    kafka_processor = KafkaLogProcessor(config.get("kafka", {}))

    # Start processing logs
    for log_record in kafka_processor.consume_logs():
        logger.debug(f"📥 Received log: {log_record}")

        anomalies = detect_anomalies(log_record)
        if not anomalies:
            continue

        logger.info(f"⚠️ Anomalies detected: {anomalies}")

        # RL agent decides response action
        action = rl_agent.decide_action(anomalies)
        logger.info(f"🤖 RL Agent decision: {action}")

        # UI approval
        approved = alert_approval_ui(anomalies, action)
        if not approved:
            logger.info("❌ User rejected the alert action. Skipping.")
            continue

        # Get mitigation recommendation
        mitigation = assistant.suggest_mitigation(anomalies)
        logger.info(f"🛡️ Suggested mitigation: {mitigation}")

        # Format alert for SIEM
        formatted_alert = format_for_siem(
            {
                "anomalies": anomalies,
                "action": action,
                "mitigation": mitigation,
            }
        )
        logger.info(f"📤 Formatted alert for SIEM: {formatted_alert}")

        # Optional: Send to SIEM system here
        # send_to_siem(formatted_alert)

        time.sleep(1)  # Simulate processing delay


if __name__ == "__main__":
    main()
