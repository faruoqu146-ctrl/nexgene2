from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.db.database import get_db
from app.db.models import Observation, ObservationType
from app.schemas import TimelineItem

router = APIRouter(prefix="/api/v1/timeline", tags=["timeline"])


@router.get("", response_model=list[TimelineItem])
def timeline(
    current_user=Depends(get_current_user),
    db: Session=Depends(get_db),
):
    rows = (
        db.query(Observation, ObservationType)
        .join(ObservationType, Observation.observation_type_id == ObservationType.id)
        .filter(Observation.user_id == current_user.id)
        .order_by(Observation.recorded_at.desc())
        .limit(200)
        .all()
    )
    result = []
    for observation, observation_type in rows:
        value = (
            observation.numeric_value
            if observation.numeric_value is not None
            else observation.text_value
            if observation.text_value is not None
            else observation.boolean_value
        )
        result.append(
            TimelineItem(
                recorded_at=observation.recorded_at,
                observation_type=observation_type.code,
                value=value,
            )
        )
    return result
