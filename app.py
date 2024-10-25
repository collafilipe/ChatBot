import telebot
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from telebot import types
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

API_TOKEN = '7212526958:AAFQainf92M6KV_H7PFuywCOavW9T7HiVYg'  # Coloque seu token aqui
bot = telebot.TeleBot(API_TOKEN)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

service = Service('chromedriver-win64\\chromedriver.exe')

def verificar_casa_aluguel(preçoAluguel):
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://www.quintoandar.com.br/alugar/imovel/sao-jose-dos-campos-sp-brasil/casa")

        div_elements = driver.find_elements(By.CSS_SELECTOR, "div.Row_row__Sdd0v")
        preço_max = float(preçoAluguel.replace('.', '').replace(',', '.'))

        lista_casas = []
        for element in div_elements:
            texto = element.text
            
            if "R$" in texto:
                preco_total = float(texto.split("R$")[1].split()[0].replace('.', '').replace(',', '.'))
                if preco_total <= preço_max:
                    link_element = element.find_element(By.TAG_NAME, "a")  # Altere conforme necessário
                    link = link_element.get_attribute("href")
                    lista_casas.append((texto, link))

        return lista_casas
    except Exception as e:
        print(f'Erro ao achar casas com o preço: {str(e)}')
        return []
    finally:
        driver.quit()

def verificar_apartamento_aluguel(preçoAluguel):
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://www.quintoandar.com.br/alugar/imovel/sao-jose-dos-campos-sp-brasil/apartamento")

        div_elements = driver.find_elements(By.CSS_SELECTOR, "div.Row_row__Sdd0v")
        preço_max = float(preçoAluguel.replace('.', '').replace(',', '.'))

        lista_apartamentos = []
        for element in div_elements:
            texto = element.text
            
            if "R$" in texto:
                preco_total = float(texto.split("R$")[1].split()[0].replace('.', '').replace(',', '.'))
                if preco_total <= preço_max:
                    link_element = element.find_element(By.TAG_NAME, "a")  # Altere conforme necessário
                    link = link_element.get_attribute("href")
                    lista_apartamentos.append((texto, link))

        return lista_apartamentos
    except Exception as e:
        print(f'Erro ao achar apartamentos com o preço: {str(e)}')
        return []
    finally:
        driver.quit()

def verificar_casa_venda(preçoVenda):
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://www.chavesnamao.com.br/casas-a-venda/sp-sao-jose-dos-campos/")

        div_elements = driver.find_elements(By.CSS_SELECTOR, "div.imoveis__Card-obm8pe-0.tNifl.first")
        preço_max = float(preçoVenda.replace('.', '').replace(',', '.'))

        lista_casas = []
        for element in div_elements:
            texto = element.text
            
            if "R$" in texto:
                preco_total = float(texto.split("R$")[1].split()[0].replace('.', '').replace(',', '.'))
                if preco_total <= preço_max:
                    link = element.find_element(By.TAG_NAME, "a").get_attribute("href")
                    lista_casas.append((texto, link))

        return lista_casas
    except Exception as e:
        print(f'Erro ao achar casas com o preço: {str(e)}')
        return []
    finally:
        driver.quit()

def verificar_apartamento_venda(preçoVenda):
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://www.chavesnamao.com.br/apartamentos-a-venda/sp-sao-jose-dos-campos/")

        div_elements = driver.find_elements(By.CSS_SELECTOR, "div.imoveis__Card-obm8pe-0.tNifl.first")
        preço_max = float(preçoVenda.replace('.', '').replace(',', '.'))

        lista_apartamentos = []
        for element in div_elements:
            texto = element.text
            
            if "R$" in texto:
                preco_total = float(texto.split("R$")[1].split()[0].replace('.', '').replace(',', '.'))
                if preco_total <= preço_max:
                    link = element.find_element(By.TAG_NAME, "a").get_attribute("href")
                    lista_apartamentos.append((texto, link))

        return lista_apartamentos
    except Exception as e:
        print(f'Erro ao achar apartamentos com o preço: {str(e)}')
        return []
    finally:
        driver.quit()

def entender_intencao(mensagem):
    frases_intencoes = [
        "quero alugar uma casa",
        "quero alugar um apartamento",
        "quero comprar uma casa",
        "quero comprar um apartamento",
        "alugar casa",
        "alugar apartamento",
        "comprar casa",
        "comprar apartamento"
    ]

    vetorizador = TfidfVectorizer()
    vetor_frases = vetorizador.fit_transform(frases_intencoes)
    vetor_mensagem = vetorizador.transform([mensagem])

    similaridades = cosine_similarity(vetor_mensagem, vetor_frases)
    indice_maior_similaridade = similaridades.argmax()
    intencao = frases_intencoes[indice_maior_similaridade]

    return intencao

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Olá, o KassadinChatBot foi iniciado. O que você gostaria de fazer hoje? Alugar ou comprar um imóvel?')

