# hyperlin
Hyperthreading in Python on Linux

This is a one-file Python module to display and control information about hyperthreading on the current machine.  It is designed for Linux.  It depends on the /sys/devices pseudo-directory that is presented by Linux kernels.

It has been tested on Ubuntu and Xubuntu 16.04 on both x86-64 and Xeon processors, on Python 2.7.3 and 3.5.2, with both one and two CPUs per motherboard.  It requires only the argparse module that is built into Python.

Short Usage:
  $ hyperlin -h
 
Shows help text.
