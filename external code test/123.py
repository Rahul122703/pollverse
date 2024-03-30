import smtplib

# Set up SMTP server connection
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

# Your Gmail credentials
from_email = "xieminiproject@gmail.com"
app_pass = "omni tvxy oelb dctl"  # This should be your App Password

try:
    # Login to SMTP server
    server.login(user=from_email, password=app_pass)
    
    # Send email
    to_email = "killkamam3@gmail.com"
    subject = "Hello"
    body = "Hello there, this is Rahul Sharma"
    message = f"Subject: {subject}\n\n{body}"
    server.sendmail(from_addr=from_email, to_addrs=to_email, msg=message)
    print("Email sent successfully.")
except Exception as e:
    print("An error occurred:", e)
finally:
    # Close the connection to the SMTP server
    server.quit()