@bot.message_handler(func=lambda message: True)
def executorComandos(message):
    intencao = entender_intencao(message.text.lower())
    chat_id = message.chat.id

    if "alugar" in intencao:
        if "casa" in intencao:
            bot.send_message(chat_id, 'Muito bem, será casa então!')
            bot.send_message(chat_id, 'Para começar, informe o preço TOTAL que gostaria de pagar pelo aluguel mensal:\n\nExemplo: 1.000, 2.000, 3.000, etc.')
            bot.register_next_step_handler(message, lambda msg: mostrar_casas_aluguel(msg, chat_id)) 
        elif "apartamento" in intencao:
            bot.send_message(chat_id, 'Muito bem, será apartamento então!')
            bot.send_message(chat_id, 'Para começar, informe o preço TOTAL que gostaria de pagar pelo aluguel mensal:\n\nExemplo: 1.000, 2.000, 3.000, etc.')
            bot.register_next_step_handler(message, lambda msg: mostrar_apartamentos_aluguel(msg, chat_id)) 

    elif "comprar" in intencao:
        if "casa" in intencao:
            bot.send_message(chat_id, 'Muito bem, será casa então!')
            bot.send_message(chat_id, 'Para começar, informe o preço TOTAL que gostaria de pagar pela casa:\n\nExemplo: 100.000, 200.000, 300.000, etc.')
            bot.register_next_step_handler(message, lambda msg: mostrar_casas_venda(msg, chat_id)) 
        elif "apartamento" in intencao:
            bot.send_message(chat_id, 'Muito bem, será apartamento então!')
            bot.send_message(chat_id, 'Para começar, informe o preço TOTAL que gostaria de pagar pelo apartamento:\n\nExemplo: 100.000, 200.000, 300.000, etc.')
            bot.register_next_step_handler(message, lambda msg: mostrar_apartamentos_venda(msg, chat_id))

def mostrar_casas_aluguel(message, chat_id):
    preçoAluguel = message.text.strip()
    bot.send_message(chat_id, f'Muito bem, irei pesquisar alugueis de casas por até {preçoAluguel}')

    lista_casas = verificar_casa_aluguel(preçoAluguel)

    if lista_casas:
        bot.send_message(chat_id, 'Encontrei as seguintes casas disponíveis para aluguel:')
        for casa_texto, link in lista_casas:
            markup = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton("CONTATAR", url=link)
            markup.add(btn)
            bot.send_message(chat_id, casa_texto, reply_markup=markup)
    else:
        bot.send_message(chat_id, 'Desculpe, não encontrei nenhuma casa disponível para esse valor.')

def mostrar_apartamentos_aluguel(message, chat_id):
    preçoAluguel = message.text.strip()
    bot.send_message(chat_id, f'Muito bem, irei pesquisar alugueis de apartamentos por até {preçoAluguel}')

    lista_apartamentos = verificar_apartamento_aluguel(preçoAluguel)

    if lista_apartamentos:
        bot.send_message(chat_id, 'Encontrei os seguintes apartamentos disponíveis para aluguel:')
        for apartamento_texto, link in lista_apartamentos:
            markup = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton("CONTATAR", url=link)
            markup.add(btn)
            bot.send_message(chat_id, apartamento_texto, reply_markup=markup)
    else:
        bot.send_message(chat_id, 'Desculpe, não encontrei nenhum apartamento disponível para esse valor.')

def mostrar_casas_venda(message, chat_id):
    preçoVenda = message.text.strip()
    bot.send_message(chat_id, f'Muito bem, irei pesquisar casas à venda por até {preçoVenda}')

    lista_casas = verificar_casa_venda(preçoVenda)

    if lista_casas:
        bot.send_message(chat_id, 'Encontrei as seguintes casas disponíveis para venda:')
        for casa_texto, link in lista_casas:
            markup = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton("CONTATAR", url=link)
            markup.add(btn)
            bot.send_message(chat_id, casa_texto, reply_markup=markup)
    else:
        bot.send_message(chat_id, 'Desculpe, não encontrei nenhuma casa disponível para esse valor.')

def mostrar_apartamentos_venda(message, chat_id):
    preçoVenda = message.text.strip()
    bot.send_message(chat_id, f'Muito bem, irei pesquisar apartamentos à venda por até {preçoVenda}')

    lista_apartamentos = verificar_apartamento_venda(preçoVenda)

    if lista_apartamentos:
        bot.send_message(chat_id, 'Encontrei os seguintes apartamentos disponíveis para venda:')
        for apartamento_texto, link in lista_apartamentos:
            markup = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton("CONTATAR", url=link)
            markup.add(btn)
            bot.send_message(chat_id, apartamento_texto, reply_markup=markup)
    else:
        bot.send_message(chat_id, 'Desculpe, não encontrei nenhum apartamento disponível para esse valor.')

bot.polling()
