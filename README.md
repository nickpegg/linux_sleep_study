# Linux Sleep Study

# The Problem

I just bought a [new laptop](https://frame.work) and in various communities
folks recommend setting the Linux kernel to do a deep sleep instead of the
default s2idle sleep. Deep sleep shuts down a lot more systems which saves a
_lot_ on power.

The issue with deep sleep though is that it takes many seconds between me
opening the laptop lid to it being useful, whereas s2idle is instantly ready.

As an engineer, my mind always thinks about tradeoffs. How much power gains am
I getting if I give up the ability to instantly use my laptop when I open the
lid?

# The Experiment

## The Machine

My laptop is a first-generation Framwork laptop.

* Framework mainboard with Intel i7-1165G7 CPU
* 16GB DDR4 3200 MHz RAM (single stick)
* Samsung 970 EVO 1TB M.2 SSD

I was running a standard system load; Firefox with a bunch of tabs open, a
bunch of terminals open for coding, etc.

## The Process

I wrote a little Python script, `battery_log.py`, which grabs battery stats
from /sys:

* Current battery charge
* Max battery charge
* Current current (in microamps)
* Current voltage (in microvolts)

Using these I calculate % battery charge remaining and Power usage (Watts). 

It also calculates the drop in % charge remaining per minute. This is only
really useful if you have the laptop asleep for a bit so that the interval
spread is pretty large.

The steps:
1. Set desired sleep mode, e.g. `echo s2idle | sudo tee /sys/power/mem_sleep`
1. Start script
1. Close laptop lid for some time (~1 hr)
1. Open laptop lid, see stats
1. Repeat with other sleep mode

# Results

## s2idle
Output:
```
$ ./battery_log.py
2021-10-30 11:45:02.648555 39.93% 4.24W 0.0000%/min
2021-10-30 11:45:12.659306 39.90% 4.12W -0.1692%/min
2021-10-30 12:40:44.638471 37.76% 1.30W -0.0386%/min
2021-10-30 12:40:54.649212 37.70% 4.63W -0.3385%/min
^C

$ cat /sys/power/mem_sleep
[s2idle] deep
```

0.0386%/min or 2.3%/hr over about 55 minutes

100% / (%/hr rate) = 43.18 hours in sleep from a full charge

Opening the lid instantly gives me the lock screen prompt

## deep

```
[nick@passat linux_sleep_experiment (main ✗)]$ ./battery_log.py
2021-10-30 12:44:06.185864 37.08% 6.53W 0.0000%/min
2021-10-30 12:44:16.196620 37.08% 5.34W 0.0000%/min
2021-10-30 13:24:59.119459 35.87% 13.92W -0.0298%/min
^C

$ cat /sys/power/mem_sleep
s2idle [deep]
```

0.0298%/min or about 1.788%/hr over about 40 minutes

100% / (%/hr rate) = 55.93 hours in sleep from a full charge

~15 seconds from lid open to lock screen prompt


# Conclusions

Deep sleep is about 23% better on battery usage than s2idle, _but_ with the 15
seconds it takes from me opening my laptop lid to it being ready to log in,
it's not really worth it if I'm opening and closing the lid often (like when
I'm using it around the house).

It might be worth it if I'm traveling, where it would be closed for a long time
between usage, but I might as well just hibernate it at that point. As a matter
of fact, I timed how long it takes to come out of hibernation and it only takes
**16 seconds** from off to login prompt (with 16GB of RAM).

## Possible Issues with Experiment

* I'm assuming that battery drain speed is uniform across charge percentages
  (drains the same at 100% as it does at 30%)
* My timing was pretty casual, didn't let it sleep for a long time and didn't
  sleep for the same amount of time for each run.
