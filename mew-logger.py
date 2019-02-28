#! /usr/bin/env python3

import os
import sys
import getopt
from datetime import timedelta
from datetime import datetime


def _usage():
    sys.stderr.write('usage: xxx\n')
    sys.exit(1)


def parse_args(args):
    opts = {
        'period': '',
        'output': '-',
    }

    popts, pargs = getopt.getopt(args, 'hp:o:', ['help', 'period=', 'output='])

    for o, a in popts:
        if o in ('-h', '--help'):
            _usage()
        elif o in ('-p', '--period'):
            opts['period'] = a
        elif o in ('-o', '--output'):
            opts['output'] = a

    return opts


def save_at(period, current):
    if period == '':
        return (datetime.now()+timedelta(days=365*1000)).timestamp()
    elif period == 'daily':
        dt = timedelta(days=1)
    elif period == 'hourly':
        dt = timedelta(seconds=3600)
    elif period == 'minutely':
        dt = timedelta(seconds=60)
    d = datetime.fromtimestamp(current)
    d = d + dt
    if period == 'minutely':
        d = d.replace(second=0)
    if period == 'hourly':
        d = d.replace(minute=0)
    if period == 'daily':
        d = d.replace(hour=0)
    return d.timestamp()


def _main():
    opts = parse_args(sys.argv[1:])
    if opts['output'] == '-' and opts['period'] != '':
        _usage()

    if opts['output'] == '-':
        output = sys.stdout
    else:
        output = open(opts['output'], 'w')

    last = 0
    last_save_at = 0
    while True:
        line = sys.stdin.readline()
        try:
            t, p = line.strip().split(',')
            t = float(t)

            if last_save_at == 0:
                last_save_at = save_at(opts['period'], t)

            if last < t:
                if last_save_at < t:
                    output.flush()
                    output.close()
                    os.rename(opts['output'], opts['output'] + '.' + datetime.fromtimestamp(last_save_at).strftime('%Y%m%d%H%M%S'))
                    output = open(opts['output'], 'w')
                    last_save_at = save_at(opts['period'], t)

                last = t
                output.write('%s,%s\n' % (t, p))
                output.flush()
        except:
            continue


if __name__ == '__main__':
    _main()
