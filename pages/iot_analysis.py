import pandas as pd
import numpy as np
from pages import iot

iotdata = iot.iot_data.copy()
iotdata.drop(['Time', 'Battery'], axis = 1,inplace=True)

########################### Remove extreme outliers #######################
iotdata['Temperature in Celsius'].values[iotdata['Temperature in Celsius'] > 75.0] = 75.0
iotdata['Humidity'].values[iotdata['Humidity'] < 0] = 0
########################### Replace missing values with mean #######################
for i in iotdata[1:]:
    iotdata[i] = iotdata[i].fillna(iotdata[i].mean()) 

iotdata['Pressure'] = iotdata['Pressure'].div(1000)  

########################## Replace outlier with interpolation #######################
def outlier_treatment(col):
    Q1 = np.percentile(iotdata[col], 25, interpolation = 'midpoint')
    Q3 = np.percentile(iotdata[col], 75, interpolation = 'midpoint')
    IQR = Q3-Q1
    LQ = Q1-(1.5*IQR)
    UQ = Q3 +(1.5*IQR)
    iotdata[col].values[iotdata[col] < LQ] = np.NaN
    iotdata[col].values[iotdata[col] > UQ] = np.NaN

for i in iotdata.columns[2:]:
    outlier_treatment(i)
    
iotdata=iotdata.interpolate(method='nearest', limit_direction='forward', axis=0) 

