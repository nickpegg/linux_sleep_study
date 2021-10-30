#!/usr/bin/env python3

"""
Log battery capacity and power usage over time
"""

import time

from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path


def main() -> None:
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        '-i', '--interval', type=int, default=10
    )
    args = arg_parser.parse_args()

    last_chg = 0.0
    chg = 0.0
    t = time.time()
    while True:
        last_chg = chg
        last_t = t

        now = datetime.now()
        chg = get_charge_pct()
        pwr = get_power_usage()
        t = time.time()

        if last_chg != 0.0:
            chg_rate_m = (chg - last_chg) / (t - last_t) * 60
        else:
            chg_rate_m = 0.0

        print(f"{now} {chg:.2f}% {pwr:.2f}W {chg_rate_m:.4f}%/min")

        time.sleep(args.interval)


def get_charge_pct() -> float:
    chg_now = float(Path("/sys/class/power_supply/BAT1/charge_now").read_text())
    chg_full = float(Path("/sys/class/power_supply/BAT1/charge_full").read_text())
    return 100 * chg_now / chg_full


def get_power_usage() -> float:
    current = float(Path("/sys/class/power_supply/BAT1/current_now").read_text())
    voltage = float(Path("/sys/class/power_supply/BAT1/voltage_now").read_text())
    current /= 1_000_000
    voltage /= 1_000_000
    return current * voltage


if __name__ == '__main__':
    main()
