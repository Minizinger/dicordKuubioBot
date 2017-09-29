#horsebase = database for storing horses
from pymongo import MongoClient
import datetime

class HorseBase:
    def __init__(self):
        self.client = MongoClient('mongodb://mongo:27017')
        self.db = self.client['kuubiobot']

    def addHorseToDB(self, channel, time, poster):
        horse = {'time': time, 'author': poster}
        self.db[channel].insert_one(horse)

    def getMyHorses(self, channel, poster):
        total = self.db[channel].find({'author': poster}).count()
        month = self.db[channel].find({'author': poster, 'time': {'$gte': datetime.datetime.today().replace(day=1, hour=0, minute=0, second=0)}}).count()
        return {'total': total, 'month': month}

    def getTopHorses(self, channel, topPositions):
        AlltimeTop = []
        collection = self.db[channel].find()
        authors = list(set([e['author'] for e in collection]))
        horsesperauthor = {}
        for a in authors:
            horsesperauthor[a] = len([e for e in collection if e['author'] == a])
        if len(authors) > 0:
            for _ in range(topPositions):
                topresult = max(horsesperauthor.items(), key=operator.itemgetter(1))
                AlltimeTop.append(topresult)
                del horsesperauthor[topresult[0]]
        
        MonthTop = []
        collection = self.db[channel].find({'time': {'$gte': datetime.datetime.today().replace(day=1, hour=0, minute=0, second=0)}})
        authors = list(set([e['author'] for e in collection]))
        horsesperauthor = {}
        for a in authors:
            horsesperauthor[a] = len([e for e in collection if e['author'] == a])
        if len(authors) > 0:
            for _ in range(topPositions):
                topresult = max(horsesperauthor.items(), key=operator.itemgetter(1))
                MonthTop.append(topresult)
                del horsesperauthor[topresult[0]]

        return {'alltime': AlltimeTop, 'month': MonthTop}

    def getTotalHorses(self, channel):
        return self.db[channel].find().count()