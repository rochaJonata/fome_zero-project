# ==========================
# Importando as bibliotecas

import pandas as pd
import streamlit as st
from PIL import Image

from streamlit_folium import folium_static

#Para desenhar gráficos
import plotly.express as px
import plotly.graph_objects as go

#Para desenhar um mapa
import folium as fl
from folium.plugins import MarkerCluster

from haversine import haversine

import inflection

st.set_page_config(page_title='Cuisines', page_icon=':knife_fork_plate:', layout='wide')

# ====================
# Funções
# ====================

def st_metric(df, linha):

    df_aux = df.loc[:, ['restaurant_id', 'restaurant_name', 'country_code', 'city', 'cuisines', 'average_cost_for_two', 'currency', 'aggregate_rating']]

    df_aux = df_aux.sort_values('aggregate_rating', ascending=False).reset_index(drop=True)

    df_aux = df_aux.loc[:, ['restaurant_id', 'restaurant_name', 'country_code', 'city', 'cuisines', 'average_cost_for_two', 'currency', 'aggregate_rating']].groupby(['country_code', 'city', 'average_cost_for_two', 'currency', 'restaurant_name', 'cuisines', 'aggregate_rating']).count().reset_index()

    df_aux = df_aux.sort_values('aggregate_rating', ascending=False).reset_index(drop=True)

    df_aux = df_aux.head(5).reset_index(drop=True)
    
    return st.metric(label=(df_aux.loc[linha, 'cuisines']+': '+df_aux.loc[linha, 'restaurant_name']), value=(str(df_aux.loc[linha, 'aggregate_rating'])+'/5.0'), help=('País: '+df_aux.loc[linha, 'country_code']+'\n\nCidade: '+df_aux.loc[linha, 'city']+'\n\nMédia Prato para dois: '+str(df_aux.loc[linha, 'average_cost_for_two'])+' ('+df_aux.loc[linha, 'currency']+')'))


def gerar_grafico_barras(df, ordenar, qtd_restaurant, titulo_grafico):
    
    df_aux = round(df.loc[:, ['cuisines', 'aggregate_rating']].groupby('cuisines').mean().reset_index(), 2)
    
    df_aux = df_aux.sort_values('aggregate_rating', ascending=ordenar).head(qtd_restaurant)
    
    df_aux.columns = ['Tipo de Culinária', 'Média da Avaliação Média']
    
    grafico_barras = px.bar(df_aux, x='Tipo de Culinária', y='Média da Avaliação Média', text_auto=True).update_layout(title={'text':('Top '+str(qtd_restaurant)+titulo_grafico),'x': 0.5, 'xanchor':'center', 'yanchor':'top'})
    
    return grafico_barras

def rename_columns(dataframe):
    
    """ Esta função é responsável por renomear as colunas do DataFrame
        
        Input: DataFrame
        Output: DataFrame
    """
    
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    
    return df

def color_name(color_code):
    
    """ Esta função é responsável por converter uma representação hexadecimal de cores em nomes das cores  
        
        Exemplo:
        
        A cor 3F7E00 significa darkgreen
        
        Input: str
        Output: str
    """
    
    # Criação do nome das Cores
    COLORS = {
        "3F7E00": "darkgreen",
        "5BA829": "green",
        "9ACD32": "lightgreen",
        "CDD614": "orange",
        "FFBA00": "red",
        "CBCBC8": "darkred",
        "FF7800": "darkred",
    }
    
    return COLORS[color_code]

def create_price_tye(price_range):
    
    """ Esta função é responsável por converter o price range em cheap, normal, expensive ou gourmet  
        
        Exemplo:
        
        Price range é 1 corresponde a cheap
        
        Input: int
        Output: str
    """
    
    if price_range == 1:
        return "cheap"
    
    elif price_range == 2:
        
        return "normal"
    elif price_range == 3:
        return "expensive"
    
    else:
        return "gourmet"

def country_name(country_id):
    
    """ Esta função é responsável por converter o código do país em nome do país correspondente 
        
        Exemplo:
        
        Código 1 corresponde ao país India
        
        Input: int
        Output: str
    """
    
    COUNTRIES = {
        1: "India",
        14: "Australia",
        30: "Brazil",
        37: "Canada",
        94: "Indonesia",
        148: "New Zeland",
        162: "Philippines",
        166: "Qatar",
        184: "Singapure",
        189: "South Africa",
        191: "Sri Lanka",
        208: "Turkey",
        214: "United Arab Emirates",
        215: "England",
        216: "United States of America",
    }
    
    return COUNTRIES[country_id]

