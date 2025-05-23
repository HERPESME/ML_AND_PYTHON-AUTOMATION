class AlertAssistant:
    """
    LLM-based incident triage assistant with stubbed RAG-like behavior.
    """

    def __init__(self):
        pass  # Normally setup for LLM API key or config

    def suggest_mitigation(self, anomalies):
        recommendations = []
        for anomaly in anomalies:
            log = anomaly.get("log", "Unknown anomaly")
            recommendation = (
                f"Review the following log for threats: '{log[:50]}...'. "
                f"Recommended action: investigate IP or block as needed."
            )
            recommendations.append(recommendation)
        return recommendations
