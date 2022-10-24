import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff
import altair as alt
import snscrape.modules.twitter as sntwitter
import pandas as pd
import numpy as np
import pickle
from wordcloud import WordCloud, STOPWORDS
from scipy.special import softmax
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

@st.experimental_memo
def load_data(path):
    df = pd.read_csv(path, warn_bad_lines=True, error_bad_lines=False,low_memory=False)
    return df

@st.experimental_memo
def clean(df):
    df['Location'] = df['Location'].replace(np.nan,'Autre')
    return df

def value_classification(df):
    df_value_classification = df.groupby('Classification')['Classification'].count()
    df_value_classification = df_value_classification.sort_values(ascending=False)
    fig = px.bar(df_value_classification.head(20), hover_name = df_value_classification.head(20).index, title='Pourcentage of all classification')
    st.plotly_chart(fig)

def value_tweet(df):
    df_group_user = df.groupby('User')['User'].count()
    df_group_user = df_group_user.sort_values(ascending=False)
    fig = px.funnel(df_group_user.head(10),hover_name = df_group_user.head(10).index, title='Number of tweet according account')
    st.plotly_chart(fig)

def reply_class(df):
    fig = px.pie(df, values='Reply', names = 'Classification', hover_name = df.index, title='Pourcentage of reply for all users')
    st.plotly_chart(fig)

def retweet_class(df):
    fig = px.pie(df, values='Retweeet', names = 'Classification', hover_name = df.index, title='Pourcentage of retweet for all users')
    st.plotly_chart(fig)

####################### MAIN ####################################

def main():

    st.title("Data Camp Project 2022")
    st.header("This is the dataframe after scraping data from twitter :")
    df = load_data('project.csv')
    df = clean(df)

    st.dataframe(df)

    cloud = st.checkbox('Print the Wordcloud from the 19-10-2022')
    cloud2 = st.checkbox('Print the Wordcloud from the 17-10-2022')
    checkbox1 = st.checkbox('Print the pourcentage of reply')
    checkbox2 = st.checkbox('Print the pourcentage of retweet')

    if cloud:
        st.write('Wordcloud of 19-10-2022')
        st.image('wordcloud.PNG')

    if cloud2:
        st.write('Wordcloud of 17-10-2022')
        st.image('wordcloud1.PNG')

    if checkbox1:
        reply_class(df)
    if checkbox2:
        retweet_class(df)

    check_graph = ["Ligne1_RATP","Ligne2_RATP","Ligne3_RATP","Ligne4_RATP","Ligne5_RATP","Ligne6_RATP","Ligne7_RATP","Ligne8_RATP","Ligne9_RATP","Ligne10_RATP","Ligne11_RATP","Ligne12_RATP","Ligne13_RATP","Ligne14_RATP"]

    choice = st.selectbox("Line selected", check_graph)

    def line_choice(df,choice) :
        df_l8 = df[df["User"]==choice]
        df_l8 = clean(df_l8)
        return df_l8

    df_l = line_choice(df,choice) 

    with st.sidebar :
        st.write("Project by Laura Benavenuto, Victor Delaroque et Vincent Eung")

    st.header('There is all the graph created for each line')
    st.write(df_l)

    st.subheader('GRaph 1')
    reply_class(df_l)

    st.subheader('GRaph 2')
    value_classification(df_l)

    st.subheader('GRaph 3')
    value_tweet(df)

    



main()
