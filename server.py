from flask import Flask, request, Response, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import os, json
from datetime import datetime
import base64
from emailer import TemperatureAbove, TemperatureBelow, HumidityAbove, HumidityBelow

# Initialize the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensor_value.db'
db = SQLAlchemy(app)

#class for face storage
class SensorValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature_value = db.Column(db.String(100)) #storing temperature reading as a string
    humidity_value = db.Column(db.String(100)) #storing humidity reading as a string
    level_value = db.Column(db.String(100)) #storing level value as a string
    def __repr__ (self):
        return '<Value %r>' % self.id

#class for setpoint storage
class setpoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tu = db.Column(db.Integer)
    tut = db.Column(db.Integer)
    tl = db.Column(db.Integer)
    tlt = db.Column(db.Integer)
    hu = db.Column(db.Integer)
    hut = db.Column(db.Integer)
    hl = db.Column(db.Integer)
    hlt = db.Column(db.Integer)

    def __repr__ (self):
        return '<Value %r>' % self.id

#for now, i will set the setpoints here
spoints = setpoint(tu=26, tut = 1, tl=23, tlt = 1, hu=80, hut = 1, hl=60, hlt = 1)
db.session.add(spoints)
db.session.commit()
#global variables for temperature and humidity alert
class flags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    TemperatureIsAbove = db.Column(db.Boolean)
    TemperatureIsBelow = db.Column(db.Boolean)
    HumidityIsAbove = db.Column(db.Boolean)
    HumidityIsBelow = db.Column(db.Boolean)

    def __repr__ (self):
        return '<Value %r>' % self.id

f = flags(TemperatureIsAbove = False, TemperatureIsBelow = False, HumidityIsAbove = False, HumidityIsBelow = False)
db.session.add(f)
db.session.commit()

# route http posts to this method
@app.route('/api/post_value', methods=['POST'])
def test():
    r = request
    data = r.json
    #print(type(data))
    sens_val = SensorValue(temperature_value=data["temp"], humidity_value=data["humid"], level_value = " ")
    if sens_val:
        print(data)
    db.session.add(sens_val)
    db.session.commit()
    check()
    return "sens_val"    

@app.route("/", methods=["POST","GET"])
def index():
    if request.method == "POST":
        data = request.form['sensor']
        sens_val = SensorValue(sensor_value=data)        
        
        try:
            db.session.add(sens_val)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue with this request"
    else:
        faces = SensorValue.query.order_by(SensorValue.id).all()
        return render_template("index.html", faces=[faces[-1]])
        #return render_template("index.html")

@app.route('/temphistory/', methods=["GET", "POST"])
def temphistory():
    faces = SensorValue.query.order_by(SensorValue.id).all()
    return render_template('temphistory.html', faces=faces)

@app.route('/humidhistory/', methods=["GET", "POST"])
def humidhistory():
    faces = SensorValue.query.order_by(SensorValue.id).all()
    return render_template('humidhistory.html', faces=faces)

@app.route('/updatetemp/', methods=["GET", "POST"])
def update():
    #values_to_update = SensorValue.query.get_or_404(id)
    global spoints
    if request.method == "POST":
        values_to_update.sensors_value = request.form['sensor_value']
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was a problem with this update request"

    else:
        s = setpoint.query.order_by(setpoint.id).all()
        return render_template('updatetemp.html', setpoints=s[0])

@app.route('/temperaturealarm/', methods=["GET", "POST"])
def temperaturealarm():
    #values_to_update = SensorValue.query.get_or_404(id)
    global spoints
    if request.method == "POST":
        values_to_update.sensors_value = request.form['sensor_value']
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was a problem with this update request"

    else:
        s = flags.query.order_by(flags.id).all()
        return render_template('temperaturealarm.html', flags=s[0])

@app.route('/tempabovereset/<int:id>', methods=["GET", "POST"])
def tempabovereset():
    global f
    if request.method == "POST":
        fla = flags.query.get_or_404(id)
        fla.TemperatureIsAbove = False
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was a problem with this update request"

@app.route('/tempbelowreset/<int:id>', methods=["GET", "POST"])
def tempbelowreset():
    global f
    if request.method == "POST":
        fla = flags.query.get_or_404(id)
        fla.TemperatureIsBelow = False
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was a problem with this update request"

@app.route('/updatetemperature/<int:id>', methods=["GET", "POST"])
def updatetemp(id):
    global spoints
    if request.method == "POST":
        s = setpoint.query.get_or_404(id)
        s.tu = request.form['tu']
        s.tut = request.form['tut']
        s.tl = request.form['tl']
        s.tlt = request.form['tlt']
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was a problem with this update request"

@app.route('/updatehumid/', methods=["GET", "POST"])
def updateh():
    #values_to_update = SensorValue.query.get_or_404(id)
    global spoints
    if request.method == "POST":
        values_to_update.sensors_value = request.form['sensor_value']
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was a problem with this update request"

    else:
        s = setpoint.query.order_by(setpoint.id).all()
        return render_template('updatehumid.html', setpoints=s[0])

@app.route('/updatehumidity/<int:id>', methods=["GET", "POST"])
def updatehumid(id):
    global spoints
    if request.method == "POST":
        s = setpoint.query.get_or_404(id)
        s.hu = request.form['hu']
        s.hut = request.form['hut']
        s.hl = request.form['hl']
        s.hlt = request.form['hlt']
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was a problem with this update request"

@app.route('/updatehumidity/<int:id>', methods=["GET", "POST"])
def updatehum(id):
    global spoints
    if request.method == "POST":
        s = setpoint.query.get_or_404(id)
        s.hu = request.form['hu']
        s.hut = request.form['hut']
        s.hl = request.form['hl']
        s.hlt = request.form['hlt']
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was a problem with this update request"

def check():
    readings = SensorValue.query.order_by(SensorValue.id).all()
    spoints = setpoint.query.order_by(setpoint.id).all()[0]
    f = flags.query.order_by(flags.id).all()[0]
    last = readings[-1]
    if (float(last.temperature_value) < spoints.tl) and (not f.TemperatureIsBelow):
        f.TemperatureIsBelow = True
        TemperatureBelow(spoints.tl)
    if (float(last.temperature_value) > spoints.tu) and (not f.TemperatureIsAbove):
        f.TemperatureIsAbove = True
        TemperatureAbove(spoints.tu)
    if ((spoints.tl < float(last.temperature_value) < spoints.tu) and (((abs(float(last.temperature_value) - spoints.tl) > spoints.tlt) or (abs(float(last.temperature_value) - spoints.tl) - spoints.tu)))):
        f.TemperatureIsBelow = False
        f.TemperatureIsAbove = False
    if (float(last.humidity_value) > spoints.hu) and (not f.HumidityIsAbove):
        f.HumidityIsAbove = True
        HumidityAbove(spoints.hu)
    if (float(last.humidity_value) < spoints.hl)  and (not f.HumidityIsBelow):
        f.HumidityIsBelow = True
        HumidityBelow(spoints.hl)
    if ((spoints.hl < float(last.humidity_value) < spoints.hu) and (((abs(float(last.humidity_value) - spoints.hl) > spoints.hlt) or (abs(float(last.humidity_value) - spoints.hu) - spoints.hut)))):
        f.HumidityIsAbove = False
        f.HumidityIsBelow = False

# start flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug= True)
