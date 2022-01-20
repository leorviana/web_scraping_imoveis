from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--headless") 

url="https://www.vivareal.com.br/venda/rj/rio-de-janeiro/"


navegador = webdriver.Chrome("C:/users/leovi/CursoDS/WebScrapping/codigos/chromedriver.exe", options=options)
navegador.get(url)

sleep(1)

try:
    notificacao = navegador.find_element_by_id("cookie-notifier-cta")
    notificacao.click()
except:
    print("Notificação indisponível, continuando scraping...")

df_raw = pd.DataFrame(columns=["endereco", "preco", "condominio", "tamanho_m2", "quartos", "banheiros", "vagas"])

for i in range(1, 1000):

    soup = BeautifulSoup(navegador.page_source, "html.parser")
    
    contents = soup.find_all("div", attrs={"class":"property-card__content"})
    
    
    enderecos=[]
    precos=[]
    condos=[]
    m2=[]
    quartos=[]
    banheiros=[]
    vagas=[]
    
    for content in contents:
    
        # Bairro
        endereco = content.find("span", attrs={"class":"property-card__address"})
        if endereco:
            endereco = endereco.text
            enderecos.append(endereco)
        else:
            endereco.append(None)
            
        
        # Valor
        preco = content.find("div", attrs={"class":"property-card__price"})
        if preco:
            preco = preco.text
            preco = preco.strip().split(" ")[1]
            precos.append(preco)
        else:
            precos.append(None)
            
          
        # Valor condominio
        condominio = content.find("strong", attrs={"class":"js-condo-price"})
        if condominio:
            condominio = condominio.text
            condominio = condominio.strip().split(" ")[1]
            condos.append(condominio)
        else:
            condos.append(None)
            
        
        # Tamanho em M2
        tamanho_m2 = content.find("span", attrs={"class":"property-card__detail-value js-property-card-value property-card__detail-area js-property-card-detail-area"})
        if tamanho_m2:
            tamanho_m2 = tamanho_m2.text
            m2.append(tamanho_m2)
        else:
            m2.append(None)
            
        
        # Número de quartos
        quarto = content.find("li", attrs={"class":"property-card__detail-item property-card__detail-room js-property-detail-rooms"})
        if quarto:
            quarto = quarto.text
            quarto = quarto.strip().split("  ")[0]
            quartos.append(quarto)
        else:
            quartos.append(None)
            
        
        # Número de banheiros
        banheiro = content.find("li", attrs={"class":"property-card__detail-item property-card__detail-bathroom js-property-detail-bathroom"})
        if banheiro:
            banheiro = banheiro.text
            banheiro = banheiro.strip().split("  ")[0]
            banheiros.append(banheiro)
        else:
            banheiros.append(None)
        
        
        # Número de vagas
        vaga = content.find("li", attrs={"class":"property-card__detail-item property-card__detail-garage js-property-detail-garages"})
        if vaga:
            vaga = vaga.text
            vaga = vaga.strip().split("  ")[0]
            vagas.append(vaga)
        else:
            vagas.append(None)
    
    
    df_temp = pd.DataFrame({"endereco": enderecos, "preco": precos, "condominio": condos, "tamanho_m2": m2, "quartos": quartos, "banheiros": banheiros, "vagas": vagas})

    df_raw = pd.concat([df_raw, df_temp])

    prox_pag = navegador.find_element_by_xpath("//a[@title='Próxima página']")
    
    if prox_pag:
        try:
            prox_pag.click()
        except:
            print("Limite de páginas excedido!")
            
            break
    
    sleep(2)
    
df_raw.to_csv("C:/users/leovi/CursoDS/WebScrapping/imoveis_rj.csv", index=False)