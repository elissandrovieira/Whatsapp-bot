from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/chatbot/webhook/', methods=['POST'])
def webhook():
	data = request.json
chat_id = data['payload']['from']
    is_contact = '5521983401163@c.us' in chat_id

    if is_contact:
	    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)

##5521983401163@c.us
