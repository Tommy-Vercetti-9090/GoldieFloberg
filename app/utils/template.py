from src.model.otp_model import Otp
import random
import smtplib
import os
from operator import itemgetter
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import current_app
from bson.objectid import ObjectId
import datetime
from bson.dbref import DBRef

app = current_app


def generate_and_save_otp(user_id):
    [min, max] = [1000, 9999]
    otp_key = str(random.randint(min, max))
    data = {
        "user_id": {"$ref": "User", "$id": user_id},
        "expire_at": datetime.datetime.now() + datetime.timedelta(minutes=10),
        "otp_key": otp_key,
        "createdAt": ObjectId().generation_time,
        "updatedAt": ObjectId().generation_time,
    }
    Otp(data)()
    # data["user_id"]["$id"] = ObjectId(data["user_id"]["$id"])
    app.db["Otp"].insert_one(data)
    return otp_key


def update_otp(user_id):
    app = current_app
    [min, max] = [1000, 9999]
    otp_key = str(random.randint(min, max))
    app.db["Otp"].find_one_and_update(
        {"user_id": DBRef(collection="User", id=ObjectId(user_id))},
        {
            "$set": {
                "otp_key": otp_key,
                "expire_at": datetime.datetime.now() + datetime.timedelta(minutes=10),
            }
        },
    )
    return otp_key


def send_mail_template(fullName, otpKey):
    return {
        "subject": "GOLDIEFLOBERG - Account Verification",
        "html": """
      <div
        style = "padding:20px 20px 40px 20px; position: relative; overflow: hidden; width: 100%;"
      >
        <img 
              style="
              top: 0;position: absolute;z-index: 0;width: 100%;height: 100vmax;object-fit: cover;" 
              src="cid:background" alt="background" 
        />
        <div style="z-index:1; position: relative;">
        <header style="padding-bottom: 20px">
          <div class="logo" style="text-align:center;">
        
          </div>
        </header>
        <main 
          style= "padding: 20px; background-color: #f5f5f5; border-radius: 10px; width: 80%; margin: 0 auto; margin-bottom: 20px; font-family: 'Poppins', sans-serif;"
        >
          <h1 
            style="color: #FF3333; font-size: 30px; font-weight: 700;"
          >Welcome To WEBE</h1>
          <p
            style="font-size: 24px; text-align: left; font-weight: 500; font-style: italic;"
          >Hi {},</p>
          <p 
            style="font-size: 20px; text-align: left; font-weight: 500;"
          >Thank you for registering with us. Please use the following OTP to verify your email address.</p>
          <h2
            style="font-size: 36px; font-weight: 700; padding: 10px; width:100%; text-align:center;color: #097969; text-align: center; margin-top: 20px; margin-bottom: 20px;"
          >{}</h2>
          <p style = "font-size: 16px; font-style:italic; color: #343434">If you did not request this email, kindly ignore this. If this is a frequent occurence <a
          style = "color: #097969; text-decoration: none; border-bottom: 1px solid #097969;" href = "#"
          >let us know.</a></p>
          <p style = "font-size: 20px;">Regards,</p>
          <p style = "font-size: 20px;">Dev Team</p>
        </main>
        </div>
      <div>
      """.format(
            fullName, otpKey
        ),
    }


async def send_email(recepient, subject, body):
    MAIL_HOST, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD = itemgetter(
        "MAIL_HOST", "MAIL_PORT", "MAIL_USERNAME", "MAIL_PASSWORD"
    )(app.config)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = MAIL_USERNAME
    msg["To"] = recepient

    msg.attach(MIMEText(body, "html"))

    transporter = smtplib.SMTP_SSL(MAIL_HOST, MAIL_PORT)
    transporter.login(MAIL_USERNAME, MAIL_PASSWORD)
    transporter.sendmail(MAIL_USERNAME, recepient, msg.as_string())
    transporter.quit()
