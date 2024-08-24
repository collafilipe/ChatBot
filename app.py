import telebot
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

API_TOKEN = 'YOUR_API_TOKEN'
bot = telebot.TeleBot(API_TOKEN)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

service = Service('chromedriver')

def verificar_casa_aluguel(preçoAluguel):
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://www.quintoandar.com.br/alugar/imovel/sao-jose-dos-campos-sp-brasil/casa")

        div_elements = driver.find_elements(By.CSS_SELECTOR, "div.Row_row__Sdd0v")
        preço = f"R$ {preçoAluguel} total"

        lista_casas = []
        for element in div_elements:
            texto2 = element.text
            
            casas_separadas = texto2.split("Campos")
            for i, casa in enumerate(casas_separadas):
                casa = casa.strip()
                if i < len(casas_separadas) - 1:
                    casa += " Campos"
                if preço in casa:
                    lista_casas.append(casa)

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
        preço = f"R$ {preçoAluguel} total"

        lista_apartamentos = []
        for element in div_elements:
            texto = element.text

            apartamentos_separadas = texto.split("Campos")
            for i, apartamento in enumerate(apartamentos_separadas):
                apartamento = apartamento.strip()
                if i < len(apartamentos_separadas) - 1:
                    apartamento += " Campos"
                if preço in apartamento:
                    lista_apartamentos.append(apartamento)
        print(lista_apartamentos)
        print(apartamentos_separadas)
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

        if imovel == 'casas' or imovel == 'casa':
            bot.send_message(message.chat.id, 'Muito bem, será casa então!')
            bot.reply_to(message, 'Para começar, informe o preço TOTAL que gostaria de pagar pelo aluguel mensal:\n\nExemplo: 1.000, 2.000, 3.000, etc.')
            estado_aluguel_preço_casa[message.chat.id] = True
            estado_aluguel[message.chat.id] = False

        elif imovel == 'apartamentos' or imovel == 'apartamento':
            bot.send_message(message.chat.id, 'Muito bem, será apartamento então!')
            bot.reply_to(message, 'Para começar, informe o preço TOTAL que gostaria de pagar pelo aluguel mensal:\n\nExemplo: 1.000, 2.000, 3.000, etc.')
            estado_aluguel_preço_apartamento[message.chat.id] = True
            estado_aluguel[message.chat.id] = False

    elif estado_aluguel_preço_casa.get(message.chat.id):
        preçoAluguel = message.text.strip()
        bot.send_message(message.chat.id, f'Muito bem, irei pesquisar alugueis de casas por {preçoAluguel}')

        lista_casas = verificar_casa_aluguel(preçoAluguel)

        if lista_casas:
            bot.send_message(message.chat.id, 'Encontrei as seguintes casas disponíveis para aluguel:')

            for casa in lista_casas:
                bot.send_message(message.chat.id, f'{casa}')

            bot.send_message(message.chat.id, 'https://www.quintoandar.com.br/alugar/imovel/sao-jose-dos-campos-sp-brasil/casa')

        else:
            bot.send_message(message.chat.id, 'Desculpe, não encontrei nenhuma casa disponível para esse valor.')
            estado_aluguel_preço_casa[message.chat.id] = False
        estado_aluguel_preço_casa[message.chat.id] = False
    
    elif estado_aluguel_preço_apartamento.get(message.chat.id):
        preçoAluguel = message.text.strip()
        bot.send_message(message.chat.id, f'Muito bem, irei pesquisar alugueis de apartamentos por {preçoAluguel}')

        lista_apartamentos = verificar_apartamento_aluguel(preçoAluguel)

        if lista_apartamentos:
            bot.send_message(message.chat.id, 'Encontrei os seguintes apartamentos disponíveis para aluguel:')

            for apartamento in lista_apartamentos:
                bot.send_message(message.chat.id, f'{apartamento}')

            bot.send_message(message.chat.id, 'https://www.quintoandar.com.br/alugar/imovel/sao-jose-dos-campos-sp-brasil/apartamento')

        else:
            bot.send_message(message.chat.id, 'Desculpe, não encontrei nenhum apartamento disponível para esse valor.')
            estado_aluguel_preço_apartamento[message.chat.id] = False
        estado_aluguel_preço_apartamento[message.chat.id] = False

    else:
        bot.reply_to(message, 'Desculpe, não entendi. Tente um dos comandos:')
        bot.send_message(message.chat.id, '/aluguel - Para ter assistência em achar algum disponível\n/venda - Para ter assistência em achar algum disponível')

estado_aluguel = {}
estado_venda = {}
estado_aluguel_preço_casa = {}
estado_aluguel_preço_apartamento = {}
estado_venda_preço_casa = {}
estado_venda_preço_apartamento = {}

bot.polling()