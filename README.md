# CM2016
Python code to read measurements from the battery charger Voltcraft Charge Manager CM2016


# Contents

This repository contains
- code to [read raw data](src/CM2016/CMserial.py) over USB from the CM2016 device
- an [abstraction of the CM2016 unit](src/CM2016/CM2016.py) that provides classes to interpret raw data from the device
- [example code](src/main.py) to read raw data from a CM2016 over USB, parse it, and display the information from the device

# Status

This code is in prototype status. It was tested on a Raspberry Pi, Linux kernel 4.14.34-v7+, Python version 2.7.13.

The code assumes that CM2016 is connected through /dev/ttyUSB0. This code can be changed in the [config file](src/CM2016.ini).

There are several things to be checked and maybe improved:
- handling of the serial connection and timeouts
- handling of unexpected situations (e.g., wrongly configured USB port)
- formatting of the output on the console

# References
- [Java-based tool for CM2016](https://gitlab.projecttac.com/tarator/cm2016)
- [Description of the raw data](http://www.leisenfels.com/howto-charge-manager-2016-data-format)