def clean_code(df_orig):
    
    """ Esta função tem a responsabilidade de limpar e tratar o dataframe 
        
        Tipos de limpeza:
        1. Remover coluna desnecessária
        2. Renomeando as colunas do DataFrame
        3. Selecionando o primeiro valor da separação de string por vírgula e atribuindo ao Dataframe
        4. Remover os espaços das string
        5. Excluir as linhas vazias
        6. Redefinir o índice do DataFrame
        7. Conversões de dados
        
        Input: Dataframe
        Output: Dataframe
    """
    
    # 1. Depois de ter analisado os dados da coluna, definimos que a coluna era desnecessaria, portanto removemos ela. 
    df_orig = df_orig.drop('Switch to order menu', axis='columns')
    
    # 2. Renomeando as colunas do DataFrame
    df = rename_columns(df_orig)
    
    # 3. Selecionando o primeiro valor da separação de string por vírgula e atribuindo ao Dataframe
    df['cuisines'] = df.loc[:, 'cuisines'].apply(lambda x: str(x).split(",")[0])
    
    # 4. Remover os espaços das string
    colunas = ['restaurant_id', 'restaurant_name', 'country_code', 'city', 'address', 'locality', 'locality_verbose', 'longitude', 'latitude', 'cuisines', 'average_cost_for_two', 'currency', 'has_table_booking', 'has_online_delivery', 'is_delivering_now', 'price_range', 'aggregate_rating', 'rating_color', 'rating_text', 'votes']

    # for coluna in colunas:
    #     df.loc[:, coluna] = df.loc[:, coluna].str.strip(" ")

    # 5. Excluir as linhas vazias
    for colum in colunas:
        df = df.loc[(df[colum] != 'NaN') & (df[colum] != 'nan') & (df[colum] != 'NaN ') & (df[colum] != 'nan '), :]
    
    # 6. Redefinir o índice do DataFrame
    df = df.reset_index(drop=True)
    
    # 7. Conversões de dados
    
    for x in range(len(df.loc[:, ['country_code', 'price_range', 'rating_color']])):
        df.loc[x, 'country_code'] = country_name(df.loc[x, 'country_code'])
        df.loc[x, 'price_range'] = create_price_tye(df.loc[x, 'price_range'])
        df.loc[x, 'rating_color'] = color_name(df.loc[x, 'rating_color'])
    
    return df

# --------------------- Inicio da Estrutura logica do código --------

# ====================
# Carregando o dataset
# ====================

#Importando o arquivo
df_orig = pd.read_csv('dataset/zomato.csv')

# ==================
# Limpando os dados
# ====================

df = clean_code(df_orig)

# ==================== Visão dos Tipos Culinários ====================

# ====================
# Barra Lateral

st.sidebar.markdown("## Filters")

countries_options = st.sidebar.multiselect('Choose the countries you want to view the information', ['Philippines', 'Brazil', 'Australia', 'United States of America', 'Canada', 'Singapure', 'United Arab Emirates', 'India', 'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa', 'Sri Lanka', 'Turkey'], default=['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia'])

#Filtro de paises
df = df.loc[df['country_code'].isin(countries_options), :]

#Filtro de quantidade de restaurantes
qtd_restaurant = st.sidebar.slider('Select the number of Restaurants you want to view', 1, 20, 10)

