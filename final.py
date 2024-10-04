from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import random
import requests
import math
from twilio.rest import Client

app = Flask(__name__)
app.secret_key = '311f671a9ec498740d7d27fd3b361ad3b4bd6705bb8cc705'

# Twilio credentials
TWILIO_ACCOUNT_SID = 'AC8d7a2298d14a128943955c7cd600d8e2'
TWILIO_AUTH_TOKEN = 'e2c2c04f60a15a613f0967dfe7ad0352'
TWILIO_PHONE_NUMBER = '+14694164254'

# Function to generate a 6-digit OTP
def generate_otp():
    return random.randint(100000, 999999)

def send_otp_via_sms(phone_number, otp):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f'Your OTP is {otp}',
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return message.sid

@app.route('/')
def index():
    return render_template('index3.html')

@app.route('/send_otp', methods=['POST'])
def send_otp():
    phone_number = request.form['phone_number']
    otp = generate_otp()
    
    session['otp'] = otp
    session['phone_number'] = phone_number
    
    try:
        message_sid = send_otp_via_sms(phone_number, otp)
        print(f"Sent OTP {otp} to phone number {phone_number} (Message SID: {message_sid})")
    except Exception as e:
        return f"Failed to send OTP: {str(e)}"
    
    return redirect(url_for('verify_otp'))

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        entered_otp = request.form['otp']
        if 'otp' in session and str(session['otp']) == entered_otp:
            return "OTP verified. Please wait..."
        else:
            return "Invalid OTP, try again."
    return render_template('verify_otp.html')

@app.route('/set_private_ip', methods=['POST'])
def set_private_ip():
    data = request.get_json()
    private_ip = data.get('ip')
    print(private_ip)
    
    if private_ip and private_ip.strip():  # Ensure IP address is neither None nor blank
        session['user_private_ip'] = private_ip
        return jsonify({'status': 'success', 'ip': private_ip})
    return jsonify({'status': 'error', 'message': 'Private IP address is invalid or not provided'}), 400

@app.route('/geofence_check')
def geofence_check():
    user_ip = session.get('user_private_ip')
    
    if user_ip:
        # Here, use the private IP as needed
        return f"The private IP address of the device is {user_ip}."
    else:
        return "User private IP address not found."

if __name__ == '__main__':
    app.run(debug=True)
