from flask import Flask, render_template, jsonify, Request
from flask_mysqldb import MySQL
import paho.mqtt.client as mqtt
from datetime import datetime
import json

# Config
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'projek1'
mysql = MySQL(app)

@app.route('/', methods=['GET'])
def index():
    temperature = 12
    humimidty = 88
    return render_template('about.html', temp=temperature, hum=humimidty)

@app.route('/dash', methods=['GET'])
def dashboard(): 
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM suhu')
    data = cur.fetchall()
    cur2 = mysql.connection.cursor()
    cur2.execute('SELECT * FROM suhu ORDER BY id DESC LIMIT 1')
    temp = cur2.fetchone()
    return render_template('dashboard.html',data=data,temp=temp)

@app.route('/json-chart', methods=['GET'])
def x_chart():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM suhujam")
    r = [dict((cur.description[i][0], value)
                for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'data' : r})
    # chart_data = jsonify({'myCollection' : r})
    # return render_template('xchart.html'),jsonify({'myCollection' : r})

@app.route('/example', methods=['GET']) 
def example():
    return render_template('example.html')

@app.route('/dashgenset', methods=['GET'])
def dashboardgenset(): 
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM voltage')
    gen = cur.fetchall()
    cur2 = mysql.connection.cursor()
    cur2.execute('SELECT * FROM voltage ORDER BY idvolt DESC LIMIT 1')
    volt = cur2.fetchone()    
    return render_template('dashboardgenset.html', gen=gen,volt=volt)


@app.route('/insert/<temp>/<hum>/<getstatus>', methods=['GET'])
def insert(temp,hum,getstatus):
    temp = float(temp)
    hum = float(hum)
    getstatus = int(getstatus)
    cur = mysql.connection.cursor()
    cur.execute(f"INSERT INTO suhu (tanggal,temp, hum, status) VALUES (UTC_TIMESTAMP(),{temp}, {hum}, '{getstatus}')")
    mysql.connection.commit()
    cur.close()
    return 'Data berhasil ditambahkan'


@app.route('/genset/kamera', methods=['POST'])
def genset():
    data = request.form['img']
    cur = mysql.connection.cursor()
    cur.execute(f"INSERT INTO `genset` (`id_data`, `gambar`) VALUES (NULL, '{data}')")
    mysql.connection.commit()
    cur.close()
    return 'Data Berhasil Ditambahkan'

@app.route('/genset/volt', methods=['POST'])
def gensetV():
    data = request.form['volt']
    bv,sv,lv,c,p = data.split(',')
    cur = mysql.connection.cursor()
    cur.execute(f"INSERT INTO `voltage` (`idvolt`,`bv`, `sv`, `lv`, `c`, `p`) VALUES (NULL, '{bv}', '{sv}', '{lv}', '{c}', '{p}')")
    mysql.connection.commit()
    cur.close()
    return 'Data Berhasil Ditambahkan'


if __name__ == '__main__':
    app.run(debug=True,)
