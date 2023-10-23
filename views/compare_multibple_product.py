from . import __init__
import streamlit as st 
import pandas as pd 
from  features import dectection_langue, preprocessing
import matplotlib.pyplot as plt 
import seaborn as sns 


# 3e page 'Comparer plusiseurs produits'
def compare_multibple_product(Initialisation):
    init = Initialisation()
    files =st.file_uploader('Choose files ', accept_multiple_files=True)
    dict_niche={}
    if files :
        st.header('Niche à comparer\n\n!\n')

        list_nom = []
        moyenne_note = [] 
        median_revenu_mensuel = []
        median_avis = []
        median_classement = []
        median_listing = []

        for elm in files:      
            nom_file = elm.name[14:-4]
            dict_niche[nom_file] = pd.read_csv(elm)
            langue = dectection_langue(dict_niche[nom_file].iloc[:,3:]) 
            dict_niche[nom_file] = preprocessing(dict_niche[nom_file].iloc[:,3:], langue) 
            dict_niche[nom_file]['LQS']= dict_niche[nom_file]['LQS'].apply(lambda x : str(x))
            labels_LQS = dict_niche[nom_file]['LQS'].apply(lambda x : str(x)).value_counts().sort_index().index
            values_LQS  = dict_niche[nom_file]['LQS'].value_counts().sort_index().values
          
        
    
            # from french datas 
            if langue == 'fr':
                # plot configuration 
                fig1,(ax1, ax2, ax3) = plt.subplots(1,3,figsize=(20, 7))
                fig1.suptitle(nom_file, size=40)
                plt.xticks(rotation = 90)
                
                # Plot Pie of listing score 
                ax1.pie(values_LQS ,  labels=labels_LQS, autopct='%1.1f%%', colors=init.couleurs, startangle=50)    
                ax1.set_title( 'Lising' ,size=20)   
                
                labels_revenu = dict_niche[nom_file]['Revenus segementé'].value_counts().sort_index().index
                values_revenu  = dict_niche[nom_file]['Revenus segementé'].value_counts().values         

                #plot pie of revenues 
                ax2.pie(values_revenu, labels = labels_revenu ,autopct='%1.1f%%', colors=init.couleurs, startangle=50)
                #sns.distplot(dict_niche[nom_file]['Revenus segementé'],bins=10)           
                ax2.set_title( 'Revenus ' ,size =20)
                
                # Histograme of evaluation 
                sns.distplot(dict_niche[nom_file]['Évaluation'], bins=10)
                ax3.set_title( 'Notes', size=20) 
                st.pyplot(fig1)

                #french
                list_nom.append(nom_file)
                moyenne_note.append(dict_niche[nom_file]['Évaluation'].median())
                median_revenu_mensuel.append(dict_niche[nom_file]['Revenus mensuels'].median())
                median_classement.append(dict_niche[nom_file]['Classement'].median())
                median_avis.append(dict_niche[nom_file]['Avis'].median())
                median_listing.append(dict_niche[nom_file]['LQS'].median())


            # from english datas  
            else:   

                # plot configuration 
                fig1, (ax1 ,ax2, ax3) = plt.subplots(1, 3, figsize=(20,7))
                fig1.suptitle(nom_file, size=40)
                plt.xticks(rotation = 90)    

                # Plot Pie of listing score     
                ax1.pie(values_LQS ,  labels=labels_LQS, autopct='%1.1f%%', colors=init.couleurs, startangle=50)    
                ax1.set_title( 'Listing' ,size =20) 

                labels_revenu = dict_niche[nom_file]['Revenus segemented'].value_counts().sort_index().index
                values_revenu  = dict_niche[nom_file]['Revenus segemented'].value_counts().values  
            
                #plot pie of revenues 
                ax2.pie(values_revenu, labels = labels_revenu ,autopct='%1.1f%%', colors =init.couleurs, startangle=50)   
                #sns.distplot(dict_niche[nom_file]['Revenus segemented'],bins=10)     
                ax2.set_title( 'Revenus ' ,size =20)  

                # Histograme of evaluation
                sns.distplot(dict_niche[nom_file]['Rating'],bins=10)
                ax3.set_title( 'Notes ' ,size =20)    
                st.pyplot(fig1)

                #english
                list_nom.append(nom_file)
                moyenne_note.append(dict_niche[nom_file]['Rating'].median())
                median_revenu_mensuel.append(dict_niche[nom_file]['Mo. Revenue'].median())
                median_classement.append(dict_niche[nom_file]['Rank'].median())
                st.write(dict_niche[nom_file].columns)
                median_avis.append(dict_niche[nom_file]['Reviews'].median())
                median_listing.append(dict_niche[nom_file]['LQS'].median())
            
            df_conclustion =pd.DataFrame(data=[moyenne_note, median_revenu_mensuel, median_classement,median_avis, median_listing],
                                         columns=list_nom, index=['Rating','Mo. Revenue ','Rank ','Reviews','LQS '] ).transpose()
            st.dataframe(df_conclustion)


        
        

        
        fig6, ax8  = plt.subplots(1, 1, figsize=(20,7))
        sns.distplot(dict_niche[files[0].name[14:-4]]['Évaluation'],bins=10, label=files[0].name[14:-4])
        sns.distplot(dict_niche[files[1].name[14:-4]]['Évaluation'],bins=10, label=files[1].name[14:-4])
        sns.distplot(dict_niche[files[2].name[14:-4]]['Évaluation'],bins=10, label=files[2].name[14:-4])
        sns.distplot(dict_niche[files[3].name[14:-4]]['Évaluation'],bins=10, label=files[3].name[14:-4])
        ax8.set_title( 'Notes ' ,size =20)  
        ax8.legend()  
        st.pyplot(fig6)

        
        
        fig7, ax8  = plt.subplots(1, 1, figsize=(20,7))
        sns.distplot(dict_niche[files[3].name[14:-4]]['Revenus segementé'].value_counts(),bins=10, label=files[0].name[14:-4])
        sns.distplot(dict_niche[files[1].name[14:-4]]['Revenus segementé'].value_counts(),bins=10, label=files[1].name[14:-4])
        sns.distplot(dict_niche[files[2].name[14:-4]]['Revenus segementé'].value_counts(),bins=10, label=files[2].name[14:-4])
        sns.distplot(dict_niche[files[3].name[14:-4]]['Revenus segementé'].value_counts(),bins=10, label=files[3].name[14:-4])
        ax8.set_title( 'Notes ' ,size =20) 
        #ax8.set_xlim(-10000,10000) 
        ax8.legend()  
        st.pyplot(fig7)
    