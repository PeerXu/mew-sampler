#! /bin/sh

mkdir -p /var/mew
/usr/sbin/mew-sampler.py --symbol TUSDBTC | /usr/sbin/mew-logger.py --period daily --output /var/mew/TUSDBTC.csv
