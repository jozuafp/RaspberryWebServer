from flask import Flask, render_template, url_for, redirect, request, session, make_response

import RPi.GPIO as GPIO
import random
import time
import datetime
import json

app = Flask(__name__)
app.config["SECRET KEY"]="inikunciku2021"
GPIO.setmode(GPIO.BCM)

#Set PIN GPIO
led=14
buzzer=15
GPIO_TRIGGER = 23
GPIO_ECHO = 24
motor = 25
ledSts=0
buzzerSts=0
temp=27.5
humidity=45
val_Ldr=0
stsLdr=0
distSts=0

now = datetime.datetime.now()
timeString = now.strftime("%Y-%m-%d %H:%M")
#Inisialisasi GPIO

GPIO.setup(led, GPIO.OUT)
GPIO.output(led, GPIO.LOW)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.output(buzzer, GPIO.LOW)
GPIO.setup(motor, GPIO.OUT)
GPIO.output(motor, GPIO.LOW)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def hitungTinggiAir():
# Kirim sinyal high ke trigger
	GPIO.output(GPIO_TRIGGER, True}
	time.sleep(0.00001)

#Stop trigger
	GPIO.output(GPIO_TRIGGER, False)
	timeout_counter = int(time.time())
	start = time.time()

#dapatkan waktu start
	while GPIO.input(GPIO_ECHO)==0 and (int(time.time()) - timeout_counter <3:
		start = time.time()

	timeout_counter = int(time.time())
	stop = time.time()
#dapatkan waktu stop

	while GPIO.input(GPIO_ECHO)==1 and (int(time.time()) - timeout_counter <3:
		stop = time.time()

# Hitung waktu tempuh bolak-balik
	elapsed = stop-start

# Hitung jarak, waktu tempuh dikalikan dengan kecepatan suara (dalam cm)
	jarak = elapsed * 34320

# Jarak masih dalam hitungan bolak-balik, bagi dua untuk tahu jarak ke halangan
	jarak = jarak / 2

#selesai
return jarak

@app.route("/", methods =["POST", "GET"])
def index():
	if "email" in session:
		return redirect(url_for('sukses req'))
# jika tombol button di klik
	if request.method == "POST":
		email = request.form['email']
	password = request.form[ 'password']
#jika email dan password benar
	if email == ‘admin@gmail.com' and password == ‘pass':
		session['email'] = email
		session['password'] = password
		return redirect(url_for('sukses req'))
#jika salah
	else:
		return redirect(url_for('index'))
return render_template(“index. html")

@app.route("/sukses")
def sukses_req():
status = "Anda sukses Login..."
return render_template("sukses.html", status=status)

@app.route("/monitoring")
def monitoring():
	stsLdr = random.randint(1, 10000)
	distSts = hitungTinggiAir()
#distSts = random.randInt(1, 10000)
	if "email" in session:
		if (distSts <= 26):
			GPIO.output(motor, False)
		if (distSts < 7):
			GPIO.output(motor, True)
		else:
			GPIO.output(motor, True)
		templateData = {
			'led': ledSts,
			'buzzer': buzzerSts,
			'suhu': temp,
			'humidity': humidity,
			'val_ldr': stsLdr,
			'jarak': distSts,
		}
		return render _template("monitoring.html", **templateData)
	else:
		return redirect(url_for('index'))

@app. route("/grafik")
def gratik():
	stsLdr = random.randint(1, 10000)
	distSts = hitungTinggiAir()

	if "email" in session:
		data = [
			(timeString, stsLdr),
			(timeString, distSts),
			(timeString, temp),
			("04-01-2021", stsLdr),
			("05-01-2021", 978),
			("06-01-2021", 297),]
			("07-01-2621", 159),
			("08-01-2021", 1209),
			("09-01-2021", 1797),

		labels = [row[0] for row in data]
		values = [row[1] for row in data]
		return render_template("grafik.html", labels=labels, values=values)
	else:
		return redirect(url_for('index'))

@app.route("/<deviceName>/<action>")
def action(deviceName, action):
	if deviceName == 'led':
		actuator = led
	if deviceName == 'buzzer':
		actuator = buzzer
	if action == "on":
		GPI0.output(actuator, GPIO.LOW)
# actuator = 1
	if action == “off":
		GPI0.output(actuator, GPIO.HIGH)
# actuator = 0
		templateData = {
			'led': ledSts,
			'buzzer': buzzerSts,
			'suhu': temp,
			'humidity’: humidity,
			'val_ldr': stsLdr,
			'jarak': distSts,
		}
	return render_template("monitoring.html", **templateData)

@app. route("/logout")
def Logout_akun():
	if "email" in session:
		session.pop('email')
		session.pop('password')
		return redirect(url_for(‘index'))
	else:
		return redirect(url_for('index'))

@app.route("/redirect-monitoring")
def ayo_redirect_about():
return redirect(url_for("monitoring"))

@app.route("/redirect-grafik")
def ayo_redirect_grafik():
return redirect(url_for("grafik"))

	if _name_ == "__main__":
		app.run(debug=True, host='192.168.101.8')
