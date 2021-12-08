import requests
from  features import *
import streamlit as st
import json
import pandas as pd 
import seaborn as sns
import io
from millify import millify 
from millify import millify
sns.set()

# configuration 
url = "https://parazun-amazon-data.p.rapidapi.com/search/"
headers = {
    'x-rapidapi-host': "parazun-amazon-data.p.rapidapi.com",
    'x-rapidapi-key': rapid_key
    }
list_pays = ['FR']
nbr_pages = 2



add_selectbox = st.sidebar.selectbox('Faire votre choix ',
                                      ('Chrome jungle Zboub',
                                      'Api Jungule Zboub',
                                      'Comparer plusiseurs produits',
                                      'Analyse Excel',
                                      'Analyse de groupe'
                                      ))

st.title('Jungle Zboub')
couleurs = ['#D56149','#49B5D5','yellow','green']#,'gray','pink','orange']  
# Premère page 'Api Jungule Zboub'
if  (add_selectbox == 'Api Jungule Zboub'):
  search  = st.text_input('entrer un nom de produit')
  if search :
    dict_reponse = scap_data(search, list_pays ,nbr_pages ,url ,headers)
    list_concat =[]
    for elm in dict_reponse:
      #cleanning dataset drop nan 
      globals() ['df_cleaned_'+ elm ]= cleaning(dict_reponse[elm])
      list_concat.append(globals() ['df_cleaned_'+ elm ])

    #plot data on scatter and boplot 
    df_util= pd.concat(list_concat,axis=0)

    # affichage de dataframe
    st.dataframe(df_util)
    st.subheader(f'Nbr de concurents :  {df_util.shape[0]}')

    #affichage de scatter
    st.markdown('**Moyenne etoiles ** en fonction du **Prix**.')

    fig_plotly = affichage(df_util ,'FR','amount','avg_rating')
    st.plotly_chart(fig_plotly)

    # affiche  boxplot Prix 
    st.markdown('**Distribution** du **prix mediant**')
    fig, ax = plt.subplots(figsize=(15,7))
    ax.boxplot(df_util['amount'],vert=False,patch_artist =True,showmeans =True )
    st.pyplot(fig)

    # affiche  histograme prix 
    st.markdown('**Histograme** des **prix **')
    fig1, ax1 = plt.subplots(figsize=(15,7))
    ax1.hist(df_util['amount'], bins=40 )
    st.pyplot(fig1)

    # affiche Histo des  moyenne des etoiles 
    st.markdown('**Histograme** des **moyenne des etoiles **')
    fig2, ax2 = plt.subplots(figsize=(15,7))
    ax2.hist(df_util['avg_rating'], bins=40 )
    st.pyplot(fig2)
# Deuxiemme page "Chrome jungle Zboub"
elif add_selectbox == 'Chrome jungle Zboub':
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


      sns.distplot(df['Évaluation'], bins=10)
      ax2.set_title( 'Notes', size=20) 
      #st.pyplot(fig1)  

      #ax2.hist(df['Évaluation'],bins=10)
      #ax2.set_title( 'Histogramme des notes ' ,size =20)


      fig2, (ax3, ax4)  = plt.subplots(1,2,figsize=(12,10))
      df_prix_q075 =  df['Prix'][df['Prix']< df ['Prix'].quantile(0.75)]
      ax3.boxplot(df_prix_q075 )
      ax3.set_title(f'\n Prix median {df_prix_q075.median()}€' ,size =20)

      df_Revenus_mensuels_q075 =  df['Revenus mensuels'][df['Revenus mensuels']< df ['Revenus mensuels'].quantile(0.75)]    
      ax4.boxplot(df_Revenus_mensuels_q075)
      ax4.set_title(f'Revenue median {df_Revenus_mensuels_q075.median()}€',size =20)


      
      labels_revenu = df['Revenus segementé'].value_counts().sort_index().index
      values_revenu  = df['Revenus segementé'].value_counts().values   

      fig3, ax5  = plt.subplots(1,1,figsize=(12,5))  
             
      ax5.pie(values_revenu ,  labels=labels_revenu, autopct='%1.1f%%', colors=couleurs, startangle=50)
      ax5.set_title('',size =20)

      fig4, ax6  = plt.subplots(1,1,figsize=(12,5))      
      sns.scatterplot( df['Classement'],df['Ventes mensuelles'], hue=df['Revenus segementé'])
      ax6.set_xlim(0,20000)
      ax6.set_title('Nbr de vente en fonction du classement ',size =20)

      
      fig5, ax7  = plt.subplots(1,1,figsize=(12,5))      
      sns.scatterplot(df['Ventes mensuelles'], df['Évaluation'], hue=df['Revenus segementé'])
      ax7.set_title('influence du chiffre d affaire   M.vente(evalutation)',size =20)

      fig8, ax9  = plt.subplots(1,1,figsize=(12,5))      
      sns.scatterplot( df['Avis'],df['Classement'], hue=df['Revenus segementé'])
      ax9.set_xlim(-2,6000)
      #ax9.set_ylim(-10,5000)
      ax9.set_title('influence du chiffre d affaire avis(classement)',size =20)

      

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

      
    st.subheader( '\n\n\n\nAnalyse ')
    

    st.pyplot(fig1)
    st.pyplot(fig2)
    st.pyplot(fig3)
    st.pyplot(fig4)
    st.pyplot(fig5)
    st.pyplot(fig8)
