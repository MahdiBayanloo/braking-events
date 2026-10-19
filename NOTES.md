
# Implementation Notes

- Input timestamps are assumed to be unique and speed has valid measurements around the dropout.
- Output timestamps use 0.1-second increments within the raw recording range.
- Speed uses time-based linear interpolation; brake states use forward fill.
- Each consecutive sequence of pressed samples is one braking event.
- `start_s` is the first pressed timestamp; `end_s` is the last pressed timestamp.
- Duration is the number of pressed samples multiplied by 0.1 seconds.
- Speed drop is calculated between the first and last pressed samples.
- With more time, I would examine sensor noise and event boundary conventions.
