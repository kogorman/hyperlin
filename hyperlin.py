#!/usr/bin/env python

"""Module for dealing with hyperthreads on Intel machines.

This program may be useful by itself for a quick check and demo, but is intended
to be used as a module by other Python programs.

NOTE: changing the state of a hyperthread requires root privileges.

Works on multi-cpu motherboards.  Tested with Ubuntu/Xubuntu 16.04

Last Modified: Sun Nov 12 14:38:45 PST 2017
"""

from __future__ import (absolute_import, division, print_function, unicode_literals)

import argparse         # https://docs.python.org/3.5/library/argparse.html

def _expand(strspec):
    ss = strspec.strip()
    if ss == '':
        return []
    l=ss.split(',')
    r = []
    for piece in l:
        ends=piece.split('-')
        if len(ends) == 1:
            r += [int(ends[0])]
        else:
            r += range(int(ends[0]), int(ends[1]) + 1)
    return r

def onlinestr():
    with open("/sys/devices/system/cpu/online") as kernel:
        return kernel.readline()
def offlinestr():
    with open("/sys/devices/system/cpu/offline") as kernel:
        return kernel.readline()
def presentstr():
    with open("/sys/devices/system/cpu/present") as kernel:
        return kernel.readline()
def present():
    return _expand(presentstr())
def online():
    return _expand(onlinestr())
def threadcount():
    return len(online())
def corecount():
    return len(present())
def offline():
    return _expand(offlinestr())
def _firstelem(pair):
    return int(pair[0])
def pairlist():
    l=[]
    for thread in online():
        with open("/sys/devices/system/cpu/cpu" + str(thread) +
                "/topology/thread_siblings_list") as sl:
            l += [sl.readline().strip()]
    lset = set(l)
    sl = sorted(list(lset), key=_firstelem)
    mylist = []
    for i in sl:
        p=i.split(',')
        if len(p) == 1:
            mylist += [[int(p[0])]]
        else:
            mylist += [[int(p[0]),int(p[1])]]
    return sorted(list(mylist), key=_firstelem)
def primaries():
    return [ p[0] for p in pairlist() ]
def secondaries():
    return [ p[1] for p in pairlist() if len(p) > 1 ]
def setstate(core, state):
    c = int(core)
    assert c in present(), str(int(core)) + "is not an available thread"
    with open("/sys/devices/system/cpu/cpu" + str(c) + "/online","w") as online:
        print(1 if state else 0, file=online)

def show():
    on=online()
    off=offline()
    here=present()
    print("Available cores:",present())
    if on == here:
        print("Online: all")
    else:
        print("Online:",on)
        print("Offline:",off)
    print("Sibling list:",pairlist())
    print("Primaries:",primaries())
    print("Secondaries:",secondaries() if len(secondaries()) > 0 else "None")

def samplerun():
    show()
    print()
    if len(secondaries()) > 1:
        victim = secondaries()[1]
    elif len(secondaries) == 1:
        victim = secondares()[0]
    else:
        print("Cannot continue: there are no secondary threads")
        return

    print("OFF")
    setstate(victim,0)
    show()
    print()

    print("ON")
    setstate(victim,1)
    show()
    print()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description="""A module for accessing hyperthread controls in Linux.
            Includes command-line controls as well.""",epilog="""The arguments
            are honored in the order shown here, regardless of position on
            the command line.""")
    parser.add_argument("--on", nargs="+",
            help="""a thread to enable.
                    May be used multiple times.  Can specify 'all' and all
                    offline threads are turned on..
                    Requires root permissions.""")
    parser.add_argument("--off", nargs="+",
            help="""a thread to disaable.
                    May be used multiple times.  Can specify 'all' but it only
                    affects the online secondaries.
                    Requires root permissions.""")
    parser.add_argument("--demo", action = "store_true",
            help="Run the test code (requires root permission)")
    parser.add_argument("--show", action = "store_true",
            help="Show the current state of all threads")
    args=parser.parse_args()

    if args.on is not None:
        for thread in args.on:
            if thread == "all":
                for t in offline():
                    setstate(t, 1)
            else:
                setstate(thread, 1)


    if args.off is not None:
        for thread in args.off:
            if thread == "all":
                for t in secondaries():
                    setstate(t, 0)
            else:
                setstate(thread, 0)

    if args.demo:
        samplerun()
        exit(0)
    if args.show:
        show()
        exit(0)
