# Wonderful FHEM log parser!
Parses `fhem` logs. Primarily used to calculate how much `heat` was used.
 > Use with care. May bite if not fed properly.

## Installation

1. Clone the repo:
```
git clone https://github.com/vale981/Da.git
```

2. Install the requirements (/note that on your system `pip` may be `pip3` etc./):
```
pip -r requirements.txt
```
3. Enjoy!

## Usage
```
usage: parseLogs.py [-h] [--parse FILE [FILE ...]] [--list]
                    [--heatAmmount HEATER] [--allHeatAmmount]
                    [--timeSpan t1..t2 | t1 | ..t2] [--verbose]

Parse the FHEM logfiles into a Database.

optional arguments:
  -h, --help            show this help message and exit
  --parse FILE [FILE ...], -p FILE [FILE ...]
                        List of Logfiles to Parse.
  --list, -l            List all Heaters in the Database.
  --heatAmmount HEATER  Sum of the actuator value times a time slice.
  --allHeatAmmount      Get the heat ammount from all known heaters.
  --timeSpan t1..t2 | t1 | ..t2
                        The time span for the heatAmmount calculation. Either
                        t1/t2 or both may be supplied.
  --verbose, -v         Output names and dates.
```

If run without arguments, the script will spit out the total heat amount for all heaters.

### Output Formating, Usage
Get the accumulated heat of `OG2_303_RT_01`:
```
# ./parseLogs.py --heatAmmount OG2_303_RT_01 --timeSpan '1 may 2016'..'1 june 2016' --verbose
OG2_303_RT_01, 0, 1462053600, 1464732000
```

Less info:
```
# ./parseLogs.py --heatAmmount OG2_303_RT_01 --timeSpan '1 may 2016'..'1 june 2016'
OG2_303_RT_01, 0, 1462053600, 1464732000
```

From the earliest record till a given date:
```
# ./parseLogs.py --heatAmmount OG2_303_RT_01 --timeSpan ..'1 june 2016'
OG2_303_RT_01, 285457264, 0, 1464732000
```


