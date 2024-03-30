import smtplib
server = smtplib.SMTP("smtp.gmail.com")
server.starttls()
from_email = "xieminproject@gmail.com"
app_pass = "omni tvxy oelb dctl"
server.login(user = from_email,password=app_pass)
server.sendmail(from_addr = from_email, to_addrs="killbusysness@gmail.com",msg="hello there this is rahul sharma")
server.close()