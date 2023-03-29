from classes import ISS, Sun
import smtplib
import time

MY_LAT = 33.454620
MY_LNG = -117.656490
MY_EMAIL = 'hct9zqyg@gmail.com'
MY_PASSWORD = 'xcvyrlkziutehnin'

# Declare class objects
sun = Sun(MY_LAT, MY_LNG)
iss = ISS()

# Check if the ISS is overhead and if it is nighttime, and if so, send email
while True:
    time.sleep(60)
    if iss.overhead(MY_LAT, MY_LNG) and sun.nighttime():
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg=f'Subject: ISS Notification\n\nISS overhead! at a bearing of {iss.bearing(MY_LAT, MY_LNG)} degrees'
            )
