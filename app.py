import requests
from views import api_jungle_toub, chome_jugle_toub, analyse_excel
from views import compare_multibple_product, group_analysis
from views import Initialisation
import streamlit as st
import seaborn as sns
sns.set()

# App Name
st.title('Jungle Toub')

# App Pages 
LISTE_PAGES = ('Api Jungule Toub', 'Comparer plusiseurs produits',
              'Chrome jungle Toub','Analyse de groupe','Analyse Excel')
add_selectbox = st.sidebar.selectbox('Faire votre choix', LISTE_PAGES)

# Premère page 'Api Jungule Toub'
if  (add_selectbox == 'Api Jungule Toub'):
  api_jungle_toub.api_amazon(Initialisation)

# 2e page "Chrome jungle Toub"
elif add_selectbox == 'Chrome jungle Toub':
  chome_jugle_toub.chome_jugle_toub(Initialisation)
  
# 3e page 'Comparer plusiseurs produits'
elif add_selectbox == 'Comparer plusiseurs produits':
  compare_multibple_product.compare_multibple_product(Initialisation)

# 4e pages 'Analyse Excel'
elif add_selectbox == 'Analyse Excel':
  analyse_excel.analyse_excel()
  
# 5e pages 'Analyse de groupe'
elif add_selectbox == 'Analyse de groupe':
  group_analysis.group_analysis(Initialisation)