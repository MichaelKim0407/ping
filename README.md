# Ping

Simple Python script to monitor output of `ping`.

Author: Michael Kim <mkim0407@gmail.com>

## Requirements

1. Linux or Mac

    If I remember correctly,
    `ping` on Windows behaves differently.
    It stops after four packets.
    This script is intended to accept indefinite `ping` output.

2. Python >= 3.5

    Type hints are used.
    Tested only with python 3.6.

## Usage

1. Clone this repo

2. Create and activate virtual environment

3. Install dependencies

    ```bash
    pipenv install
    ```

4. Run `ping`

    ```bash
    ping google.com | python ping.py
    ```

    Or `ping` your desired host.

5. Monitor output

    All log files are tab separated:

    * `raw.log`: Raw `ping` output with timestamps
    * `ping.log`: Timestamp, seq id and ping time. `-1` for timeout.
    * `timeout.log`: Timestamp and seq id.
    * `unknown.log`: Anything that does not match the standard patterns.
