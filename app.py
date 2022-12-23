from flask import Flask, render_template, flash
import paho.mqtt.client as mqtt
import time

#pip list --format=freeze > requirements.txt
#set FLASK_APP=app.py
#set FLASK_ENV=developmen


app = Flask(__name__)
app.secret_key = "manbearpig_MUDMAN888"


best_time = 0
energy_saving = 0

###############################################################################
#MQTT protocol for connecting to the washing machine
broker = 'broker.mqttdashboard.com'
port = 1883
topic1 = 'DY/best_time'
topic2 = 'DY/energy_saving'
topic3 = 'DY/end_flag'
client_id1 = 'myClient'
client_id2 = 'myClient'
username = 'mrezamazidi'
password = 'hsbtest1366'

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

def on_message(client, userdata, message):
    global best_time, energy_saving, end_flag
    if message.topic == topic1:
        best_time = message.payload.decode("utf-8")
    elif message.topic == topic2:
        energy_saving = message.payload.decode("utf-8")
    elif message.topic == topic3:
        end_flag = message.payload.decode("utf-8")
  


@app.route("/")
def index():
    client = mqtt.Client(client_id1)
    client.username_pw_set(username, password)
    client.connect(broker, port)
    client.on_connect = on_connect
    client.loop_start()
    client.subscribe(topic1, 1)
    client.subscribe(topic2, 1)
    client.subscribe(topic3, 1)
    client.on_message = on_message 
    time.sleep(5)
    client.loop_stop()

    flash(f'{best_time}', category = 'category1')
    flash(f'{energy_saving}', category = 'category2')
    flash(f'{end_flag}', category = 'category3')
    return render_template("index.html")


# @app.route("/redirected")
# def redirected():
# 	return render_template("index.html")



# @app.route("/greet", methods=['POST', 'GET'])
# def greeter():
# 	flash("Hi " + str(request.form['name_input']) + ", great to see you!")
# 	return render_template("index.html")
