"""Alert management endpoints."""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from backend.services.alert_service import AlertService
from loguru import logger

router = APIRouter(prefix="/api/alerts", tags=["alerts"])
alert_service = AlertService()


@router.get("/")
async def get_alerts(patient_id: Optional[str] = None):
    """Get active alerts, optionally filtered by patient."""
    try:
        alerts = alert_service.get_active_alerts(patient_id)
        return {"status": "success", "alerts": alerts, "count": len(alerts)}
    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: str):
    """Mark alert as acknowledged."""
    try:
        success = alert_service.acknowledge_alert(alert_id)
        if success:
            return {"status": "success", "message": f"Alert {alert_id} acknowledged"}
        else:
            raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error acknowledging alert: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{alert_id}/resolve")
async def resolve_alert(alert_id: str):
    """Mark alert as resolved."""
    try:
        success = alert_service.resolve_alert(alert_id)
        if success:
            return {"status": "success", "message": f"Alert {alert_id} resolved"}
        else:
            raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error resolving alert: {e}")
        raise HTTPException(status_code=500, detail=str(e))
