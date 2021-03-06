import json
from urllib.request import urlopen
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import MetaData, Table
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy import Index
from sqlalchemy.orm import relationship, backref
import logging
from sqlalchemy.orm import sessionmaker
from apis import getCountyCode, getCensusData
from table_classes import eduPoverty_row


path = os.path.abspath("MinorLeague.db")
#dir_path = os.path.dirname(os.path.realpath("/MinorLeague/MinorLeague.db"))
#Define declarative base class
Base = declarative_base()
engine = create_engine("sqlite:///"+path, echo = False)#Set to false to git rid of log
#Link a session to the engine and initialize it
conn = engine.connect()
metadata = Base.metadata


Session = sessionmaker(bind=engine)
session = Session()


#Upload the ZipCodes table as a Table object
zipCodes = Table('ZipCodes', metadata, autoload = True, autoload_with=engine)
censusTables = Table('CensusTables',metadata, autoload = True, autoload_with=engine)
#print(zipCodes.columns)

# A table that gives the population of a stadium's county
class Attributes(Base):
    
    __tablename__ = "Attributes"
    year = Column('year', Integer, primary_key = True)
    stadium = Column('stadium', String(40), primary_key = True)
    population = Column('population', Integer)
    meanIncome = Column('meanIncome', Integer)
    medianIncome = Column('medianIncome', Integer)
    povertyPop = Column('povertyPop', Integer)
    medianHomeVal= Column('medianHomeVal', Integer)
    workers = Column('workers', Integer)
    medianHouseIncome = Column('medianHouseIncome', Integer)
    medianFamilyIncome = Column('medianFamilyIncome', Integer)
    medianNonFamIncome = Column('medianNonFamIncome', Integer)
    medianWorkerIncome = Column('medianWorkerIncome', Integer)
    medianAge = Column('medianAge', Integer)
    medianRealEstateTax = Column('medianRealEstateTax', Integer)
    medianHouseholdCosts = Column('medianHouseholdCosts', Integer)
    totalHouses = Column('totalHouses', Integer)
    
    def __init__(self, year, stadium,meanIncome,medianIncome,povertyPop,medianHomeVal,
                 workers,medianHouseIncome,medianFamilyIncome,medianNonFamIncome,medianWorkerIncome,
                 medianAge,population,medianRealEstateTax,medianHouseholdCosts,totalHouses):
        
        self.year = year
        self.stadium = stadium
        self.meanIncome = meanIncome
        self.medianIncome = medianIncome
        self.povertyPop = povertyPop
        self.medianHomeVal = medianHomeVal
        self.workers = workers
        self.medianHouseIncome = medianHouseIncome
        self.medianFamilyIncome = medianFamilyIncome
        self.medianNonFamIncome = medianNonFamIncome
        self.medianWorkerIncome = medianWorkerIncome
        self.medianAge = medianAge
        self.population = population
        self.medianRealEstateTax = medianRealEstateTax
        self.medianHouseholdCosts = medianHouseholdCosts
        self.totalHouses = totalHouses

# Create the table
#Base.metadata.create_all(engine)
    
"""  
jimmystadium = session.query(zipCodes).filter_by(ZipCode = 48317).one() #This returns the item from the table as an object
print(jimmystadium.City) #Then you can access it's attributes directly
"""
       

# A list of years that we need data for
years = [2011, 2012, 2013, 2014, 2015, 2016, 2017]

atList = []
atList1 = []
atList2 = []

censusList = []

for row1 in session.query(censusTables).all():
    censusList.append(row1.TableNames)
    
#print(censusList[0]+"Next:"+ censusList[1]+"Next:"+ censusList[2])


for row in session.query(zipCodes).all():
    for year in years:
        meanIncome, medianIncome, povertyPop = getCensusData(year, row.County, row.State, censusList[0])
        #subject table
        medianHomeVal,workers,medianHouseIncome,medianFamilyIncome,medianNonFamIncome,medianWorkerIncome,medianAge = getCensusData(year, row.County, row.State, censusList[1])
        #data_profile table
        population,medianRealEstateTax,medianHouseholdCosts,totalHouses = getCensusData(year, row.County, row.State, censusList[2])
        #detailed_tables

    """
    print(year, meanIncome, medianIncome, povertyPop) 
    print(year, medianHomeVal,workers,medianHouseIncome,medianFamilyIncome,medianNonFamIncome,medianWorkerIncome,medianAge)
    print(year, population,medianRealEstateTax,medianHouseholdCosts,totalHouses )       
        
        #print (row.Stadium, year, getPop(year, countyName=row.County, state = row.State))
        #new = Attributes(str(year), row.Stadium, atList[0][0],  atList[0][1],
        #atList[0][2],  atList[0][3], atList[1][0], atList[1][1], atList[1][2], atList[1][3]
        #, atList[1][4], atList[1][5], atList[1][6], atList[2][0], atList[2][1], atList[2][3])
        #session.add(new) THIS LINE AND THE ONE BELOW IT SHOULD ADD THE DATA TO A NEW TABLE CALLED "POPULATION"
        #session.commit() IT KEPT THROWING AN ERROR THAT DATABASE IS LOCKED

    #for row in session.query(zipCodes).filter_by(ZipCode= '48317').first():

"""




