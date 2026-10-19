
import pandas as pd
import pytest

from solution import resample_signals, find_braking_events


def test_resample_interpolates_speed_and_preserves_brake_state():
    raw = pd.DataFrame({
        "timestamp_s": [0.0, 0.15, 0.3],
        "speed_kmh": [50.0, None, 20.0],
        "brake_pressed": [0, 1, 1],
    })

    result = resample_signals(raw)

    assert list(result.index) == [0.0, 0.1, 0.2, 0.3]

    # Missing speed and intermediate grid values are interpolated.
    assert result.loc[0.1, "speed_kmh"] == pytest.approx(40.0)
    assert result.loc[0.2, "speed_kmh"] == pytest.approx(30.0)

    # Brake states use the last known value, never interpolation.
    assert result["brake_pressed"].tolist() == [0, 0, 1, 1]



def test_short_braking_event_is_ignored():
    df = pd.DataFrame({
        "speed_kmh": [50, 48, 45, 44, 43],
        "brake_pressed": [0, 1, 1, 0, 0],
    }, index=[0.0, 0.1, 0.2, 0.3, 0.4])

    result = find_braking_events(df)

    assert result.empty
    assert list(result.columns) == [
        "start_s", "end_s", "duration_s", "speed_drop_kmh"
    ]


def test_valid_braking_event():
    df = pd.DataFrame({
        "speed_kmh": [60, 55, 50, 45, 40, 35, 30],
        "brake_pressed": [0, 1, 1, 1, 1, 1, 0],
    }, index=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6])

    result = find_braking_events(df)

    assert len(result) == 1

    event = result.iloc[0]

    assert event["start_s"] == pytest.approx(0.1)
    assert event["end_s"] == pytest.approx(0.5)
    assert event["duration_s"] == pytest.approx(0.5)
    assert event["speed_drop_kmh"] == pytest.approx(20.0)
