import telebot
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from telebot import types

API_TOKEN = '7212526958:AAFQainf92M6KV_H7PFuywCOavW9T7HiVYg'
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
            texto2 = element.text
            if "R$" in texto2:
                preço_elemento = float(texto2.split("R$")[1].split()[0].replace('.', '').replace(',', '.'))
                if preço_elemento <= preço_max:
                    lista_casas.append(texto2)

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
                preço_elemento = float(texto.split("R$")[1].split()[0].replace('.', '').replace(',', '.'))
                if preço_elemento <= preço_max:
                    lista_apartamentos.append(texto)

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
                preço_elemento = float(texto.split("R$")[1].split()[0].replace('.', '').replace(',', '.'))
                if preço_elemento <= preço_max:
                    link = element.find_element(By.TAG_NAME, "a").get_attribute("href")  # Obtém o link da casa
                    lista_casas.append((texto, link))  # Adiciona o texto e o link

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
                preço_elemento = float(texto.split("R$")[1].split()[0].replace('.', '').replace(',', '.'))
                if preço_elemento <= preço_max:
                    link = element.find_element(By.TAG_NAME, "a").get_attribute("href")  # Obtém o link do apartamento
                    lista_apartamentos.append((texto, link))  # Adiciona o texto e o link

        return lista_apartamentos
    except Exception as e:
        print(f'Erro ao achar apartamentos com o preço: {str(e)}')
        return []
    finally:
        driver.quit()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Olá, o KassadinChatBot foi iniciado. Por favor, digite os seguintes comandos abaixo para que ele possa executar as operações:')
    bot.send_message(message.chat.id, '/aluguel - Para ter assistência em achar algum disponível\n/venda - Para ter assistência em achar algum disponível')

@bot.message_handler(commands=['aluguel'])
def aluguel(message):
    bot.reply_to(message, 'Gostaria de saber sobre casas ou apartamentos?')
    estado_aluguel[message.chat.id] = True

@bot.message_handler(commands=['venda'])
def venda(message):
    bot.reply_to(message, 'Gostaria de saber sobre casas ou apartamentos?')
    estado_venda[message.chat.id] = True