# 3e page 'Comparer plusiseurs produits'
elif add_selectbox == 'Comparer plusiseurs produits':
 
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
        ax1.pie(values_LQS ,  labels=labels_LQS, autopct='%1.1f%%', colors=couleurs, startangle=50)    
        ax1.set_title( 'Lising' ,size=20)   
        
        labels_revenu = dict_niche[nom_file]['Revenus segementé'].value_counts().sort_index().index
        values_revenu  = dict_niche[nom_file]['Revenus segementé'].value_counts().values         

        #plot pie of revenues 
        ax2.pie(values_revenu, labels = labels_revenu ,autopct='%1.1f%%', colors=couleurs, startangle=50)
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
        ax1.pie(values_LQS ,  labels=labels_LQS, autopct='%1.1f%%', colors=couleurs, startangle=50)    
        ax1.set_title( 'Listing' ,size =20) 

        labels_revenu = dict_niche[nom_file]['Revenus segemented'].value_counts().sort_index().index
        values_revenu  = dict_niche[nom_file]['Revenus segemented'].value_counts().values  
      
        #plot pie of revenues 
        ax2.pie(values_revenu, labels = labels_revenu ,autopct='%1.1f%%', colors =couleurs, startangle=50)   
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
        median_avis.append(dict_niche[nom_file]['Reviews'].median())
        median_listing.append(dict_niche[nom_file]['LQS'].median())
    
    df_conclustion =pd.DataFrame(data=[moyenne_note, median_revenu_mensuel, median_classement,median_avis, median_listing],columns=list_nom, index=['Rating','Mo. Revenue ','Rank ','Reviews','LQS '] ).transpose()
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
# 4e pages 'Analyse Excel'
elif add_selectbox == 'Analyse Excel':
  uploaded_file = st.file_uploader("Choose a file") 
  excel_file = pd.read_excel(uploaded_file, sheet_name=None, index_col=None)   


  list_score_demande = []
  list_score_competition = []
  liste_score_JS_moy = []
  list_nom_produit = []
  liste_pays=[]
  
  for xl_name in excel_file:
    #st.write(xl_name)
    #st.write(excel_file[xl_name])  
    st.header(xl_name)
    df = encodage_level_alphabet(excel_file[xl_name])    
    df_numerique = encodage_level_numerique(df)
    df_numerique, filtre = nan_cleaning(df_numerique)

    def deciamle(x):
      return millify (x, precision=2)
    
    
    
    
    
    if filtre.count(True) !=0 :
      list_score_demande.append(deciamle(df_numerique['DEMANDE'].mean()))
      list_score_competition.append(deciamle(df_numerique['COMPETITION'].mean()))
      liste_score_JS_moy.append(deciamle(df_numerique['SCORE '].mean()))
      list_nom_produit.append(xl_name)


      pays_choisi = excel_file[xl_name]['Pays'].apply(lambda x : x.upper())
      st.write("**Chiffre basé sur les Marketplaces**:  ",'  ,  '.join(list(pays_choisi[filtre])))
      liste_pays.append('  ,  '.join(list(pays_choisi[filtre])))
      col1, col2, col3, col4 = st.columns(4)
      col1.metric("Demand Score ", f'{millify (df_numerique["DEMANDE"].mean(axis=0))}')
      col2.metric("Score compet",  f'{millify (df_numerique["COMPETITION"].mean(axis=0))}')
      col3.metric("Score JS", millify (df_numerique["SCORE "].mean(axis=0), precision=1) )
      col4.metric("Vol. de Vente moy/ mois ", f'{millify (df_numerique["Vol. de vente Mensuel"].sum(), precision =3)}' )
    with st.expander("afficher les données "):
      st.write(df_numerique)
    
    result = pd.DataFrame([list_score_competition, list_score_demande, liste_score_JS_moy, liste_pays],
                          columns=(list_nom_produit),
                          index=['score competition','Score demande','JS Score Moyen', 'Liste de pays '])

  
  st.write(result.T)

      

# 5e pages 'Analyse de groupe'
elif add_selectbox == 'Analyse de groupe':
  files =st.file_uploader('Choose files ', accept_multiple_files=True)
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
  ax1.pie(values_LQS ,  labels=labels_LQS, autopct='%1.1f%%', colors=couleurs, startangle=50)    
  ax1.set_title( 'Lising' ,size=20)   
    
  labels_revenu = df['Revenus segementé'].value_counts().sort_index().index
  values_revenu  = df['Revenus segementé'].value_counts().values   
        

  #plot pie of revenues 
  ax2.pie(values_revenu, labels = labels_revenu ,autopct='%1.1f%%', colors=couleurs, startangle=50)
  #sns.distplot(dict_niche[nom_file]['Revenus segementé'],bins=10)           
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
  variation_x= st.slider('zoom du classement', min_value=0, max_value= int(df['Classement'].max()), value=int(df['Classement'].quantile(1)))
  ax10.set_xlim(0,variation_x)
  variation_y= st.slider('zoom de l\'avis', min_value=0, max_value= int(df['Avis'].max()), value=int(df['Avis'].quantile(1)))
  ax10.set_ylim(-10,variation_y)
  ax10.set_title('influence du chiffre d affaire avis(classement)',size =20)  
  st.pyplot(fig9)
