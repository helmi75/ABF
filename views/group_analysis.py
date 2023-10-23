
from . import __init__
import streamlit as st 
from  features import  preprocessing
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns 

def group_analysis(Initialisation):
    init = Initialisation()
    
    files =st.file_uploader('Choose files ', accept_multiple_files=True)
    if files:
      list_niche=[]
      for elm in files:      
        df = pd.read_csv(elm) 
        df = df.iloc[:,3:]    
        df = preprocessing(df, 'fr')       
        list_niche.append(df)  
    
      df = pd.concat(list_niche)
      df = df[~df['Évaluation'].isna()]
      df = df[~df['Honoraires'].isna()]
    
    
      st.write(f'Nbr d individu à analyser {df.shape[0]}') 
      # plot configuration 
      fig1,(ax1, ax2, ax3) = plt.subplots(1,3,figsize=(20, 7))
    
      plt.xticks(rotation = 90)
    
      labels_LQS = df['LQS'].apply(lambda x : str(x)).value_counts().sort_index().index
      values_LQS  = df['LQS'].value_counts().sort_index().values       
      # Plot Pie of listing score 
      ax1.pie(values_LQS ,  labels=labels_LQS, autopct='%1.1f%%', colors=init.couleurs, startangle=50)    
      ax1.set_title( 'Lising' ,size=20)   
      
      labels_revenu = df['Revenus segementé'].value_counts().sort_index().index
      values_revenu  = df['Revenus segementé'].value_counts().values   
          

      #plot pie of revenues 
      ax2.pie(values_revenu, labels = labels_revenu ,autopct='%1.1f%%', colors=init.couleurs, startangle=50)
      # sns.distplot(dict_niche[nom_file]['Revenus segementé'],bins=10)           
      ax2.set_title( 'Revenus ' ,size =20)
          
      # Histograme of evaluation 
      sns.distplot(df['Évaluation'], bins=10)
      ax3.set_title( 'Notes', size=20) 
      st.pyplot(fig1)

      fig4, ax6  = plt.subplots(1,1,figsize=(12,5))      
      sns.scatterplot( df['Classement'],df['Ventes mensuelles'], hue=df['Revenus segementé'])
      ax6.set_xlim(0,20000)
      ax6.set_title('Nbr de vente en fonction du classement ',size =20)
      st.pyplot(fig4)

        
      fig5, ax7  = plt.subplots(1,1,figsize=(12,5))      
      sns.scatterplot(df['Ventes mensuelles'], df['Évaluation'], hue=df['Revenus segementé'])
      ax7.set_title('influence du chiffre d affaire   M.vente(evalutation)',size =20)
      st.pyplot(fig5)   

      fig9, ax10  = plt.subplots(1,1,figsize=(12,5)) 

      st.header('influence du chiffre d affaire avis(classement)')
      sns.scatterplot( df['Classement'] ,df['Avis'], hue=df['Revenus segementé']) 
      variation_x= st.slider('zoom du classement', min_value=0, 
                             max_value= int(df['Classement'].max()), 
                             value=int(df['Classement'].quantile(1)))
      ax10.set_xlim(0,variation_x)

      variation_y= st.slider('zoom de l\'avis', min_value=0, 
                             max_value= int(df['Avis'].max()), 
                             value=int(df['Avis'].quantile(1)))
      ax10.set_ylim(-10,variation_y)
      ax10.set_title('influence du chiffre d affaire avis(classement)',size =20)  
      st.pyplot(fig9)