#!/usr/bin/env python3

import sys
import time
import argparse
import logParser
import dateparser
from math import inf

argparser = argparse.ArgumentParser(description='Parse the FHEM logfiles into a Database.')
argparser.add_argument('--parse', '-p', nargs='+', help='List of Logfiles to Parse.', required=False, metavar='FILE')
argparser.add_argument('--list', '-l', help='List all Heaters in the Database.', action='store_true')
argparser.add_argument('--heatAmmount', help='Sum of the actuator value times a time slice.', nargs=1, metavar='HEATER')
argparser.add_argument('--allHeatAmmount', help='Get the heat ammount from all known heaters.', action='store_true')
argparser.add_argument('--timeSpan', help='The time span for the heatAmmount calculation. Either t1/t2 or both may be supplied.', nargs=1, metavar='t1..t2 | t1 | ..t2')
argparser.add_argument('--verbose', '-v', help='Output more information about the query.', action='store_true')


# Parse args. Set name to default.
args = argparser.parse_args()
mintime, maxtime = 0, time.time()
if args.timeSpan:
        times = args.timeSpan[0].split('..')


        if len(times) < 1 or len(times) > 2:
            print('Invalid Timespan!')
            exit(1)
        elif len(times) == 2:
            times[0] = dateparser.parse(times[0]).timestamp()
            times[1] = dateparser.parse(times[1]).timestamp()

            if times[0] == '':
                maxtime = int(times[1])
            else:
                mintime, maxtime = times

        else:
            mintime = int(times[0])

if not args.parse is None:
    parser = logParser.LogParser(args.parse)
    parser.parse()
elif not args.list is False:
    print('\n'.join(logParser.getHeaterList()))
elif not args.heatAmmount is None:
        heat = args.heatAmmount[0], logParser.getHeaterSum(args.heatAmmount[0], mintime, maxtime)
        if args.verbose:
           print(', '.join([heat[0], str(heat[1]), str(int(mintime)), str(int(maxtime))]))
        else:
          print(heat[1])
elif not args.allHeatAmmount is None:
        allheaters = logParser.getAllHeaterSums(mintime, maxtime)

        for heater in allheaters:
          if args.verbose:
            print(', '.join([heater, str(allheaters[heater]), str(int(mintime)), str(int(maxtime))]))
          else:
            print(', '.join([heater, str(allheaters[heater])]))