@bot.message_handler(func=lambda message: True)
def executorComandos(message):
    if estado_aluguel.get(message.chat.id):
        imovel = message.text.strip().lower()

        if imovel in ['casas', 'casa']:
            bot.send_message(message.chat.id, 'Muito bem, será casa então!')
            bot.reply_to(message, 'Para começar, informe o preço TOTAL que gostaria de pagar pelo aluguel mensal:\n\nExemplo: 1.000, 2.000, 3.000, etc.')
            estado_aluguel_preço_casa[message.chat.id] = True
            estado_aluguel[message.chat.id] = False

        elif imovel in ['apartamentos', 'apartamento']:
            bot.send_message(message.chat.id, 'Muito bem, será apartamento então!')
            bot.reply_to(message, 'Para começar, informe o preço TOTAL que gostaria de pagar pelo aluguel mensal:\n\nExemplo: 1.000, 2.000, 3.000, etc.')
            estado_aluguel_preço_apartamento[message.chat.id] = True
            estado_aluguel[message.chat.id] = False

    elif estado_aluguel_preço_casa.get(message.chat.id):
        preçoAluguel = message.text.strip()
        bot.send_message(message.chat.id, f'Muito bem, irei pesquisar alugueis de casas por até {preçoAluguel}')

        lista_casas = verificar_casa_aluguel(preçoAluguel)

        if lista_casas:
            bot.send_message(message.chat.id, 'Encontrei as seguintes casas disponíveis para aluguel:')
            for casa in lista_casas:
                bot.send_message(message.chat.id, casa)

            bot.send_message(message.chat.id, 'https://www.quintoandar.com.br/alugar/imovel/sao-jose-dos-campos-sp-brasil/casa')

        else:
            bot.send_message(message.chat.id, 'Desculpe, não encontrei nenhuma casa disponível para esse valor.')
        estado_aluguel_preço_casa[message.chat.id] = False
    
    elif estado_aluguel_preço_apartamento.get(message.chat.id):
        preçoAluguel = message.text.strip()
        bot.send_message(message.chat.id, f'Muito bem, irei pesquisar alugueis de apartamentos por até {preçoAluguel}')

        lista_apartamentos = verificar_apartamento_aluguel(preçoAluguel)

        if lista_apartamentos:
            bot.send_message(message.chat.id, 'Encontrei os seguintes apartamentos disponíveis para aluguel:')
            for apartamento in lista_apartamentos:
                bot.send_message(message.chat.id, apartamento)

            bot.send_message(message.chat.id, 'https://www.quintoandar.com.br/alugar/imovel/sao-jose-dos-campos-sp-brasil/apartamento')

        else:
            bot.send_message(message.chat.id, 'Desculpe, não encontrei nenhum apartamento disponível para esse valor.')
        estado_aluguel_preço_apartamento[message.chat.id] = False

    elif estado_venda.get(message.chat.id):
        imovel = message.text.strip().lower()

        if imovel in ['casas', 'casa']:
            bot.send_message(message.chat.id, 'Muito bem, será casa então!')
            bot.reply_to(message, 'Para começar, informe o preço TOTAL que gostaria de pagar pela casa:\n\nExemplo: 100.000, 200.000, 300.000, etc.')
            estado_venda_preço_casa[message.chat.id] = True
            estado_venda[message.chat.id] = False

        elif imovel in ['apartamentos', 'apartamento']:
            bot.send_message(message.chat.id, 'Muito bem, será apartamento então!')
            bot.reply_to(message, 'Para começar, informe o preço TOTAL que gostaria de pagar pelo apartamento:\n\nExemplo: 100.000, 200.000, 300.000, etc.')
            estado_venda_preço_apartamento[message.chat.id] = True
            estado_venda[message.chat.id] = False

    elif estado_venda_preço_casa.get(message.chat.id):
        preçoVenda = message.text.strip()
        bot.send_message(message.chat.id, f'Muito bem, irei pesquisar casas à venda por até {preçoVenda}')

        lista_casas = verificar_casa_venda(preçoVenda)

        if lista_casas:
            bot.send_message(message.chat.id, 'Encontrei as seguintes casas disponíveis para venda:')
            for casa_texto, link in lista_casas:
                markup = types.InlineKeyboardMarkup()
                btn = types.InlineKeyboardButton("CONTATAR", url=link)
                markup.add(btn)
                bot.send_message(message.chat.id, casa_texto, reply_markup=markup)

        else:
            bot.send_message(message.chat.id, 'Desculpe, não encontrei nenhuma casa disponível para esse valor.')
        estado_venda_preço_casa[message.chat.id] = False

    elif estado_venda_preço_apartamento.get(message.chat.id):
        preçoVenda = message.text.strip()
        bot.send_message(message.chat.id, f'Muito bem, irei pesquisar apartamentos à venda por até {preçoVenda}')

        lista_apartamentos = verificar_apartamento_venda(preçoVenda)

        if lista_apartamentos:
            bot.send_message(message.chat.id, 'Encontrei os seguintes apartamentos disponíveis para venda:')
            for apartamento_texto, link in lista_apartamentos:
                markup = types.InlineKeyboardMarkup()
                btn = types.InlineKeyboardButton("CONTATAR", url=link)
                markup.add(btn)
                bot.send_message(message.chat.id, apartamento_texto, reply_markup=markup)

        else:
            bot.send_message(message.chat.id, 'Desculpe, não encontrei nenhum apartamento disponível para esse valor.')
        estado_venda_preço_apartamento[message.chat.id] = False

# Dicionários de estado
estado_aluguel = {}
estado_venda = {}
estado_aluguel_preço_casa = {}
estado_aluguel_preço_apartamento = {}
estado_venda_preço_casa = {}
estado_venda_preço_apartamento = {}

bot.polling()
