import pandas as pd


def resample_signals(df: pd.DataFrame) -> pd.DataFrame:
    """Return df on a regular 10 Hz grid (see exercise.md)."""
    raise NotImplementedError


def find_braking_events(df: pd.DataFrame, min_duration_s: float = 0.5) -> pd.DataFrame:
    """Return one row per braking event (see exercise.md)."""
    raise NotImplementedError


if __name__ == "__main__":
    raw = pd.read_csv("drive.csv")
    print(find_braking_events(resample_signals(raw)))
