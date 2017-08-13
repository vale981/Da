import sys
import datetime
import argparse
import logParser
from math import inf

argparser = argparse.ArgumentParser(description='Parse the FHEM logfiles into a Database.')
argparser.add_argument('--parse', '-p', nargs='+', help='List of Logfiles to Parse.', required=False, metavar='FILE')
argparser.add_argument('--list', '-l', help='List all Heaters in the Database.', action='store_true')
argparser.add_argument('--heatAmmount', help='Sum of the actuator value times a time slice.', nargs=1, metavar='HEATER')
argparser.add_argument('--allHeatAmmount', help='Get the heat ammount from all known heaters.', action='store_true')
argparser.add_argument('--timeSpan', help='The time span for the heatAmmount calculation. Either t1/t2 or both may be supplied.', nargs=1, metavar='t1..t2 | t1 | ..t2')

# Parse args. Set name to default.
args = argparser.parse_args()
mintime, maxtime = 0, inf
if args.timeSpan:
        times = args.timeSpan[0].split('..')

        if len(times) < 1 or len(times) > 2:
            print('Invalid Timespan!')
            exit(1)
        elif len(times) == 2:
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
    print(logParser.getHeaterSum(args.heatAmmount[0], mintime, maxtime))
elif not args.allHeatAmmount is None:
    print(logParser.getAllHeaterSums(mintime, maxtime))
