from sqlalchemy import Column, Integer, String, REAL
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from datetime import datetime
from math import inf

engine = create_engine('sqlite:///heaters.db')
session_factory = sessionmaker(bind=engine)
Session = lambda : scoped_session(session_factory)

Base = declarative_base()
heaters = {}

class HeaterStatProto():
    time = Column(Integer, primary_key=True)
    actuator = Column(Integer)
    desired_temp = Column(REAL)
    measured_temp = Column(REAL)
    dewpoint = Column(REAL)
    humidity = Column(REAL)

class Heater(Base):
    __tablename__ = 'heater_list'
    name = Column(String, primary_key=True)

Base.metadata.create_all(engine)

def getHeater(name):
    if name in heaters:
        return heaters[name]

    session = Session()
    heater = Heater(name=name)
    session.merge(heater)
    session.commit()
    session.close()

    heater = type(name, (Base, HeaterStatProto), {'__tablename__': 'heater_' + name})

    Base.metadata.create_all(engine)
    heaters[name] = heater
    return heater

def getHeaterList():
    session = Session()
    heaters = session.query(Heater).all()
    session.close()
    return [heater.name for heater in heaters]

def getHeaterSum(heater, mintime = 0, maxtime = inf):
    if not heater in getHeaterList():
        return 'Heater not found!'

    heater = getHeater(heater)
    session = Session()
    heaterData = session.query(heater).filter(heater.time > mintime, heater.time < maxtime).order_by(heater.time.asc()).all()
    session.close()

    totalHeat = 0
    for h in range(0, len(heaterData) - 1):
        try:
            totalHeat += heaterData[h].actuator * (heaterData[h+1].time - heaterData[h].time)
        except:
            continue

    return totalHeat

def getAllHeaterSums(*args, **kwargs):
    sums = {}
    for heater in getHeaterList():
        sums[heater] = getHeaterSum(heater, *args, **kwargs)

    return sums

class LogParser:
    # Some constants...
    def parseLog(self, data):
        totalLines = len(data)
        print('Parsing', totalLines, 'lines.')

        heaterData = {}

        lineNum = 0
        for line in data:
            lineNum += 1
            print('\r  Progress:', int((lineNum/totalLines)*100), end='')
            line = line.strip().split(' ')

            if not (len(line) == 4):
                continue

            timeStamp, name, prop, value = line
            prop = prop[:-1].replace('-', '_')

            if hasattr(HeaterStatProto, prop):
                timeStamp = datetime.strptime(timeStamp, '%Y-%m-%d_%H:%M:%S').timestamp()

                if not name in heaterData:
                    heaterData[name] = {}

                if not timeStamp in heaterData[name]:
                    heaterData[name][timeStamp] = {}

                heaterData[name][timeStamp][prop] = value

        print('\n')
        self.simplify(heaterData)
        return heaterData

    def simplify(self, data):
        print('Removing redundant data...')
        for heater in data.values():
            lastValue = None
            for key, value in list(heater.items()):
                if value == lastValue:
                    del heater[key]
                    continue

                lastValue = value

    def writeHeaters(self, data):
        print('Writing the parsed data to the Database...')
        heaters = []

        for heater, heaterHistory in data.items():
            dbHeater = getHeater(heater)
            for time, heaterData in heaterHistory.items():
                heaters.append(dbHeater(time=time, **heaterData))

        session = Session()
        #session.add_all(heaters)
        for heater in heaters:
            try:
                session.merge(heater)
            except:
                print('Could not write: ', heaterx)

        session.commit()
        session.close()

    def parse(self):
        try:
            for logfile in self._logfiles:
                with open(logfile) as lf:
                    try:
                        print('Reading:', logfile)
                        logdata = lf.readlines()
                        self.writeHeaters(self.parseLog(logdata))

                    except (IOError, UnicodeDecodeError) as e:
                        print('Could not read: ', logfile)

                    print()

        except EnvironmentError:
            raise ValueError('Invalid log file!')

        print('Done')

    def __init__(self, logfiles):
        # Try to read the heater log.
        self._logData = []
        self._logfiles = logfiles


