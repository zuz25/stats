import pandas as pd
import numpy as np
import time
#import matplotlib.pyplot as plt

path='../ME Stats Data/'
date="2018-11-7"
path=path+date+"/"
pd.set_option('display.float_format', lambda x: '%.3f' % x)
df = pd.read_csv(path+date+'-raw.csv')
df_completed= df.dropna()
#print(df.columns.names)

stats = []
statsIndex =['Max','Min','Mean','Median','STD DEV']
statsCols =[]
dfStats=pd.DataFrame(index=statsIndex)
def durationStats(dataframe,description,initialTimeId,finalTimeId):
    #{0:.3f}.'.format(
    theseStats =[]
    statsCols.append(description)
    theseStats.append("{0:.1f}".format(((dataframe[finalTimeId]-dataframe[initialTimeId])/1000/60).max()))
    theseStats.append("{0:.1f}".format(((dataframe[finalTimeId]-dataframe[initialTimeId])/1000/60).min()))
    theseStats.append("{0:.1f}".format(((dataframe[finalTimeId]-dataframe[initialTimeId])/1000/60).mean()))
    theseStats.append("{0:.1f}".format(((dataframe[finalTimeId]-dataframe[initialTimeId])/1000/60).median()))
    theseStats.append("{0:.1f}".format(((dataframe[finalTimeId]-dataframe[initialTimeId])/1000/60).std()))
    #print(theseStats)
    #stats.append(theseStats)
    # print("Max Time",description,": ","{0:.1f}".format(((dataframe[finalTimeId]-dataframe[initialTimeId])/1000/60).max()))
    # print("Min Time",description,": ","{0:.1f}".format(((dataframe[finalTimeId]-dataframe[initialTimeId])/1000/60).min()))
    # print("Mean Time",description,": ","{0:.1f}".format(((dataframe[finalTimeId]-dataframe[initialTimeId])/1000/60).mean()))
    # print("Median Time",description,": ","{0:.1f}".format(((dataframe[finalTimeId]-dataframe[initialTimeId])/1000/60).median()))
    # print("STD Dev of time",description,": ","{0:.1f}".format(((dataframe[finalTimeId]-dataframe[initialTimeId])/1000/60).std()))
    # print("\n")
    df_completed[description]=(dataframe[finalTimeId]-dataframe[initialTimeId])/1000/60
    dfStats[description]=theseStats
    #print(dataframe[description])
    
    
def etaStats(dataframe,description,reference, ETA, actual):
    df_completed[description]=(dataframe[reference]+dataframe[ETA]*1000-dataframe[actual])/1000/60
    theseStats=[]
    statsCols.append(description)
    theseStats.append("{0:.1f}".format(((dataframe[description])).max()))
    theseStats.append("{0:.1f}".format(((dataframe[description])).min()))
    theseStats.append("{0:.1f}".format(((dataframe[description])).mean()))
    theseStats.append("{0:.1f}".format(((dataframe[description])).median()))
    theseStats.append("{0:.1f}".format(((dataframe[description])).std()))
    # print("Max Time",description,": ","{0:.1f}".format(((dataframe[description])).max()))
    # print("Min Time",description,": ","{0:.1f}".format(((dataframe[description])).min()))
    # print("Mean Time",description,": ","{0:.1f}".format(((dataframe[description])).mean()))
    # print("Median Time",description,": ","{0:.1f}".format(((dataframe[description])).median()))
    # print("STD Dev of time",description,": ","{0:.1f}".format(((dataframe[description])).std()))
    # print("\n")
    #stats.append(theseStats)
    dfStats[description]=theseStats

def findPUeqDO(dataframe,description):
    uniqueVINs=dataframe['VIN'].unique().tolist()
    print(uniqueVINs)
    uniquePUDOs=list(set(dataframe['ORIGIN_LAT'].unique().tolist()).intersection(dataframe['DESTINATION_LAT'].unique().tolist()))
    print(uniquePUDOs)
