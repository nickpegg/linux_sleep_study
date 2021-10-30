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

My laptop is a first-generation Framwork laptop with an Intel i7-1165G7 CPU.

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
