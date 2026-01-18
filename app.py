import os
import pandas as pd
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from flask import Flask, request, render_template, send_file

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

SENDER_EMAIL = "kahlonnoor0022@gmail.com"
SENDER_PASSWORD = "akmkwarnweputrqz"

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def calculate_topsis(input_file, weights, impacts, output_file):
    try:
        if input_file.endswith('.csv'):
            df = pd.read_csv(input_file)
        else:
            df = pd.read_excel(input_file)

        df_numeric = df.select_dtypes(include=[np.number])
        original_df = df.copy()

        weights = [float(w) for w in weights.split(',')]
        impacts = impacts.split(',')

        if len(weights) != len(df_numeric.columns):
            return None, "Error: Number of weights must match numeric columns."
        if len(impacts) != len(df_numeric.columns):
            return None, "Error: Number of impacts must match numeric columns."

        rss = np.sqrt((df_numeric**2).sum())
        normalized_df = df_numeric.div(rss)
        weighted_df = normalized_df.mul(weights)

        ideal_best = []
        ideal_worst = []

        for i, col in enumerate(weighted_df.columns):
            if impacts[i] == '+':
                ideal_best.append(weighted_df[col].max())
                ideal_worst.append(weighted_df[col].min())
            else:
                ideal_best.append(weighted_df[col].min())
                ideal_worst.append(weighted_df[col].max())

        s_best = np.sqrt(((weighted_df - ideal_best)**2).sum(axis=1))
        s_worst = np.sqrt(((weighted_df - ideal_worst)**2).sum(axis=1))

        performance_score = s_worst / (s_best + s_worst)
        original_df['Topsis Score'] = performance_score
        original_df['Rank'] = performance_score.rank(ascending=False)

        original_df.to_csv(output_file, index=False)
        return original_df, "Success"

    except Exception as e:
        return None, str(e)

def send_email(receiver_email, attachment_path):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email
    msg['Subject'] = "Your TOPSIS Result"

    body = "Hello,\n\nPlease find the attached TOPSIS result file.\n\nBest regards,\nWeb Service"
    msg.attach(MIMEText(body, 'plain'))

    filename = os.path.basename(attachment_path)
    attachment = open(attachment_path, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename= {filename}")
    msg.attach(part)
    attachment.close()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
    server.quit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download_sample')
def download_sample():
    return send_file('sample.csv', as_attachment=True)

@app.route('/process', methods=['POST'])
def process():
    if 'data_file' not in request.files:
        return "No file uploaded"
    
    file = request.files['data_file']
    weights = request.form['weights']
    impacts = request.form['impacts']
    email = request.form['email']

    if file.filename == '':
        return "No file selected"

    input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(input_path)
    output_filename = f"result_{file.filename.split('.')[0]}.csv"
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

    # Calculate
    result_df, status = calculate_topsis(input_path, weights, impacts, output_path)
    
    if status != "Success":
        return f"Error: {status}"

    # Email
    try:
        send_email(email, output_path)
        email_status = f"Result sent to {email}"
    except Exception as e:
        email_status = f"Error sending email: {str(e)}"

    # Show Result on Page
    return render_template('index.html', 
                           tables=[result_df.to_html(classes='data', header="true", index=False)], 
                           message=email_status)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
