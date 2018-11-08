import pandas as pd
import numpy as np
import time
#import matplotlib.pyplot as plt

pd.set_option('display.float_format', lambda x: '%.3f' % x)
df = pd.read_csv('../ME Stats Data/11-7-data.csv')
df_completed= df.dropna()
#print(df.columns.names)

def durationStats(dataframe,description,initialTimeId,finalTimeId):
    #{0:.3f}.'.format(
    print("Max Time",description,": ","{0:.1f}".format(((dataframe[finalTimeId]-dataframe[initialTimeId])/1000/60).max()))
    print("Min Time",description,": ","{0:.1f}".format(((dataframe[finalTimeId]-dataframe[initialTimeId])/1000/60).min()))
    print("Mean Time",description,": ","{0:.1f}".format(((dataframe[finalTimeId]-dataframe[initialTimeId])/1000/60).mean()))
    print("Median Time",description,": ","{0:.1f}".format(((dataframe[finalTimeId]-dataframe[initialTimeId])/1000/60).median()))
    print("STD Dev of time",description,": ","{0:.1f}".format(((dataframe[finalTimeId]-dataframe[initialTimeId])/1000/60).std()))
    print("\n")
    dataframe[description]=(dataframe[finalTimeId]-dataframe[initialTimeId])/1000/60
    print(dataframe[description])
    
    
def etaStats(dataframe,description,reference, ETA, actual):
    dataframe[description]=(dataframe[reference]+dataframe[ETA]*1000-dataframe[actual])/1000/60
    print("Max Time",description,": ","{0:.1f}".format(((dataframe[description])).max()))
    print("Min Time",description,": ","{0:.1f}".format(((dataframe[description])).min()))
    print("Mean Time",description,": ","{0:.1f}".format(((dataframe[description])).mean()))
    print("Median Time",description,": ","{0:.1f}".format(((dataframe[description])).median()))
    print("STD Dev of time",description,": ","{0:.1f}".format(((dataframe[description])).std()))
    print("\n")

durationStats(df_completed,"TIME_IN_QUEUE","REQUESTED","STARTED")
#durationStats(df[df['STARTED']-df['REQUESTED']],"TIME_IN_QUEUE","REQUESTED","STARTED")
durationStats(df_completed,"TIME_WAITING_FOR_PICKUP","STARTED","PICKED_UP")
durationStats(df_completed,"TOTAL_WAIT_TIME","REQUESTED","PICKED_UP")
durationStats(df_completed,"TOTAL_TIME_ON_ROUTE","PICKED_UP", "LAST_UPDATED")
etaStats(df_completed,"ESTIMATED_PICKUP-PICKED_UP","STARTED","ESTIMATED_PICKUP","PICKED_UP")
etaStats(df_completed,"ESTIMATED_DROPOFF-DROPOFF","PICKED_UP","ESTIMATED_DROPOFF","LAST_UPDATED")


#df_filtered = df[(df.STARTED >= ) & (df.year == 2017)]
print("Total Cancelled Rides: ",df['RIDE_STATUS'].str.count("CANCELLED").sum())
print("Total Queued Rides: ",df[(df['STARTED']-df['REQUESTED'])/1000/60>1]['ID'].count())
print ("Total Completed rides: ",df['RIDE_STATUS'].str.count("COMPLETED").sum()+df['RIDE_STATUS'].str.count("AT_DROPOFF").sum())
print("Total Rejected Rides: ", df['RIDE_STATUS'].str.count("REJECTED").sum())
print("Total Abandoned Rides: ", df['RIDE_STATUS'].str.count("ABANDONED").sum())

df_completed.to_csv('../ME Stats Data/11-7-output.csv')
#print(df_completed['pickup_actual-eta']/1000/60)
