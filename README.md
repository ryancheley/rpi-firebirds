# rpi-cvfirebirds

Scrolls the start time of any Coachella Valley Firebirds (AHL) game scheduled for today across a Raspberry Pi [Sense HAT](https://www.raspberrypi.com/products/sense-hat/) LED matrix.

## Requirements

- A Raspberry Pi with a Sense HAT attached. The `sense-hat` dependency installs only on Linux; running elsewhere will fail at `SenseHat()`.

## Raspberry Pi setup

`RTIMU` (the Sense HAT's IMU library) is not on PyPI — it only ships as a Raspberry Pi OS apt package. The virtualenv therefore has to see system site-packages:

```bash
sudo apt install sense-hat          # installs RTIMULib + RTIMU bindings
uv venv --system-site-packages      # venv that can see apt's RTIMU
uv sync                             # install httpx2 + sense-hat
```

## Run

```bash
uv run program.py
```

For each of today's games involving the Firebirds (team ID 445), it scrolls:

```
The <visitor> will be playing the <home team> at <local start time>
```

Times are converted from the game's timezone to the Pi's local timezone.

## Data sources

- Schedule and team names: `ahl.ryancheley.com`
- Game metadata (start time, timezone): HockeyTech `lscluster.hockeytech.com`
