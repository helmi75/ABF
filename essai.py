import streamlit as st
import pandas as pd 

y = 15
x = 4
a = 18
z = 65
liste_1 = ['valeur1 ', 'valeur2']
liste_2 = [y, x]
liste_3 = [a, z]

df = pd.DataFrame([liste_2, liste_2, liste_3], index =['one',' two','tree'], columns=['uno','due'])
st.dataframe(df)


    




options = st.multiselect(
     'What are your favorite colors', df.columns, default =['uno','due'])
for elm in options:
    st.write(elm)



