from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user, require_admin
from app.models.user import User
from app.models.alert import Alert
from typing import List
from datetime import datetime

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("/")
async def get_alerts(
    is_resolved: bool = None,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get alerts"""
    query = db.query(Alert)
    
    if is_resolved is not None:
        query = query.filter(Alert.is_resolved == is_resolved)
    
    alerts = query.order_by(Alert.created_at.desc()).limit(limit).all()
    return alerts

@router.patch("/{alert_id}/resolve")
async def resolve_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Resolve an alert (admin only)"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.is_resolved = True
    alert.resolved_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Alert resolved successfully"}
