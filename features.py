import requests
import time as time
import pandas as pd
import numpy as np 
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import streamlit as st 









# scrapt data from API 
def scap_data(keyword, list_pays, nbr_pages, url, headers):  
  dict_reponse={}
  for pays in list_pays :    
    for i in range(1,nbr_pages+1):
      querystring = {"keywords":keyword,"region":pays,"page":str(i)}
      response = requests.request("GET", url, headers=headers, params=querystring)
      dict_reponse[pays+'_'+str(i)]=response
      time.sleep(1)
  return dict_reponse

def merge_dicts(a, b):
  m = a.copy()
  m.update(b)
  return m


def cleaning(reponse_api):

  #tranform from json to Dataframe
  d = reponse_api.json()
  df_search_result = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in d.items() ]))
  
  #store the result in the dataframe
  result_list=[]
  for elm in df_search_result['results']:
    result_list.append(elm)
  df_result = pd.DataFrame(result_list)

  # delate Nan in price and reviews columns
  df_result = df_result[~df_result['price'].isna()]
  df_result = df_result[~df_result['reviews'].isna()]

  #cleaning empty field
  liste_prix =[]
  for elm in df_result['price'] :
    if elm :
      liste_prix.append(elm)
  df_list_price = pd.DataFrame(liste_prix)


  liste_reviews =[]
  for elm in df_result['reviews'] :
    if elm :
      liste_reviews.append(elm)
  df_liste_reviews = pd.DataFrame(liste_reviews)
  df_finale= pd.concat([df_result,df_liste_reviews,df_list_price],axis=1)

  #reshape to the util dataframe
  df_utile = df_finale[['asin','title','prime','images','position','best_seller','avg_rating','num_ratings','amount','list_price','currency']]
  df_utile = df_utile[~df_utile['amount'].isnull()]

  #return a cleaned dataframe
  return df_utile

def affichage(data,country ,x ,y ):
  #affichage plotly

  fig = go.Figure(data=go.Scatter(x=data[x],
                                y=data[y],
                                mode='markers',
                                marker_color=data['avg_rating'],
                                text=data['title'])) # hover text goes here
  fig.update_layout(title=f' Note en fonction du prix {country}')  
  return fig


def preprocessing(df, langue):
  
  
  if langue == 'fr' :
    
    
    # Traitement des Revenues
    df["Honoraires"] = df["Honoraires"].replace('...', np.nan)
    df["Honoraires"] = df["Honoraires"].astype(float)

    # Traitement des ventes journalière 
    df['Ventes journalières'] = df['Ventes journalières'].replace('...', np.nan)
    df['Ventes journalières'] = df['Ventes journalières'].astype(float)

    # Traitement des ventes mensuelle 
    df['Revenus mensuels'] = df['Revenus mensuels'].replace('...', np.nan)
    df['Revenus mensuels'] = df['Revenus mensuels'].astype(float)
    # Traitement du temps 
    # codage des ... en nan  Date First Available
    df['Date de première disponibilité'] = df['Date de première disponibilité'].replace('...', np.nan)
    
    #supréssion des nan 
    df=df[df['Date de première disponibilité'].isna()==False]

    # encodage en datime 
    df['Date de première disponibilité'] = pd.to_datetime(df['Date de première disponibilité'])
    df = df[~df['Revenus mensuels'].isna()]

    df["LQS"] = df["LQS"].replace('...', np.nan)
    df["LQS"] = df["LQS"].astype(float)
    df = df[~df['LQS'].isna()]
    df['Revenus segementé'] = df['Revenus mensuels'].apply(lambda x : segmentation(x))
    df['Ventes mensuelles'] = df['Ventes mensuelles'].astype(float)
    df['Vendeurs'] = df['Vendeurs'].astype(float)

    

    
  else :
    
    df['D. Sales'] = df['D. Sales'].replace('...', np.nan)
    df['D. Sales'] = df['D. Sales'].astype(float)

    # Traitement des ventes mensuelle 
    df['Mo. Sales'] = df['Mo. Sales'].replace('...', np.nan)
    df['Mo. Sales'] = df['Mo. Sales'].astype(float)

    # Traitement des Revenues 
    df["Mo. Revenue"] = df["Mo. Revenue"].replace('...', np.nan)
    df["Mo. Revenue"] = df["Mo. Revenue"].astype(float)

    # Traitement du temps 
    # codage des ... en nan  Date First Available
    df['Date First Available'] = df['Date First Available'].replace('...', np.nan)

    #supréssion des nan 
    df=df[df['Date First Available'].isna()==False]

    # encodage en datime 
    df['Date First Available'] = pd.to_datetime(df['Date First Available'])

    # supression des NaN
    df = df[~df['Mo. Revenue'].isna()]
    df = df[~df['LQS'].isna()]
    df['Revenus segemented'] = df['Mo. Revenue'].apply(lambda x : segmentation(x))

  return df 

