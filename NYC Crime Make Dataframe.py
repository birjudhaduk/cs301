import pandas as pd
import numpy as np

df = pd.read_csv('C:\\Users\\birju\\Documents\\CS 301\\NYPD_Complaint_Data_Current__Year_to_Date_.csv')
df = df.drop(['CMPLNT_FR_DT', 'CMPLNT_NUM', 'ADDR_PCT_CD', 'CMPLNT_TO_DT',
              'CMPLNT_TO_TM', 'HADEVELOPT', 'HOUSING_PSA', 'JURISDICTION_CODE',
              'JURIS_DESC', 'KY_CD', 'LOC_OF_OCCUR_DESC', 'OFNS_DESC',
              'PARKS_NM', 'PATROL_BORO', 'PD_CD', 'PD_DESC', 'PREM_TYP_DESC',
              'RPT_DT', 'STATION_NAME', 'SUSP_AGE_GROUP', 'SUSP_RACE',
              'SUSP_SEX', 'TRANSIT_DISTRICT', 'VIC_AGE_GROUP', 'VIC_RACE',
              'VIC_SEX', 'X_COORD_CD', 'Y_COORD_CD', 'Lat_Lon'], axis=1)

df.to_csv('C:\\Users\\birju\\Documents\\CS 301\\NYPD_Complaint_Data_Clean.csv', index = False)

total = np.zeros(25)
manhattan = np.zeros(25)
queens = np.zeros(25)
bronx = np.zeros(25)
brooklyn = np.zeros(25)
staten_island = np.zeros(25)
felony = np.zeros(25)
misdemeanor = np.zeros(25)
violation = np.zeros(25)
for ind in df.index:
    name = df['BORO_NM'][ind]
    level = df['LAW_CAT_CD'][ind]
    hour = int(str(df['CMPLNT_FR_TM'][ind])[0:2])
    total[hour] += 1
    if name == 'MANHATTAN':
        manhattan[hour] += 1
    if name == 'QUEENS':
        queens[hour] += 1
    if name == 'BRONX':
        bronx[hour] += 1
    if name == 'BROOKLYN':
        brooklyn[hour] += 1
    if name == 'STATEN ISLAND':
        staten_island[hour] += 1
    if level == 'FELONY':
        felony[hour] += 1
    if level == 'MISDEMEANOR':
        misdemeanor[hour] += 1
    if level == 'VIOLATION':
        violation[hour] += 1
total[24] = total[0]
manhattan[24] = manhattan[0]
queens[24] = queens[0]
bronx[24] = bronx[0]
brooklyn[24] = brooklyn[0]
staten_island[24] = staten_island[0]
felony[24] = felony[0]
misdemeanor[24] = misdemeanor[0]
violation[24] = violation[0]
hour = ['12AM', '1AM', '2AM', '3AM', '4AM', '5AM', '6AM',
        '7AM', '8AM', '9AM', '10AM', '11AM', '12PM',
        '1PM', '2PM', '3PM', '4PM', '5PM', '6PM',
        '7PM', '8PM', '9PM', '10PM', '11PM', '12.AM']

d = {'Hour':hour, 'Total':total, 'Manhattan':manhattan, 'Queens':queens,
     'Bronx':bronx, 'Brooklyn':brooklyn, 'Staten Island':staten_island,
     'Felony':felony, 'Misdemeanor':misdemeanor, 'Violation':violation}
df_count = pd.DataFrame(d, columns = ['Hour', 'Total', 'Manhattan', 'Queens',
                                      'Bronx', 'Brooklyn', 'Staten Island',
                                      'Felony', 'Misdemeanor', 'Violation'])
df_count.to_csv('C:\\Users\\birju\\Documents\\CS 301\\NYPD_Complaint_Data_Count.csv', index = False)
