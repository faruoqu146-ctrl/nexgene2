from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.db.models import Observation, ObservationType


def record(db: Session, user_id: int, code: str, value, recorded_at):
    observation_type = (
        db.query(ObservationType)
        .filter(ObservationType.code == code)
        .first()
    )
    if not observation_type:
        raise ValueError(f"Unknown observation type: {code}")

    kwargs = {
        "user_id": user_id,
        "observation_type_id": observation_type.id,
        "recorded_at": recorded_at,
    }
    if isinstance(value, bool):
        kwargs["boolean_value"] = value
    elif isinstance(value, (int, float)):
        kwargs["numeric_value"] = float(value)
    else:
        kwargs["text_value"] = str(value)

    observation = Observation(**kwargs)
    db.add(observation)
    return observation


def checkin_time(value):
    return value or datetime.now(timezone.utc)


def build_insights(rows):
    grouped = {}
    for observation, observation_type in rows:
        value = (
            observation.numeric_value
            if observation.numeric_value is not None
            else observation.text_value
            if observation.text_value is not None
            else observation.boolean_value
        )
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            grouped.setdefault(observation_type.code, []).append(float(value))

    insights = []

    for code, title, message_template, direction, threshold in [
        (
            "sleep_duration",
            "Sleep has been trending down",
            "Your recent average sleep is {recent:.1f} hours, below your current baseline of {baseline:.1f} hours.",
            "low",
            0.5,
        ),
        (
            "stress",
            "Stress has been running higher",
            "Your recent stress score averages {recent:.1f}/10 versus a baseline of {baseline:.1f}/10.",
            "high",
            1.0,
        ),
        (
            "focus",
            "Focus has been dipping",
            "Your recent focus score averages {recent:.1f}/10 versus a baseline of {baseline:.1f}/10.",
            "low",
            1.0,
        ),
    ]:
        values = grouped.get(code, [])
        if len(values) >= 2:
            recent = sum(values[:3]) / min(3, len(values))
            baseline = sum(values) / len(values)
            changed = recent < baseline - threshold if direction == "low" else recent > baseline + threshold
            if changed:
                insights.append({
                    "code": code + "_trend",
                    "title": title,
                    "message": message_template.format(recent=recent, baseline=baseline),
                    "evidence_count": len(values),
                })

    return insights
