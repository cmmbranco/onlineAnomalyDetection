

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#df = pd.read_csv('results/my/realKnownCause/my_nyc_taxi.csv')
df = pd.read_csv('results/my/realKnownCause/my_nyc_diff.csv')

mydf = df[['anomaly_score','label']]

#print(mydf)


TP = 0;
TN = 0;
FP = 0;
FN = 0;

for row in df.iterrows():

    if(row[1]['anomaly_score'] == row[1]['label']):
        if row[1]['anomaly_score'] == 0:
            TN += 1

        else:
            TP += 1

    else:
        if row[1]['anomaly_score'] == 0:
            FN +=1

        else:
            FP += 1



print('my,standard,TP,TN,FP,FN,' + str(TP) + ',' + str(TN)+ ','+ str(FP)+ ','+ str(FN) )
