import boto3
import csv
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

s3 = boto3.client('s3')
ses = boto3.client('ses', region_name='us-east-1')  # <-- your SES region

SENDER_EMAIL = "companyserviceshr@gmail.com"

def lambda_handler(event, context):
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        print(f"Triggered by file: s3://{bucket}/{key}")

        local_csv = '/tmp/recipients.csv'
        s3.download_file(bucket, key, local_csv)

        with open(local_csv, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    email = row['Email'].strip()
                    name = row['Name'].strip()
                    status = row['Status'].strip().lower()
                    company = row['Company'].strip() if 'Company' in row else "Our Company"
                    file_key = row['Attachment_File'].strip() if 'Attachment_File' in row and row['Attachment_File'] else ""


                    if status == 'selected' and file_key:
                        send_email_with_attachment(bucket, email, name, file_key, company)
                    elif status == 'rejected':
                        send_plain_email(email, name, company)
                    else:
                        print(f"[SKIP] {email} - invalid status or missing file")

                except Exception as ex:
                    print(f"[ERROR] Row processing failed: {str(ex)}")

        return {"statusCode": 200, "body": "Emails processed."}

    except Exception as e:
        print(f"[FATAL ERROR] {str(e)}")
        return {"statusCode": 500, "body": str(e)}


def send_plain_email(email, name, company):
    subject = f"{company} - Application Update"
    body = f"Hi {name},\n\nThank you for your interest, time and effort in exploring growth opportunities at {company}.\n\nWe care about your experience, and we aim to provide an open, fair, and inclusive hiring process with a personal touch.\nOur team carefully review each application, and unfortunately on this occasion, we will not be progressing you to the next stage of the hiring process at {company}.We appreciate the time taken to submit your application.\nWe encourage you to keep in touch to receive our latest updates and jobs.\n\nWe wish you the best in your job search.\n\nBest,\n{company} Team"

    ses.send_email(
        Source=SENDER_EMAIL,
        Destination={'ToAddresses': [email]},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': body}}
        }
    )
    print(f"[✅] Rejection email sent to {email}")

def send_email_with_attachment(bucket, email, name, file_key, company):
    local_file = '/tmp/offer.pdf'
    s3.download_file(bucket, file_key, local_file)

    with open(local_file, 'rb') as f:
        attachment = f.read()

    subject = f"🎉 Congratulations, You're Selected by {company}!"
    body = f"Hi {name},\n\nWarm greetings from {company}!\n\nCongratulations and welcome to the {company} family. We are delighted to offer you a role with {company} (details in the attached offer letter) and the offered role is the foundation for a rewarding career with {company}. Our holistic Learning and Development programs will groom you further for an enriching and exciting career with us.\n\nAttached offer letter includes important details about your compensation, benefits, and terms and conditions of your employment.\n\nWe are excited and looking forward to having you on-board, and we believe that you will make a successful career for yourself at {company}.\n\nWe wish you all the best for your future endeavors.\n\nBest regards,\n{company} Team"

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = email

    msg.attach(MIMEText(body, 'plain'))

    part = MIMEApplication(attachment)
    part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_key))
    msg.attach(part)

    ses.send_raw_email(RawMessage={'Data': msg.as_string()})
    print(f"[✅] Offer letter sent to {email} from {company}")