#Filtro de tipos de culinárias
cuisines_options = st.sidebar.multiselect('Choose types of cuisine', ['Italian', 'European', 'Filipino', 'American', 'Korean', 'Pizza',
       'Taiwanese', 'Japanese', 'Coffee', 'Chinese', 'Seafood',
       'Singaporean', 'Vietnamese', 'Latin American', 'Healthy Food',
       'Cafe', 'Fast Food', 'Brazilian', 'Argentine', 'Arabian', 'Bakery',
       'Tex-Mex', 'Bar Food', 'International', 'French', 'Steak',
       'German', 'Sushi', 'Grill', 'Peruvian', 'North Eastern',
       'Ice Cream', 'Burger', 'Mexican', 'Vegetarian', 'Contemporary',
       'Desserts', 'Juices', 'Beverages', 'Spanish', 'Thai', 'Indian',
       'Mineira', 'BBQ', 'Mongolian', 'Portuguese', 'Greek', 'Asian',
       'Author', 'Gourmet Fast Food', 'Lebanese', 'Modern Australian',
       'African', 'Coffee and Tea', 'Australian', 'Middle Eastern',
       'Malaysian', 'Tapas', 'New American', 'Pub Food', 'Southern',
       'Diner', 'Donuts', 'Southwestern', 'Sandwich', 'Irish',
       'Mediterranean', 'Cafe Food', 'Korean BBQ', 'Fusion', 'Canadian',
       'Breakfast', 'Cajun', 'New Mexican', 'Belgian', 'Cuban', 'Taco',
       'Caribbean', 'Polish', 'Deli', 'British', 'California', 'Others',
       'Eastern European', 'Creole', 'Ramen', 'Ukrainian', 'Hawaiian',
       'Patisserie', 'Yum Cha', 'Pacific Northwest', 'Tea', 'Moroccan',
       'Burmese', 'Dim Sum', 'Crepes', 'Fish and Chips', 'Russian',
       'Continental', 'South Indian', 'North Indian', 'Salad',
       'Finger Food', 'Mandi', 'Turkish', 'Kerala', 'Pakistani',
       'Biryani', 'Street Food', 'Nepalese', 'Goan', 'Iranian', 'Mughlai',
       'Rajasthani', 'Mithai', 'Maharashtrian', 'Gujarati', 'Rolls',
       'Momos', 'Parsi', 'Modern Indian', 'Andhra', 'Tibetan', 'Kebab',
       'Chettinad', 'Bengali', 'Assamese', 'Naga', 'Hyderabadi', 'Awadhi',
       'Afghan', 'Lucknowi', 'Charcoal Chicken', 'Mangalorean',
       'Egyptian', 'Malwani', 'Armenian', 'Roast Chicken', 'Indonesian',
       'Western', 'Dimsum', 'Sunda', 'Kiwi', 'Asian Fusion', 'Pan Asian',
       'Balti', 'Scottish', 'Cantonese', 'Sri Lankan', 'Khaleeji',
       'South African', 'Drinks Only', 'Durban', 'World Cuisine',
       'Izgara', 'Home-made', 'Giblets', 'Fresh Fish', 'Restaurant Cafe',
       'Kumpir', 'Döner', 'Turkish Pizza', 'Ottoman', 'Old Turkish Bars',
       'Kokoreç'], default=['Home-made', 'BBQ', 'Japanese', 'Brazilian', 'Arabian', 'American', 'Italian'])

df = df.loc[df['cuisines'].isin(cuisines_options), :]

# ==========================
# Layout no Streamlit

st.markdown('# :knife_fork_plate: Visão Tipos Culinários')

st.markdown('## Melhores Restaurantes dos Principais tipos Culinários')

with st.container():
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        
        st_metric(df, 0)
        
    with col2:
        
        st_metric(df, 1)
        
    with col3:
        
        st_metric(df, 2)
        
    with col4:
        
        st_metric(df, 3)
        
    with col5:

        st_metric(df, 4)

with st.container():
    # Top 10 dos Restaurantes
    
    st.write("## Top ", str(qtd_restaurant), 'Restaurantes')
    
    df_aux = df.loc[:, ['restaurant_id', 'restaurant_name', 'country_code', 'city', 'cuisines', 'average_cost_for_two', 'aggregate_rating', 'votes']]
    
    df_aux.rename(columns = {'country_code':'country'}, inplace = True)
    
    df_aux = df_aux.sort_values('aggregate_rating', ascending=False)
    
    df_aux = df_aux.head(qtd_restaurant)
    
    st.dataframe(df_aux)
    
with st.container():

    col1, col2 = st.columns(2)
    with col1:
        # Top 10 Melhores Tipos de Culinárias
        
        st.plotly_chart(gerar_grafico_barras(df, False, qtd_restaurant, ' Melhores Tipos de Culinárias'), use_container_width=True)
        
    with col2:
        # Top 10 Piores Tipos de Culinárias
        
        st.plotly_chart(gerar_grafico_barras(df, True, qtd_restaurant, ' Piores Tipos de Culinárias'), use_container_width=True)
        