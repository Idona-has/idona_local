from channels import Group

def ws_connect(message):
    Group('users').add(message.reply_channel)

def ws_disconnect(message):
    Group('users').discard(message.reply_channel)

def mqtt_message(message):
	print("MQTT Message:", message)