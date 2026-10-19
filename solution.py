import pandas as pd
import math


def resample_signals(df: pd.DataFrame) -> pd.DataFrame:
    """Return df on a regular 10 Hz grid (see exercise.md)."""
    raw = df.sort_values("timestamp_s").set_index("timestamp_s")

    # Create timestamps at exactly 0.1-second intervals.
    start_tick = math.ceil(raw.index.min() * 10)
    end_tick = math.floor(raw.index.max() * 10)
    grid = pd.Index(
        [tick / 10 for tick in range(start_tick, end_tick + 1)],
        name="timestamp_s",
    )

    # Keep both original timestamps and target grid timestamps.
    aligned = raw.reindex(raw.index.union(grid)).sort_index()

    # Speed changes continuously; brake state is discrete.
    aligned["speed_kmh"] = aligned["speed_kmh"].interpolate(method="index")
    aligned["brake_pressed"] = aligned["brake_pressed"].ffill()

    result = aligned.loc[grid, ["speed_kmh", "brake_pressed"]].copy()
    result["brake_pressed"] = result["brake_pressed"].astype(int)

    return result



def find_braking_events(
    df: pd.DataFrame, min_duration_s: float = 0.5
) -> pd.DataFrame:
    """Find consecutive braking periods meeting the minimum duration."""
    columns = ["start_s", "end_s", "duration_s", "speed_drop_kmh"]

    # Identify samples where the brake is pressed.
    pressed = df["brake_pressed"].eq(1)

    # Assign a group ID whenever the brake state changes.
    groups = pressed.ne(pressed.shift(fill_value=False)).cumsum()

    events = []

    # Process each consecutive braking period.
    for _, event in df[pressed].groupby(groups[pressed]):
        duration = len(event) * 0.1

        # Ignore braking periods shorter than the threshold.
        if duration < min_duration_s:
            continue

        events.append({
            "start_s": float(event.index[0]),
            "end_s": float(event.index[-1]),
            "duration_s": duration,
            "speed_drop_kmh": float(
                event["speed_kmh"].iloc[0]
                - event["speed_kmh"].iloc[-1]
            ),
        })

    return pd.DataFrame(events, columns=columns)



if __name__ == "__main__":
    raw = pd.read_csv("drive.csv")
    print(find_braking_events(resample_signals(raw)))