#    for vin in uniqueVINs:
#         for pudo in uniquePUDOs:
#             tempDF=dataframe[dataframe.loc[dataframe['VIN'] == vin]]# & dataframe.loc[dataframe['ORIGIN_LAT']==pudo]]
#             print(tempDF)
#             for index, row in tempDF.iterrows():
#                 print(vin, row['VIN'], pudo, row['ORIGIN_LAT'])

#durationStats(df_completed,"Time in Queue (Mins)","REQUESTED","STARTED")
durationStats(df_completed[df_completed['STARTED']-df_completed['REQUESTED']>(1000*60)],"Time in Queue","REQUESTED","STARTED")
durationStats(df_completed,"Time Waiting for Pickup (Mins)","STARTED","PICKED_UP")
durationStats(df_completed,"Total Wait Time (Mins)","REQUESTED","PICKED_UP")
durationStats(df_completed,"Total Time on Route(Mins)","PICKED_UP", "LAST_UPDATED")
etaStats(df_completed,"Estimated Pickup - Actual Pickup (Mins)","STARTED","ESTIMATED_PICKUP","PICKED_UP")
etaStats(df_completed,"Estimated Dropoff - Actual Dropoff (Mins)","PICKED_UP","ESTIMATED_DROPOFF","LAST_UPDATED")


#df_filtered = df[(df.STARTED >= ) & (df.year == 2017)]
print("Total Cancelled Rides: ",df['RIDE_STATUS'].str.count("CANCELLED").sum())
print("Total Queued Rides: ",df[(df['STARTED']-df['REQUESTED'])/1000/60>1]['ID'].count())
print ("Total Completed rides: ",df['RIDE_STATUS'].str.count("COMPLETED").sum()+df['RIDE_STATUS'].str.count("AT_DROPOFF").sum())
print("Total Rejected Rides: ", df['RIDE_STATUS'].str.count("REJECTED").sum())
print("Total Abandoned Rides: ", df['RIDE_STATUS'].str.count("ABANDONED").sum())

#str("Total Cancelled Rides: "+str(df['RIDE_STATUS'].str.count("CANCELLED").sum()))
#str("Total Queued Rides: ",df[(df['STARTED']-df['REQUESTED'])/1000/60>1]['ID'].count())
#str("Total Completed rides: ",df['RIDE_STATUS'].str.count("COMPLETED").sum()+df['RIDE_STATUS'].str.count("AT_DROPOFF").sum())
#str("Total Rejected Rides: ", df['RIDE_STATUS'].str.count("REJECTED").sum())
#str("Total Abandoned Rides: ", df['RIDE_STATUS'].str.count("ABANDONED").sum())



file = open(path+date+"-overall-stats.txt","w") 
#
file.write(str("Total Cancelled Rides: "+str(df['RIDE_STATUS'].str.count("CANCELLED").sum())))
file.write(str("Total Queued Rides: "+str(df[(df['STARTED']-df['REQUESTED'])/1000/60>1]['ID'].count())))
file.write(str("Total Completed rides: "+str(df['RIDE_STATUS'].str.count("COMPLETED").sum()+df['RIDE_STATUS'].str.count("AT_DROPOFF").sum())))
file.write(str("Total Rejected Rides: " + str(df['RIDE_STATUS'].str.count("REJECTED").sum())))
file.write(str("Total Abandoned Rides: " + str(df['RIDE_STATUS'].str.count("ABANDONED").sum())))
#  
file.close() 
#findPUeqDO(df_completed,"Pickup equals Dropoff (Y/N)")

#print(stats)
#print(statsCols)
writer = pd.ExcelWriter(path+date+'-output.xlsx')
dfStats.to_excel(writer,'stats')
df_completed.to_excel(writer,'data')
writer.save()
#dfStats.(path+date+'-stats.csv')
#df_completed.to_csv(path+date+'-output.csv')
#print(df_completed['pickup_actual-eta']/1000/60)
