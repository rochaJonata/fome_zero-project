<div align="center">
  
![](logo.jpg)
</div>

# Problema de Negócio

A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu core business é facilitar o encontro e negociações de clientes e restaurantes. Os restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas e também uma nota de avaliação dos serviços e produtos do restaurante, dentre outras informações.

O CEO Guerra também foi recém contratado e precisa entender melhor o negócio para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a Fome Zero, e para isso, ele precisa que seja feita uma análise nos dados da empresa e que sejam gerados dashboards, a partir dessas análises, para responder
às seguintes perguntas:

## 📋 Visão Geral

1. Quantos restaurantes únicos estão registrados?
2. Quantos países únicos estão registrados?
3. Quantas cidades únicas estão registradas?
4. Qual o total de avaliações feitas?
5. Qual o total de tipos de culinária registrados?

## 🌍 Visão Países

1.	Qual a quantidade de restaurantes registrados por país?
2.	Qual a quantidade de cidades registrados por país?
3.	Qual a média de avaliações feitas por país?
4.	Qual a média de preço de um prato para duas pessoas por país?

## 🏨 Visão Cidades

1.	Quais são as cidades com mais restaurantes na base de dados?
2.	Quais são as cidades com restaurantes com média de avaliação acima de 4?
3.	Quais são as cidades com restaurantes com média de avaliação abaixo de 2.5?
4.	Quais são as cidades com mais restaurantes com tipos culinários distintos?

## 🍽️ Visão Tipos Culinários

1.	Quais são os melhores restaurantes dos principais tipos culinários?
2.	Quais são os restaurantes com maiores avaliações? 
3.	Quais são os melhores tipos de culinárias?
4.	Quais são os piores tipos de culinárias?


O objetivo desse projeto é responder a essas questões e transformar seus resultados em dashboards que permitam o rápido entendimento do andamento do negócio.

# Premissas assumidas para análise

1.	A análise foi realizada com dados entre 17/04/2023 a 10/05/2023.
2.	O modelo de negócio assumido é um Marketplace.
3.	As 3 principais visões do negócio foram: Visão Países, Visão Cidades e Visão Tipos Culinários.
4.	Os preços de um prato para duas pessoas estão nas suas respectivas moedas de cada país.

# Estratégia da solução

O painel estratégico foi desenvolvido utilizando as métricas que refletem as 3 principais visões do modelo de negócio da empresa:

1.	**🌍 Visão Países**
2.	**🏨 Visão Cidades**
3.	**🍽️ Visão Tipos Culinários**


Cada visão é representada pelo seguinte conjunto de métricas.

### 1.	🌍 Visão Países

* Quantidade de Restaurantes Registrados por País
* Quantidade de Cidades Registrados por País
* Média de Avaliações feitas por País
* Preço de um prato para duas pessoas

### 2.	🏨 Visão Cidades

*	Top 10 Cidades com mais Restaurantes na Base de Dados
*	Top 7 Cidades com Restaurantes com média de avaliação acima de 4
*	Top 7 Cidades com Restaurantes com média de avaliação abaixo de 2.5
*	Top 10 Cidades mais restaurantes com tipos culinários distintos

### 3.	🍽️ Visão Tipos Culinários

*	Melhores Restaurantes dos Principais tipos Culinários
*	Top 10 Restaurantes
*	Top 10 Melhores Tipos de Culinárias
*	Top 10 Piores Tipos de Culinárias

# Top 3 Insights de dados

1.	A Indonésia e Australia possuem maiores média de preços de um prato para duas pessoas em relação aos outros países, porém isso não significa que são os pratos mais caros pois estão moedas diferentes.
2.	O país que possui a maior quantidade de restaurante, é também o país que possui restaurantes que estão entre o top 10 restaurantes. 
3.	Os melhores restaurantes dos principais tipos culinários não estão entre o top 10 dos restaurantes

# O produto final do projeto

Dashboards online, hospedado em uma Cloud e disponível para acesso em qualquer dispositivo conectado à internet.

O painel pode ser acessado através desse link: https://rochajonata-fome-zero.streamlit.app/

# Conclusão

O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam essas métricas da melhor forma possível para o CEO.

Portanto, a empresa Fome Zero tem atuação global com forte presença na Índia e nos Estados Unidos apresentando grande diversidade culinária.

# Próximo passos

* Aumentar o número de métricas
* Criar novos filtros.
* Adicionar novas visões de negócio.
* Padronizar os dados financeiros e de avaliação com o objetivo de tornar a comparação entre restaurantes e países mais justas/precisas na análise.
