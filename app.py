from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from email.mime.text import MIMEText
import smtplib
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ----------------------- Flask-Mail Config -----------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')
mail = Mail(app)

# ----------------------- Routes -----------------------

@app.route('/', methods=['GET', 'HEAD'])
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/treatments')
def treatments():
    return render_template('treatments.html')

@app.route('/cure_case')
def cure_case():
    return render_template('cure_case.html')

@app.route('/contact')
def contact():
    return render_template(
        'contact.html',
        phone='94274 29035',
        email='dr.borisagars.sh.homeopathy@gmail.com',
        address='Shreeya Spine & Pain Management Centre, Kumarshala Main Road, Khambha-Amreli, Gujarat'
    )

@app.route('/test')
def test():
    return "Flask is working!"

@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        complain = request.form.get('complain')
        date = request.form.get('date')
        email = request.form.get('email')
        phone = request.form.get('phone')

        # Email to clinic
        clinic_body = f"""New appointment booking:

Name: {name}
Age: {age}
Complaint: {complain}
Preferred Date: {date}
Email: {email}
Phone: {phone}"""

        send_email(
            'dr.borisagars.sh.homeopathy@gmail.com',
            'New Appointment Booking',
            clinic_body
        )

        # Confirmation Email to patient
        patient_body = f"""Dear {name},

Thank you for booking your appointment with SH Homeopathy.

We will let you know your time of online visit soon.

Warm regards,
SH Homeopathy Team"""

        send_email(email, 'Appointment Confirmation', patient_body)

        return render_template('thankyou.html', name=name)

    return render_template('appointment.html')

@app.route('/treatments/<page>')
def treatment_page(page):
    try:
        return render_template(f'{page}.html')
    except:
        return render_template('404.html'), 404

# ----------------------- Order Kit -----------------------

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        kit = request.form.get('kit')
        price = request.form.get('price')
        payment_method = request.form.get('payment_method')
        transaction_id = request.form.get('transaction_id') or 'Not Provided'

        # Order text
        order_details = f"""New Order Received!
========================
Name: {name}
Email: {email}
Phone: {phone}
Address: {address}
Ordered Kit: {kit}
Total Price: ₹{price}
Payment Method: {payment_method}
Transaction ID: {transaction_id}
========================"""

        # Save locally
        with open('orders.txt', 'a', encoding='utf-8') as f:
            f.write(order_details + '\n')

        # Email to Clinic
        send_email(
            'dr.borisagars.sh.homeopathy@gmail.com',
            'New Kit Order',
            order_details
        )

        # Confirmation Email to Customer
        confirmation_msg = f"""Dear {name},

Thank you for placing your order with SH Homeopathy.

Here are your order details:
- Kit: {kit}
- Total: ₹{price}
- Payment Method: {payment_method}
- Transaction ID: {transaction_id}

We will process and dispatch your kit soon.

If you have any queries, contact us at +91-94274 29035.

Warm regards,
SH Homeopathy Team"""

        send_email(email, 'Order Confirmation - SH Homeopathy', confirmation_msg)

        return render_template('thankyou.html', name=name, kit=kit)

    return render_template('order.html')

# ----------------------- Email Function -----------------------

def send_email(recipient, subject, body):
    sender = os.environ.get('EMAIL_USER')
    password = os.environ.get('EMAIL_PASSWORD')
    msg = MIMEText(body.encode('utf-8'), _charset='utf-8')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)

# ----------------------- Run App -----------------------

if __name__ == '__main__':
    if not os.path.exists('static/uploads'):
        os.makedirs('static/uploads')
    app.run(host='0.0.0.0', port=10000)
