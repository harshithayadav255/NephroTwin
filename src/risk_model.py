
def get_monitoring_context(egfr):
    """
    Provide educational context for an eGFR value.
    This is not a diagnosis or a validated prediction model.
    """

    if egfr < 15:
        return {
            "category": "Very low eGFR",
            "message": (
                "This value needs prompt professional medical "
                "assessment. A single result cannot diagnose "
                "a condition."
            )
        }

    if egfr < 30:
        return {
            "category": "Low eGFR",
            "message": (
                "Professional assessment is important. "
                "Interpret the result with other clinical findings."
            )
        }

    if egfr < 60:
        return {
            "category": "Reduced eGFR",
            "message": (
                "Follow-up and clinical interpretation are important. "
                "One measurement alone does not establish chronic "
                "kidney disease."
            )
        }

    return {
        "category": "eGFR 60 or above",
        "message": (
            "This value alone does not rule out kidney disease. "
            "Other tests and medical history may be needed."
        )
    }
