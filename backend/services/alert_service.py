"""Alert generation and notification service."""
from typing import Dict, Any, List, Optional
from backend.core.database import db
from backend.core.config import settings
from backend.services.streaming_service import StreamingService
from loguru import logger
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import uuid


class AlertService:
    """Service for generating and managing alerts."""

    def __init__(self):
        """Initialize alert service."""
        self.alerts_file = "alerts/alert_history.csv"
        self.streaming_service = StreamingService()

    async def create_alert(
        self,
        patient_id: str,
        alert_type: str,
        severity: str,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create and distribute an alert.

        Args:
            patient_id: Patient ID
            alert_type: Type of alert (vitals, deterioration, etc.)
            severity: Severity level (low, medium, high, critical)
            message: Alert message
            details: Additional alert details

        Returns:
            Created alert data
        """
        try:
            alert_id = str(uuid.uuid4())
            timestamp = datetime.utcnow().isoformat()

            alert_data = {
                "alert_id": alert_id,
                "patient_id": patient_id,
                "alert_type": alert_type,
                "severity": severity,
                "message": message,
                "details": details or {},
                "timestamp": timestamp,
                "status": "active"
            }

            # Save to CSV
            db.append_row(self.alerts_file, {
                "alert_id": alert_id,
                "patient_id": patient_id,
                "alert_type": alert_type,
                "severity": severity,
                "message": message,
                "timestamp": timestamp,
                "status": "active"
            })

            # Publish to Kafka
            if settings.ENABLE_REAL_TIME_STREAMING:
                await self.streaming_service.produce_alert(alert_data)

            # Send email if critical
            if severity in ['high', 'critical'] and settings.ENABLE_EMAIL_ALERTS:
                await self.send_email_alert(alert_data)

            logger.info(f"Alert created: {alert_id} for patient {patient_id}")

            return alert_data

        except Exception as e:
            logger.error(f"Error creating alert: {e}")
            raise

    async def send_email_alert(self, alert_data: Dict[str, Any]):
        """Send email notification for alert."""
        try:
            # Get patient info to find assigned doctor
            patient_id = alert_data['patient_id']

            # Create email
            message = MIMEMultipart()
            message['From'] = settings.ALERT_EMAIL_FROM
            message['To'] = settings.SMTP_USERNAME  # In production, get doctor's email from patient record
            message['Subject'] = f"[{alert_data['severity'].upper()}] Patient Alert: {patient_id}"

            body = f"""
PATIENT ALERT - Monit Patient System

Alert ID: {alert_data['alert_id']}
Patient ID: {alert_data['patient_id']}
Severity: {alert_data['severity'].upper()}
Type: {alert_data['alert_type']}
Time: {alert_data['timestamp']}

Message:
{alert_data['message']}

Details:
{alert_data.get('details', {})}

Please review the patient immediately.

---
Monit Patient System
"Predict the future where uncertainty is the enemy"
"""

            message.attach(MIMEText(body, 'plain'))

            # Send email
            await aiosmtplib.send(
                message,
                hostname=settings.SMTP_SERVER,
                port=settings.SMTP_PORT,
                username=settings.SMTP_USERNAME,
                password=settings.SMTP_PASSWORD,
                start_tls=True
            )

            logger.info(f"Email sent for alert {alert_data['alert_id']}")

        except Exception as e:
            logger.error(f"Error sending email alert: {e}")
            # Don't raise - email failure shouldn't break alert creation

    def get_active_alerts(self, patient_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get active alerts, optionally filtered by patient."""
        try:
            alerts_df = db.read_csv(self.alerts_file)
            if alerts_df.empty:
                return []

            # Filter active alerts
            if 'status' in alerts_df.columns:
                alerts_df = alerts_df[alerts_df['status'] == 'active']

            # Filter by patient if specified
            if patient_id and 'patient_id' in alerts_df.columns:
                alerts_df = alerts_df[alerts_df['patient_id'] == patient_id]

            # Sort by timestamp (most recent first)
            if 'timestamp' in alerts_df.columns:
                alerts_df = alerts_df.sort_values('timestamp', ascending=False)

            return alerts_df.to_dict('records')

        except Exception as e:
            logger.error(f"Error getting active alerts: {e}")
            return []

    def acknowledge_alert(self, alert_id: str) -> bool:
        """Mark alert as acknowledged."""
        try:
            return db.update_row(
                self.alerts_file,
                alert_id,
                'alert_id',
                {'status': 'acknowledged'}
            )
        except Exception as e:
            logger.error(f"Error acknowledging alert {alert_id}: {e}")
            return False

    def resolve_alert(self, alert_id: str) -> bool:
        """Mark alert as resolved."""
        try:
            return db.update_row(
                self.alerts_file,
                alert_id,
                'alert_id',
                {'status': 'resolved'}
            )
        except Exception as e:
            logger.error(f"Error resolving alert {alert_id}: {e}")
            return False
