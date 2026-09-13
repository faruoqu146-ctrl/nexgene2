def test_project_contracts():
    from app.main import app
    paths = {route.path for route in app.routes}
    assert "/api/v1/health" in paths
    assert "/api/v1/checkins/morning" in paths
    assert "/api/v1/checkins/evening" in paths
    assert "/api/v1/checkins/insights" in paths
    assert "/api/v1/timeline" in paths


def test_insight_engine():
    from types import SimpleNamespace
    from app.services.daily import build_insights

    rows = []
    for value in [5.0, 5.0, 5.0, 8.0]:
        rows.append((
            SimpleNamespace(
                numeric_value=value,
                text_value=None,
                boolean_value=None,
            ),
            SimpleNamespace(code="sleep_duration"),
        ))

    result = build_insights(rows)
    assert result
    assert result[0]["code"] == "sleep_duration_trend"
