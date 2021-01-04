import smtplib, ssl
message = ""
def TemperatureAbove(setpoint):
    global message
    message = f"This email is from your motor, the temperature reading is above your setpoint of {setpoint}"
    print("i sent temperature above email")
    sendemail()

def TemperatureBelow(setpoint):
    global message 
    message = f"This email is from your motor, the temperature reading is below your setpoint of {setpoint}"
    print("i sent temperature below email")
    sendemail()

def HumidityAbove(setpoint):
    global message 
    message = f"This email is from your motor, the humidity reading is above your setpoint of {setpoint}"
    print("i sent humidity above email")
    sendemail()

def HumidityBelow(setpoint):
    global message 
    message = f"This email is from your motor, the humidity reading is below your setpoint of {setpoint}"
    print("i sent humidity below email")
    sendemail()

def sendemail():
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "sunsendertest@gmail.com"
    receiver_email = "sunreceivertest@gmail.com"
    password = "sunsunsun"

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
