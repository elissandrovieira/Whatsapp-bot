import time
import random

from flask import Flask, request, jsonify

from bot.ai_bot import AIBot
from services.wpp import Wpp

app = Flask(__name__)

@app.route('/chatbot/webhook/', methods=['POST'])
def webhook():
    data = request.json

    if not data or 'payload' not in data or 'from' not in data['payload']:
        return jsonify({'error': 'Invalid payload'}), 400

    chat_id = data['payload']['from']
    received_message = data['payload']['body']
    is_contact = '5521983401163@c.us' in chat_id
    is_group = '@g.us' in chat_id

    if is_group:
        return jsonify({'status': 'success', 'message': 'Mensagem de grupo ignorada.'}), 200

    bot = AIBot()
    wpp = Wpp()

    if is_contact:
        wpp.start_typing(chat_id=chat_id)
        time.sleep(random.randint(3, 10))

        history_messages = wpp.get_history_messages(
            chat_id=chat_id,
            limit=10,
        )

        response = bot.invoke(
            history_messages=history_messages,
            message=received_message,
        )
        wpp.send_message(
            chat_id=chat_id,
            message=response,
        )

        wpp.stop_typing(chat_id=chat_id)

    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
