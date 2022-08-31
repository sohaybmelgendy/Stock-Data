from ib_insync import *
import pandas as pd
from datetime import datetime, timezone
import time

#First, you have to create folders with the exact ticker name in your path.

ib = IB()

#for gateway use this
#ib.connect('127.0.0.1',-4001 or 4002- review gateway ports in API documentation ,clientId=1)

# us this for TWS (Workstation)
# Review TWS API settings
ib.connect('127.0.0.1', 7497, clientId=1)

stocknames=['Enter stock names here','Separated by commas like that for each ticker']

for stockname in stocknames:
#primaryExchange='ARCA' if needed
    stock = Stock(stockname, 'SMART', 'USD',primaryExchange='ARCA')

#endDateTime='' , for the present, or if you want specific date use the following
#example datetime(2022, 5, 4, tzinfo=timezone.utc)

#Edit months according to your needs
    months=[]
    for month in months:
        if month==11:
            y="Nov-2021"
            targetmonth=month
            targetyear=2021
            startday=1
            endday=30
        elif month==12:
            y="Dec-2021"
            targetmonth=month
            targetyear=2021
            startday=1
            endday=31
        elif month==1:
            y="Jan-2022"
            targetmonth=month
            targetyear=2022
            endday=31
            startday=19
        elif month==2:
            y="Feb-2022"
            targetmonth=month
            targetyear=2022
            startday=18
            endday=28
        elif month==3:
            y="March-2022"
            targetmonth=month
            targetyear=2022
            startday=1
            endday=31
        elif month==4:
            y="April-2022"
            targetmonth=month
            targetyear=2022
            startday=1
            endday=29
        elif month==5:
            y="May-2022"
            targetmonth=month
            targetyear=2022
            startday=2
            endday=26


        if targetmonth==12:
            extratargetmonth=1
        else:
            extratargetmonth=targetmonth+1

        if targetmonth !=12:
            extratargetyear=targetyear
        else:
            extratargetyear=targetyear+1

        def historicaldata(x):
            global df
            global filename
            bars = ib.reqHistoricalData(
                stock, endDateTime=datetime(targetyear, targetmonth, x, tzinfo=timezone.utc), durationStr='1 D',
                barSizeSetting='1 min', whatToShow='TRADES', useRTH=False, formatDate=2)

            # convert to pandas dataframe
            df = util.df(bars)
            df['epoch']=pd.to_datetime(df.date).astype(int) / 10**9


            filename=datetime.fromtimestamp(df['epoch'].iat[0]).strftime('%d-%m-%y')


            return df,filename

        filenames=[]
        for i in range(startday+1,endday+1):
            x=i
            historicaldata(x)

            if filename not in filenames:
                df.to_csv(r'Enter path here'.format(stockname,y), mode='a', index=False,header=False)
                filenames.append(filename)
                print(stockname +" "+ filename)
                time.sleep(1)
            else:
                time.sleep(1)
                continue


        def extradays():

            bars2 = ib.reqHistoricalData(
                stock, endDateTime=datetime(extratargetyear, extratargetmonth, 1, tzinfo=timezone.utc), durationStr='1 D',
                barSizeSetting='1 min', whatToShow='TRADES', useRTH=False, formatDate=2)

            # convert to pandas dataframe
            dff = pd.DataFrame(bars2)
            dff['epoch']=pd.to_datetime(dff.date).astype(int) / 10**9
            #save to a CSV file.
            dff.to_csv(r'Enter your path here'.format(stockname,y), mode='a', index=False,header=False)
            filename2=datetime.fromtimestamp(dff['epoch'].iat[0]).strftime('%d-%m-%y')
            print(filename2)



        #adding the headers to the CSV file.
        Cov = pd.read_csv("Same Path here\{}\{}.csv".format(stockname,y), header=None)
        Cov.to_csv("Same Path here\{}\{}.csv".format(stockname,y),header=["date", "open", "high", "low","close","volume","average","barCount","epoch"],index=False)
