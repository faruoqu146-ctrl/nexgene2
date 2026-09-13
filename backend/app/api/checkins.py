from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.db.database import get_db
from app.db.models import Observation, ObservationType
from app.schemas import EveningCheckin, Insight, MorningCheckin
from app.services.daily import build_insights, checkin_time, record

router = APIRouter(prefix="/api/v1/checkins", tags=["checkins"])


@router.post("/morning")
def morning(
    payload: MorningCheckin,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    recorded_at = checkin_time(payload.recorded_at)
    for code, value in [
        ("sleep_duration", payload.sleep_duration),
        ("sleep_quality", payload.sleep_quality),
        ("energy", payload.energy),
    ]:
        record(db, current_user.id, code, value, recorded_at)
    db.commit()
    return {
        "status": "recorded",
        "type": "morning",
        "recorded_at": recorded_at,
    }


@router.post("/evening")
def evening(
    payload: EveningCheckin,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    recorded_at = checkin_time(payload.recorded_at)
    for code, value in [
        ("mood", payload.mood),
        ("stress", payload.stress),
        ("focus", payload.focus),
    ]:
        record(db, current_user.id, code, value, recorded_at)
    if payload.activity_duration is not None:
        record(
            db,
            current_user.id,
            "activity_duration",
            payload.activity_duration,
            recorded_at,
        )
    db.commit()
    return {
        "status": "recorded",
        "type": "evening",
        "recorded_at": recorded_at,
    }


@router.get("/insights", response_model=list[Insight])
def insights(
    current_user=Depends(get_current_user),
    db: Session=Depends(get_db),
):
    rows = (
        db.query(Observation, ObservationType)
        .join(ObservationType, Observation.observation_type_id == ObservationType.id)
        .filter(Observation.user_id == current_user.id)
        .order_by(Observation.recorded_at.desc())
        .all()
    )
    return build_insights(rows)
