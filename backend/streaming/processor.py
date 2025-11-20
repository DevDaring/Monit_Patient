"""Stream processing logic for patient vitals."""
from typing import Dict, Any
from backend.services.patient_service import PatientService
from backend.services.alert_service import AlertService
from backend.services.agent_service import AgentService
from backend.core.database import db
from loguru import logger


class VitalsProcessor:
    """Processor for incoming vital signs data."""

    def __init__(self):
        """Initialize processor."""
        self.patient_service = PatientService()
        self.alert_service = AlertService()
        self.agent_service = AgentService()

        # Thresholds for alerts
        self.thresholds = {
            'heart_rate': {'min': 50, 'max': 120},
            'bp_systolic': {'min': 90, 'max': 180},
            'bp_diastolic': {'min': 60, 'max': 110},
            'o2_saturation': {'min': 92, 'max': 100},
            'temperature': {'min': 36.0, 'max': 38.5}
        }

    async def process_vitals(self, vitals_data: Dict[str, Any]):
        """
        Process incoming vital signs.

        Steps:
        1. Store vitals in database
        2. Check for anomalies
        3. Trigger alerts if needed
        4. Invoke agent system for critical cases
        """
        try:
            patient_id = vitals_data.get('patient_id')
            if not patient_id:
                logger.warning("Vitals data missing patient_id")
                return

            # 1. Store vitals
            self.patient_service.add_vital_signs(vitals_data)

            # 2. Check for anomalies
            anomalies = self._detect_anomalies(vitals_data)

            if anomalies:
                logger.warning(f"Anomalies detected for patient {patient_id}: {anomalies}")

                # 3. Calculate risk score
                risk_data = self.patient_service.calculate_risk_score(patient_id)
                risk_level = risk_data.get('risk_level', 'unknown')

                # 4. Create alert if risk is medium or higher
                if risk_level in ['medium', 'high', 'critical']:
                    await self.alert_service.create_alert(
                        patient_id=patient_id,
                        alert_type="vitals_anomaly",
                        severity=risk_level,
                        message=f"Vital signs anomalies detected: {', '.join(anomalies)}",
                        details={
                            "anomalies": anomalies,
                            "risk_score": risk_data.get('risk_score', 0),
                            "vitals": vitals_data
                        }
                    )

                    # 5. Invoke agent system for critical cases
                    if risk_level in ['high', 'critical']:
                        await self._invoke_agent_analysis(patient_id, vitals_data, anomalies)

        except Exception as e:
            logger.error(f"Error processing vitals: {e}")

    def _detect_anomalies(self, vitals_data: Dict[str, Any]) -> list:
        """Detect anomalies in vital signs."""
        anomalies = []

        for vital, thresholds in self.thresholds.items():
            value = vitals_data.get(vital)
            if value is not None:
                if value < thresholds['min']:
                    anomalies.append(f"{vital} too low ({value})")
                elif value > thresholds['max']:
                    anomalies.append(f"{vital} too high ({value})")

        return anomalies

    async def _invoke_agent_analysis(
        self,
        patient_id: str,
        vitals_data: Dict[str, Any],
        anomalies: list
    ):
        """Invoke agent system for detailed analysis."""
        try:
            query = f"""
Urgent analysis needed for patient {patient_id}.

Detected anomalies: {', '.join(anomalies)}

Latest vital signs:
- Heart Rate: {vitals_data.get('heart_rate')} bpm
- Blood Pressure: {vitals_data.get('bp_systolic')}/{vitals_data.get('bp_diastolic')} mmHg
- O2 Saturation: {vitals_data.get('o2_saturation')}%
- Temperature: {vitals_data.get('temperature')}°C

Please provide:
1. Risk assessment
2. Possible causes
3. Recommended interventions
4. Urgency level
"""

            context = {
                "patient_id": patient_id,
                "vitals": vitals_data,
                "anomalies": anomalies
            }

            # Process through agent system
            result = await self.agent_service.process_query(query, context)

            logger.info(f"Agent analysis completed for patient {patient_id}")

            # Store agent findings in database for review
            db.append_row("agents/agent_performance_logs.csv", {
                "patient_id": patient_id,
                "query": query,
                "result": str(result),
                "timestamp": vitals_data.get('timestamp')
            })

        except Exception as e:
            logger.error(f"Error invoking agent analysis: {e}")
