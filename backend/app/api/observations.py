from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.db.database import get_db
from app.db.models import Observation, ObservationType
from app.schemas import ObservationCreate, ObservationResponse

router = APIRouter(prefix="/api/v1/observations", tags=["observations"])


def serialize(o, t):
    return ObservationResponse(
        id=o.id,
        observation_type=t.code,
        numeric_value=o.numeric_value,
        text_value=o.text_value,
        boolean_value=o.boolean_value,
        recorded_at=o.recorded_at,
    )


@router.post("", response_model=ObservationResponse, status_code=201)
def create_observation(
    payload: ObservationCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if sum(
        v is not None
        for v in (payload.numeric_value, payload.text_value, payload.boolean_value)
    ) != 1:
        raise HTTPException(
            status_code=422,
            detail="Exactly one observation value is required",
        )
    observation_type = (
        db.query(ObservationType)
        .filter(ObservationType.code == payload.observation_type)
        .first()
    )
    if not observation_type:
        raise HTTPException(status_code=400, detail="Unknown observation type")

    observation = Observation(
        user_id=current_user.id,
        observation_type_id=observation_type.id,
        numeric_value=payload.numeric_value,
        text_value=payload.text_value,
        boolean_value=payload.boolean_value,
        recorded_at=payload.recorded_at,
    )
    db.add(observation)
    db.commit()
    db.refresh(observation)
    return serialize(observation, observation_type)


@router.get("", response_model=list[ObservationResponse])
def list_observations(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(Observation, ObservationType)
        .join(ObservationType, Observation.observation_type_id == ObservationType.id)
        .filter(Observation.user_id == current_user.id)
        .order_by(Observation.recorded_at.desc())
        .all()
    )
    return [serialize(o, t) for o, t in rows]
