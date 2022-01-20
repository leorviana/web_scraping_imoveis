import pandas as pd
import numpy as np

import requests
from bs4 import BeautifulSoup

# Importando o dataset criado com os dados coletados, vamos limpá-lo para posterior uso

df = pd.read_csv(r"C:/users/leovi/CursoDS/WebScrapping/imoveis_rj.csv")

# Removendo dados duplicados

df = df.drop_duplicates()

# Preenchendo os valores nulos de condominio por 0, provavelmente são casas por isso não pagam condominio

df.condominio = df.condominio.fillna("0")

# Trocando os valores "--" por 0

df = df.replace({"--":"0"})

# Trocando valores inválidos de preço para None

df["preco"]= df.preco.replace({"partir":None, "R$":None, "Consulta":None})

# Dropando os imoveis com valores nulos

df = df.dropna()

# Removendo pontos nos precos e condominios e removendo alguns volores de tamanho antes de transformá-los em inteiros

df.preco = [i.replace(".", "") for i in df.preco.values]
df.condominio = [i.replace(".", "") for i in df.condominio.values]

#Separando apenas os bairros dos endereco

parte2=[]
for i in df.endereco.values:
    if i.split("-")[1]:
        parte2.append(i.split("-")[1].split(",")[0].strip())
    else:
        parte2.append(None)

df["bairro"] = parte2 

df["bairro"] = df.bairro.str.lower()

# Removendo o endereço completo

df = df.drop("endereco", axis=1)

df.reset_index(inplace=True, drop=True)

# Continuação bairros

# Coletando os bairros do rio para comparação e correção

url = "https://pt.wikipedia.org/wiki/Lista_de_bairros_da_cidade_do_Rio_de_Janeiro"

requisicao = requests.get(url)

soup = BeautifulSoup(requisicao.text, "html.parser")

tabela = soup.find("table", attrs={"class":"wikitable"})

bairros_rj=[]

for i in range(2, 11):
    if i not in [5,6,8,9,10]:
        tr = tabela.find_all("tr")[i]
        td = tr.find_all("td")[2]

        for x in td.find_all("a"):
            bairros_rj.append(x.text)
    else:
        tr = tabela.find_all("tr")[i]
        td = tr.find_all("td")[1]

        for x in td.find_all("a"):
            bairros_rj.append(x.text)

bairros_rj = [i.lower() for i in bairros_rj]

# Comparando se os bairros coletados realmente existem

for i in df.bairro:
    if i not in bairros_rj:
        df["bairro"][df.bairro.values.tolist().index(i)] = None
    else:
        continue       

# Corrigindo valores inválidos

df.tamanho_m2 = [i.replace("\n", "") for i in df.tamanho_m2.values]
df.tamanho_m2 = [i.replace("\n ", "") for i in df.tamanho_m2.values]
df.quartos = [i.replace("\n", "") for i in df.quartos.values]
df.banheiros = [i.replace("\n", "") for i in df.banheiros.values]
df.vagas = [i.replace("\n", "") for i in df.vagas.values]

df.tamanho_m2 = [None if "-" in i else i for i in df.tamanho_m2.values]
df.quartos = [None if "-" in i else i for i in df.quartos.values]
df.banheiros = [None if "-" in i else i for i in df.banheiros.values]
df.vagas = [None if "-" in i else i for i in df.vagas.values]

df = df.dropna()

# Corrigindo os tipos

colunas_int = df.columns.tolist()
colunas_int.remove("bairro")

for i in colunas_int:
    df[i] = df[i].astype(int)
    

# Outras correções

df.quartos = [None if i > 5 else i for i in df.quartos.values]
df.banheiros = [None if i > 6 else i for i in df.banheiros.values]
df.vagas = [None if i > 4 else i for i in df.vagas.values]
df.tamanho_m2 = [None if i > 1000 else i for i in df.tamanho_m2.values]

df = df.dropna()
    
        
df.to_csv("C:/users/leovi/CursoDS/WebScrapping/imoveis_rj_limpo.csv", index=False)