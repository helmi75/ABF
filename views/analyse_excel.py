from . import __init__
import streamlit as st 
import pandas as pd
from millify import millify
from features import encodage_level_alphabet, encodage_level_numerique, nan_cleaning

# 4e pages 'Analyse Excel'
def analyse_excel():
    st.markdown("### Analysis of data from an Excel file\n - download the sample file from this link\n -  ")
    uploaded_file = st.file_uploader("Excel product data ") 
    excel_file = pd.read_excel(uploaded_file, sheet_name=None, index_col=None) 
    #excel_file = pd.read_csv(uploaded_file)  
    if excel_file:
        dexiemme_contener = st.container()
        premier_contener = st.container() 
        list_score_demande = []
        list_score_competition = []
        liste_score_JS_moy = []
        list_nom_produit = []
        liste_pays = []
        liste_vol_vente_mensuel = []
        liste_score_vol_vente_mensuel = []

        # new scoring 
        liste_score_pays = []# OK  
        liste_score__vol_vente_mensuel =[] #OK
        liste_score_coef =[] # next work 
        liste_score_saisonalite = [] 
        for xl_name in excel_file:
            #st.write(xl_name)
            #st.write(excel_file[xl_name])  
            st.header(xl_name)
            df = encodage_level_alphabet(excel_file[xl_name])    
            df_numerique = encodage_level_numerique(df)
            df_numerique, filtre = nan_cleaning(df_numerique)

            def deciamle(x):
                return millify (x, precision=2)   

            with st.expander("afficher le tableau "):
                if filtre.count(True) !=0 :
                    list_score_demande.append(deciamle(df_numerique['DEMANDE'].mean()))
                    list_score_competition.append(deciamle(df_numerique['COMPETITION'].mean()))
                    liste_score_JS_moy.append(deciamle(df_numerique['SCORE '].mean()))
                    list_nom_produit.append(xl_name)
                    liste_vol_vente_mensuel.append(df_numerique["Vol. de vente Mensuel"].sum())       
                    pays_choisi = excel_file[xl_name]['Pays'].apply(lambda x : x.upper())
                    st.write("**Chiffre basé sur les Marketplaces**:  ",'  ,  '.join(list(pays_choisi[filtre])))
                    liste_pays.append('  ,  '.join(list(pays_choisi[filtre])))
                    liste_score_pays.append(len(pays_choisi[filtre]))
                    

                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Demand Score ", f'{millify (df_numerique["DEMANDE"].mean(axis=0))}')
                    col2.metric("Score compet",  f'{millify (df_numerique["COMPETITION"].mean(axis=0))}')
                    col3.metric("Score JS", millify (df_numerique["SCORE "].mean(axis=0), precision=1))
                    col4.metric("Vol. de Vente moy/ mois ",
                                f'{millify (df_numerique["Vol. de vente Mensuel"].sum(), precision =3)}')
                
                    st.write(df_numerique)

                    col11, col12 = st.columns(2)
                    fig, ax1 = plt.subplots(1,1)
                    labels_pays = df_numerique['Pays']
                    values_vol_vente  = df_numerique['Vol. de vente Mensuel'].sort_index().values 
                    ax1.pie(values_vol_vente ,  labels=labels_pays, autopct='%1.1f%%')    
                    ax1.set_title( 'Volume de vente ' ,size=20)
                    col12.pyplot(fig)

                    #fig1, ax2 = plt.subplots()
                    df_saison = df_numerique.set_index('Pays').iloc[:,-12:].T
                
                    #st.dataframe(df_saison.T)
                    fig1=go.Figure()
                    for elm in df_saison.columns:        
                        fig1.add_trace(go.Scatter(x= df_saison[elm].index, 
                                            y= df_saison[elm],
                                            mode='lines+markers',
                                            name=elm,
                                            ))
                        fig1.update_layout(title_text='Demande mensuelle',  title_x=0.5)       
                        st.plotly_chart(fig1)
        

        
    
    
    

    scores_vol_vente_mensuel =  liste_vol_vente_mensuel/max(liste_vol_vente_mensuel)*9
    score_pays = []
    for score in liste_score_pays :
        score_pays.append(millify (score/max(liste_score_pays)*9, precision=2))

    

    result = pd.DataFrame([list_score_competition, 
                        list_score_demande,
                        liste_score_JS_moy,
                        scores_vol_vente_mensuel,
                        score_pays,
                        liste_pays,
                        liste_vol_vente_mensuel],                         
                        columns=(list_nom_produit),
                        index=['Score competition',
                                'Score demande',
                                'JS Score Moyen',
                                'Score vol vente /M',
                                'Score pays',
                                'Liste de pays ',
                                'Vol. de vente Mensuel'                                  
                                ])
    result = result.T

    result['Score vol vente /M'] = result['Score vol vente /M'].apply(lambda x : millify (x, precision=2))

    with dexiemme_contener :  
        option = ['Score competition', 'Score demande', 'JS Score Moyen', 
                'Score vol vente /M','Score pays'
                ]    

        score_selection = st.multiselect(label='Strategie', 
                                    options=option ,
                                    default=['Score competition', 'Score demande', 'JS Score Moyen', 
                                                'Score vol vente /M','Score pays'] )
    

    result_score = result[score_selection] # ajouter automatiquement 


    for elm in result_score.columns:
        result_score[elm] = result_score[elm].apply(lambda x : float(x))
        result_score_mean = result_score.mean(axis=1).sort_values(ascending=False)

    
        
        

        col11, col12 = st.columns(2)
    
        with premier_contener :  
            st.header("Classements produits")   
            fig , ax = plt.subplots(1,1, figsize=(12,7))
            plt.xticks(rotation = 90)
            
            sns.barplot( result_score_mean.index, result_score_mean.values)
            premier_contener.pyplot(fig)
            premier_contener.write(result_score_mean)    
    
        st.dataframe(result)