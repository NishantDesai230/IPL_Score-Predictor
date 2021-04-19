import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
import pickle
import seaborn as sns

#READING THE DATA
df = pd.read_csv('ipl.csv')

#COLUMNS THAT WE WILL REMOVE..
r_column = ['mid','batsman','bowler','striker','non-striker']

#DROPING UNNECCESARY COLUMNS..
df.drop(labels=r_column,axis=True,inplace=True)

#TAKING DATA AFTER 5 OVERS FOR BETTER PREDICTION..
df = df[df['overs']>=5.0]

#IMPORTING DATETIME..
from datetime import datetime


df['date'] = df['date'].apply(lambda x:datetime.strptime(x,"%Y-%m-%d"))


df['bat_team'].unique()


current_team = ['Kolkata Knight Riders', 'Chennai Super Kings', 'Rajasthan Royals','Mumbai Indians', 'Kings XI Punjab','Royal Challengers Bangalore', 'Delhi Daredevils', 'Sunrisers Hyderabad']


df = df[(df['bat_team'].isin(current_team)) & (df['bowl_team'].isin(current_team))] 


df['bat_team'].unique()

x = pd.get_dummies(data=df,columns=['bat_team','bowl_team'])


x = x[['date','runs', 'wickets', 'overs', 'runs_last_5', 'wickets_last_5',
       'bat_team_Chennai Super Kings', 'bat_team_Delhi Daredevils',
       'bat_team_Kings XI Punjab', 'bat_team_Kolkata Knight Riders',
       'bat_team_Mumbai Indians', 'bat_team_Rajasthan Royals',
       'bat_team_Royal Challengers Bangalore', 'bat_team_Sunrisers Hyderabad',
       'bowl_team_Chennai Super Kings', 'bowl_team_Delhi Daredevils',
       'bowl_team_Kings XI Punjab', 'bowl_team_Kolkata Knight Riders',
       'bowl_team_Mumbai Indians', 'bowl_team_Rajasthan Royals',
       'bowl_team_Royal Challengers Bangalore',
       'bowl_team_Sunrisers Hyderabad',
       'total']]


X_train = x.drop(labels='total',axis=1)[x['date'].dt.year <= 2016]
X_test = x.drop(labels='total',axis=1)[x['date'].dt.year>=2017]


y_train = x[x['date'].dt.year<=2016]['total'].values

y_test = x[x['date'].dt.year>=2017]['total'].values


X_train.drop(labels='date',axis=True,inplace=True)
X_test.drop(labels='date',axis=True,inplace=True)


from sklearn.linear_model import LinearRegression

lm = LinearRegression()

lm.fit(X_train,y_train)

predicted = lm.predict(X_test)

p_df = pd.DataFrame(predicted)

sns.regplot(y_test,predicted)

from sklearn.metrics import r2_score

score = r2_score(y_test,predicted)

from sklearn import metrics

print("MSE:",metrics.mean_squared_error(y_test,predicted))
print("RMSE:",np.sqrt(metrics.mean_squared_error(y_test,predicted)))

df2 = pd.DataFrame(y_test)
df3 = pd.DataFrame(predicted)

filename = 'IPL_Score_prediction.pkl'
pickle.dump(lm,open(filename, 'wb'))
