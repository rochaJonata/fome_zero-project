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

st.set_page_config(page_title='Countries', page_icon=':earth_americas:', layout='wide')

# ====================
# Funções
# ====================

def gerar_grafico_barras(op, df, colunas_selecionadas, novo_nome_coluna, titulo_grafico):
    
    if op == True:
    
        df_aux = df.loc[:, colunas_selecionadas].groupby('country_code').mean().reset_index()

        df_aux.columns = ['Países', novo_nome_coluna]

        df_aux = df_aux.sort_values(novo_nome_coluna, ascending=False)

        grafico_barras = px.bar(df_aux, x='Países', y=novo_nome_coluna, text_auto=True).update_layout(title={'text':titulo_grafico, 'x':0.5, 'xanchor':'center', 'yanchor':'top'})

        return grafico_barras
    
    else:
        
        df_aux = df.loc[:, colunas_selecionadas].groupby('country_code').count().reset_index()

        df_aux.columns = ['Países', novo_nome_coluna]

        df_aux = df_aux.sort_values(novo_nome_coluna, ascending=False)

        grafico_barras = px.bar(df_aux, x='Países', y=novo_nome_coluna, text_auto=True).update_layout(title={'text':titulo_grafico,'x': 0.5, 'xanchor':'center', 'yanchor':'top'})
        
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

# ==================== Visão da empresa ====================

# ====================
# Barra Lateral

st.sidebar.markdown("## Filters")

countries_options = st.sidebar.multiselect('Choose the countries you want to view the information', ['Philippines', 'Brazil', 'Australia', 'United States of America', 'Canada', 'Singapure', 'United Arab Emirates', 'India', 'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa', 'Sri Lanka', 'Turkey'], default=['Philippines', 'Brazil', 'Australia', 'United States of America', 'Canada', 'Singapure', 'United Arab Emirates', 'India', 'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa', 'Sri Lanka', 'Turkey'])

#Filtro de paises
df = df.loc[df['country_code'].isin(countries_options), :]

# ==========================
# Layout no Streamlit

st.markdown('# :earth_americas: Visão Países')

with st.container():
    # Quantidade de Restaurantes Registrados por País
    
    st.plotly_chart(gerar_grafico_barras(False, df, ['restaurant_id', 'country_code'], 'Quantidade de Restaurantes', 'Quantidade de Restaurantes Registrados por País'), use_container_width=True)

with st.container():
    # Quantidade de Cidades Registrados por País
    
    df_aux = df.loc[:, ['restaurant_id', 'city', 'country_code']].groupby(['country_code', 'city']).count().reset_index()

    st.plotly_chart(gerar_grafico_barras(False, df_aux, ['city', 'country_code'], 'Quantidade de Cidades', 'Quantidade de Cidades Registrados por País'), use_container_width=True)

with st.container():

    col1, col2 = st.columns(2)
    with col1:
        # Média de Avaliações feitas por País
        
        st.plotly_chart(gerar_grafico_barras(True, df, ['country_code', 'aggregate_rating'], 'Média de Avaliações', 'Média de Avaliações feitas por País'), use_container_width=True)

    with col2:
        # Preço de um prato para duas pessoas por País
        
        st.plotly_chart(gerar_grafico_barras(True, df, ['country_code', 'average_cost_for_two'], 'Média de Preços', 'Média de Preço de um prato para duas pessoas por País'), use_container_width=True)