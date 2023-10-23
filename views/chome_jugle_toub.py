from . import __init__
import streamlit as st 
import pandas as pd 
from  features import dectection_langue, preprocessing
import seaborn as sns 
import matplotlib.pyplot as plt 

def chome_jugle_toub(Initialisation):
    init = Initialisation()
    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.header(uploaded_file.name[14:-4]) 
        df = df.iloc[:,3:]

        # detect data language 
        langue = dectection_langue(df.columns)  
        st.write(f'App {langue}')
        
        # data cleaning 
        df = preprocessing(df, langue) 
        st.subheader( f'\nNombre de produit : {df.shape[0]}\n')  
            
        
        
        # Plot data prosses
        labels = df['LQS'].value_counts().index
        sizes =df['LQS'].value_counts().values  
        st.subheader( '\n\n\n\nAnalyse Univarié')       
        if langue == 'fr':
            
            fig1, (ax1, ax2)  = plt.subplots(1,2,figsize=(12,10))
            ax1.pie(sizes,  labels=labels, autopct='%1.1f%%', shadow=False, startangle=50)    
            ax1.set_title( 'Répartition des notes de lising' ,size =20)    


            sns.distplot(df['Avis'], bins=10)
            ax2.set_title( 'Notes', size=20) 
            #st.pyplot(fig1)  

            #ax2.hist(df['Évaluation'],bins=10)
            #ax2.set_title( 'Histogramme des notes ' ,size =20)

            
            

            fig2, (ax3, ax4)  = plt.subplots(1,2,figsize=(12,10))
            df_prix_q075 =  df['Prix'][df['Prix']<df['Prix'].quantile(0.75)]
            ax3.boxplot(df_prix_q075 )
            ax3.set_title(f'\n Prix median {df_prix_q075.median()}€' ,size =20)

            df_Revenus_mensuels_q075 =  df['Revenus mensuels'][df['Revenus mensuels']<df['Revenus mensuels'].quantile(0.75)]    
            st.write(df['Revenus mensuels'].quantile(0.75))
            ax4.boxplot(df_Revenus_mensuels_q075)
            ax4.set_title(f'Revenue median {df_Revenus_mensuels_q075.median()}€',size =20)


            
            labels_revenu = df['Revenus segementé'].value_counts().index
            values_revenu  = df['Revenus segementé'].value_counts().values   
                    

            fig3, ax5  = plt.subplots(1,1,figsize=(12,5))  
                    
            ax5.pie(values_revenu ,  labels=labels_revenu, autopct='%1.1f%%', colors=init.couleurs, startangle=50)
            ax5.set_title('',size =20)

            fig4, ax6  = plt.subplots(1,1,figsize=(12,5))      
            sns.scatterplot( data=df, x='Classement', y='Ventes mensuelles', hue=df['Revenus segementé'])
            ax6.set_xlim(0,20000)
            ax6.set_title('Nbr de vente en fonction du classement ',size =20)

            
            fig5, ax7  = plt.subplots(1,1,figsize=(12,5))      
            sns.scatterplot( data=df, x='Ventes mensuelles', y='Évaluation', hue=df['Revenus segementé'])
            ax7.set_title('influence du chiffre d affaire   M.vente(evalutation)',size =20)

            fig8, ax9  = plt.subplots(1,1,figsize=(12,5))      
            sns.scatterplot( data=df, x='Avis', y='Classement', hue=df['Revenus segementé'])
            ax9.set_xlim(-2,6000)
            #ax9.set_ylim(-10,5000)
            ax9.set_title('influence du chiffre d affaire avis(classement)',size =20)

            st.pyplot(fig1)
            st.pyplot(fig2)
            st.pyplot(fig3)
            st.pyplot(fig4)
            st.pyplot(fig5)
            st.pyplot(fig8)

            

        else :
            fig1, (ax1, ax2)  = plt.subplots(1,2,figsize=(12,10))
            ax1.pie(sizes,  labels=labels, autopct='%1.1f%%', shadow=False, startangle=50)    
            ax1.set_title( 'Répartition des notes de lising' ,size =20)

            ax2.hist(df['Rating'],bins=10)
            ax2.set_title( 'Histogramme des notes ' ,size =20)

            fig2, (ax3, ax4)  = plt.subplots(1,2,figsize=(12,10))
            df_prix_q075 =  df['Price'][df['Price']< df ['Price'].quantile(0.75)]
            ax3.boxplot(df_prix_q075 )
            ax3.set_title( f'\nBoxplot prix :  ' ,size =20)

            df_Revenus_mensuels_q075 =  df['Mo. Sales'][df['Mo. Sales']< df ['Mo. Sales'].quantile(0.75)]    
            ax4.boxplot(df_Revenus_mensuels_q075)
            ax4.set_title('Boxplot revenue',size =20)

            st.pyplot(fig1)
            st.pyplot(fig2)
            #st.pyplot(fig3)
            st.pyplot(fig4)
            st.pyplot(fig5)
            st.pyplot(fig8)

            
            st.subheader( '\n\n\n\nAnalyse ')
            

            
        
        
        
        