# ==========================
# Importando as bibliotecas

import pandas as pd
import streamlit as st
from PIL import Image

from streamlit_folium import folium_static

#Para desenhar um mapa
import folium as fl
from folium.plugins import MarkerCluster

from haversine import haversine

import inflection

st.set_page_config(
    page_title="Home",
    page_icon="botao-de-menu.ico",
    layout="wide"
)

# ====================
# Funções
# ====================

def mostrar_mapa(df):
    
    """ Função que retorna um folium_static
        
        Input: DataFrame
        Output: folium_static
    """
    
    fig = fl.Figure(width=1920, height=1080)

    m = fl.Map(max_bounds=True, zoom_start=100).add_to(fig)

    marker_cluster = MarkerCluster().add_to(m)
    
    for _, line in df.iterrows():
        
        fl.Marker(
            location=(line['latitude'], line['longitude']),
            icon=fl.Icon(color=line['rating_color'], icon='home'),
            popup=fl.Popup("<font size=\"3,5%\"><b>{}</b><br><br>Price: {:.2f} ({}) for two<br>Type: {}<br>Aggragate Rating: {}/5.0</font>".format(line['restaurant_name'], float(line['average_cost_for_two']), line['currency'], line['cuisines'], line['aggregate_rating']), max_width=300)

        ).add_to(marker_cluster)
    
    return folium_static(m, width=1024, height=600)

def mostrar_metrica(df, st, coluna, titulo):
    
    """ Função que retorna um streamlit.metric
        
        Input: DataFrame, Streamlit, str, str
        Output: streamlit.metric
    """
    
    result_unicos = len(df.loc[:, coluna].unique())
    
    return st.metric(label=titulo, value=result_unicos)

@st.cache_data
def convert_df(df):
    
    """ Função responsável por gravar um dataframe em um arquivo de .csv 
        
        Input: DataFrame
        Output: CSV
    """
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

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
        4. Definindo um termo padrão para palavras que pussuem o mesmo significado
        5. Remover os espaços das string
        6. Excluir as linhas vazias
        7. Excluir linha que possui 'Others' como tipo de culinaria
        8. Remove linhas duplicadas
        9. Redefinir o índice do DataFrame
        10. Conversões de dados
        
        Input: Dataframe
        Output: Dataframe
    """
    
    # 1. Depois de ter analisado os dados da coluna, definimos que a coluna era desnecessaria, portanto removemos ela. 
    df_orig = df_orig.drop('Switch to order menu', axis='columns')
    
    # 2. Renomeando as colunas do DataFrame
    df = rename_columns(df_orig)
    
    # 3. Selecionando o primeiro valor da separação de string por vírgula e atribuindo ao Dataframe
    df['cuisines'] = df.loc[:, 'cuisines'].apply(lambda x: str(x).split(",")[0])
    
    # 4. Definindo um termo padrão para palavras que pussuem o mesmo significado
    df['cuisines'] = df.loc[:, 'cuisines'].apply(lambda x: x.replace("Cafe","Coffee"))
    
    # 5. Remover os espaços das string
    colunas = ['restaurant_id', 'restaurant_name', 'country_code', 'city', 'address', 'locality', 'locality_verbose', 'longitude', 'latitude', 'cuisines', 'average_cost_for_two', 'currency', 'has_table_booking', 'has_online_delivery', 'is_delivering_now', 'price_range', 'aggregate_rating', 'rating_color', 'rating_text', 'votes']

    # for coluna in colunas:
    #     df.loc[:, coluna] = df.loc[:, coluna].str.strip(" ")

    # 6. Excluir as linhas vazias
    for colum in colunas:
        df = df.loc[(df[colum] != 'NaN') & (df[colum] != 'nan') & (df[colum] != 'NaN ') & (df[colum] != 'nan '), :]
    
    # 7. Excluir linha que possui 'Others' como tipo de culinaria 
    df = df.loc[df['cuisines'] != 'Others', :]
    
    # 8. Remove linhas duplicadas
    df = df.drop_duplicates()
    
    # 9. Redefinir o índice do DataFrame
    df = df.reset_index(drop=True)
    
    # 10. Conversões de dados
    
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

# ==================== Página Home ====================

# ====================
# Barra Lateral

with st.sidebar:
    col1, col2 = st.columns(2)
    with col1:
        image = Image.open('logo.jpg')
        st.image(image, width=120)
    with col2:
        st.markdown('# Fome Zero')

st.sidebar.markdown("""---""")

st.sidebar.markdown("## Filters")

countries_options = st.sidebar.multiselect('Choose the countries you want to view the information', ['Philippines', 'Brazil', 'Australia', 'United States of America', 'Canada', 'Singapure', 'United Arab Emirates', 'India', 'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa', 'Sri Lanka', 'Turkey'], default=['Philippines', 'Brazil', 'Australia', 'United States of America', 'Canada', 'Singapure', 'United Arab Emirates', 'India', 'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa', 'Sri Lanka', 'Turkey'])

#Filtro de paises
df = df.loc[df['country_code'].isin(countries_options), :]

st.sidebar.markdown("## Processed Data")

csv = convert_df(df)
#Botão para baixar o dataframe limpo
st.sidebar.download_button(
    label="Download",
    data=csv,
    file_name='data.csv',
    mime='text/csv',
)

# ==========================
# Layout no Streamlit

st.markdown("# Fome Zero!")

st.markdown("## O Melhor lugar para encontrar seu mais novo restaurante favorito!")

st.markdown("### Temos as seguintes marcas dentro da nossa plataforma:")

with st.container():
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        # Restaurantes Cadastrados
        mostrar_metrica(df, st, 'restaurant_id', "Restaurantes Cadastrados")
        
    with col2:
        # Países Cadastrados
        mostrar_metrica(df, st, 'country_code', "Países Cadastrados")
        
    with col3:
        # Cidades Cadastradas
        mostrar_metrica(df, st, 'city', "Cidades Cadastradas")
        
    with col4:
        # Avaliações Feitas
        total_avaliacao = df.loc[:, 'votes'].sum()
        resultado = '{0:,}'.format(total_avaliacao).replace(',','.') #Aqui coloca os pontos
        st.metric(label="Avaliações Feitas", value=resultado)
        
    with col5:
        # Tipos de Culinárias
        mostrar_metrica(df, st, 'cuisines', "Tipos de Culinárias")
        
with st.container():
    
    mostrar_mapa(df)
    