def segmentation2(x) :
    if x <= 100 :
      x= 'inféreiur à 100'
    elif (x>100) &  (x<=1000) :
      x ='entre 100 a 1K'
    elif (x>1000) &  (x<=5000) :
      x = 'entre 1K a 5K'
    elif (x>5000) &  (x<=10000) :
      x = 'entre 5K a 10K'
    elif (x>10000) &  (x<=20000) :
      x = 'entre 10K a 20K'
    elif (x>20000) &  (x<=50000) :
      x = 'entre 20K a 50K'
    elif x> 50000 :
      x = 'supérieur à 50K'
    else:
      x = 'negatif'
    return x

def segmentation(x):
  if x <= 1000 :
    x= 'inféreiur à 1K'
  elif (x>1000) &  (x<=10000) :
    x ='entre 1K a 10K'   
  elif (x>10000) &  (x<=50000) :
    x = 'entre 10K a 50K'
  elif x> 50000 :
    x = 'supérieur à 50K'
  else:
    x = 'negatif'
  return x

def dectection_langue(list_colum):
  text = " ".join(list_colum)
  texte1 = "[\r {\r\"id\": \"1\",\r\"language\": \"fr\",\r\"text\": \""+text+"\"\r}\r]"
  texte1 = texte1.replace("è",'e')
  texte1 = texte1.replace("é",'e')
  texte1 = texte1.replace("É",'e')  

  #Api detection langue  
  url = "https://language-detection4.p.rapidapi.com/language-detection"
  payload = texte1
  headers = {
                'content-type': "application/json",
                'accept': "application/json",
                'x-rapidapi-host': "language-detection4.p.rapidapi.com",
                'x-rapidapi-key': "f2b69e8ab2mshc6b37f3259eace5p104495jsnc2a8ef50efc6"
              }

  response = requests.request("POST", url, data=payload, headers=headers)
  return response.json()[0]['detected_languages'][0]['prediction']

def encodage_level_alphabet(df):
      code_pour_dist_demande = {'medium': '2_medium','high': '1_high','low':'3_low'}
      df['COMPETITION'] = df['COMPETITION'].map(code_pour_dist_demande)
      df['DEMANDE'] = df['DEMANDE'].map(code_pour_dist_demande)
      return df 

def encodage_level_numerique(df):
      code_pour_dist_demande = {'2_medium': (6), '1_high': (9), '3_low':(3)}
      code_pour_dist_competition = {'2_medium': (6), '1_high': (3), '3_low':(9)}
      df['COMPETITION'] = df['COMPETITION'].map(code_pour_dist_competition)
      df['DEMANDE'] = df['DEMANDE'].map(code_pour_dist_demande)
      return df

def nan_cleaning(dataframe):
    filtre=[]
    for elm in  dataframe.isna().sum(axis=1):
      if  (elm >= 0) & (elm <13) :
        filtre.append(True)
      if elm >= 13 :
        filtre.append(False)
     
    return dataframe[filtre], filtre









       
