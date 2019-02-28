#! /usr/bin/env python3

import sys
import time
import getopt

import requests


class BinanceSampler(object):
    BASEURL = 'https://api.binance.com/api/v1/trades'

    def __init__(self, symbol='TUSDBTC', limit=3, timeout=1):
        self.symbol = symbol
        self.limit = limit
        self.timeout = 1
        self.session = None

    def sample(self):
        if self.session is None:
            self.session = requests.Session()

        try:
            res = requests.get(self.BASEURL + '?symbol=' + self.symbol + '&limit=' + str(self.limit), timeout=self.timeout)
            if res.status_code != 200:
                return []
        except:
            self.session = None
            return []

        trades = res.json()
        trades = [{
            'timestamp': t['time'] / 1000,
            'price': float(t['price']),
        } for t in trades]

        return trades


def parse_args(args):
    opts = {
        'symbol': 'TUSDBTC',
        'limit': 3,
        'timeout': 1,
        'interval': 5,
        'output': '-',
    }

    popts, pargs = getopt.getopt(args, 'ho:', ['help', 'symbol=', 'limit=', 'timeout=', 'interval=', 'output='])

    for o, a in popts:
        if o in ('-h', '--help'):
            _usage()
        elif o == '--symbol':
            opts['symbol'] = a
        elif o == '--limit':
            opts['limit'] = int(a)
        elif o == '--timeout':
            opts['timeout'] = float(a)
        elif o == '--interval':
            opts['interval'] = float(a)
        elif o in ('-o', '--output'):
            opts['output'] = a

    return opts


def _usage():
    sys.stderr.write('usage: xxx\n')
    sys.exit(1)


def _main():
    opts = parse_args(sys.argv[1:])

    sampler = BinanceSampler(
        symbol=opts['symbol'],
        limit=opts['limit'],
        timeout=opts['timeout'],
    )

    if opts['output'] == '-':
        output = sys.stdout
    else:
        output = open(opts['output'], 'a')

    while True:
        trds = sampler.sample()
        for trd in trds:
            output.write('%s,%s\n' % (trd['timestamp'], trd['price']))
        output.flush()
        time.sleep(opts['interval'])

if __name__ == '__main__':
    _main()
