from . import __init__
import streamlit as st 
from  features import scap_data, cleaning, affichage

def api_amazon(Initialisation):
  
  init = Initialisation()
  st.markdown("### Price decision tool ")
  search  = st.text_input('enter a product name from Amazon website')
  if search :
    dict_reponse = scap_data(search, init.list_pays ,init.nbr_pages ,init.url ,init.headers)
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

    
if __name__ == "_main__":
    pass