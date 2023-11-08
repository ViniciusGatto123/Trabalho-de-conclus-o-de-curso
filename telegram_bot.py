from gettext import dpgettext
import io
import requests
import json
from app import db_config
import psycopg2


class TelegramBot:
    # Token bot
    def __init__(self):
        token = "6403075811:AAGzqzSPMluNJAEYMqbOzooZz-ymgK6hfpk"
        self.url_base = f"https://api.telegram.org/bot{token}/"

    # Inicia o bot
    def start(self):
        update_id = None
        while True:
            update = self.getMessages(update_id)
            messages = update["result"]
            if messages:
                for message in messages:
                    update_id = message["update_id"]
                    chat_id = message["message"]["from"]["id"]

                    answer = self.createAnswer(message, chat_id)
                    print(f"Resposta do Bot: {answer}")
                    self.answer(answer, chat_id)

                    # Verificar se a mensagem contém o callback_data para ver registros
                    if "callback_query" in message:
                        callback_data = message["callback_query"]["data"]
                        if callback_data == "dados":
                            self.viewData(chat_id)  # Remova a linha answer_register =

    # Obtem mensagens
    def getMessages(self, update_id):
        requisition_link = f"{self.url_base}getUpdates?timeout=100"
        if update_id:
            requisition_link = f"{requisition_link}&offset={update_id+1}"
        result = requests.get(requisition_link)
        return json.loads(result.content)

    # Envia a mensagem formatada
    def viewData(self, chat_id):
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT quantity, observation, code, price, description, category, photo FROM data"
        )
        data = cursor.fetchall()

        conn.close()

        if data:
            for datas in data:
                (
                    quantity,
                    observation,
                    code,
                    price,
                    description,
                    category,
                    photo,
                ) = datas

                response = f"Descrição: {description}\nPreço: {price}\nQuantidade: {quantity}\nCódigo: {code}\nCategoria: {category}\nObservação: {observation}\n"

                self.answer(response, chat_id)
                # Verificar se há uma imagem associada ao registro
                if photo:
                    # Enviar a imagem como arquivo anexo
                    image_buffer = io.BytesIO(photo)
                    image_buffer.seek(0)
                    sendLink = f"{self.url_base}sendPhoto?chat_id={chat_id}"
                    files = {"photo": ("image.png", image_buffer, "image/png")}
                    requests.post(sendLink, files=files)

                else:
                    # Caso não haja dados no banco
                    self.answer("Nenhuma foto cadastrada.", chat_id)

    def send_image(self, chat_id, file_id):
        sendLink = f"{self.url_base}sendPhoto?chat_id={chat_id}&photo={file_id}"
        requests.get(sendLink)

    # Cria resposta
    def createAnswer(self, message, chat_id):
        message = str(message["message"]["text"])

        if message.startswith("/dados"):  # Lidar com o comando /dados
            return self.viewData(chat_id)

        return "Para verificar os produtos cadastrados, digite /dados"

    # Envia a resposta
    def answer(self, resposta, chat_id):
        sendLink = f"{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}"
        requests.get(sendLink)


bot = TelegramBot()
bot.start()
