import smtplib
import email.message

server = smtplib.SMTP('smtp.gmail.com:587')

email_content = """
<html>

<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
   <title>Connecsi</title>
</head>

<body>
Connecsi User wants to connect with you...
Please login to view the full message...
<a href="#">Login</a>
</body>
</html>


"""

msg = email.message.Message()
msg['Subject'] = 'test'

msg['From'] = 'kiran.padwal@connecsi.com'
msg['To'] = 'kiran.padwal@connecsi.com'
password = "####"
msg.add_header('Content-Type', 'text/html')
msg.set_payload(email_content)

s = smtplib.SMTP('smtp.gmail.com: 587')
s.starttls()

# Login Credentials for sending the mail
s.login(msg['From'], password)

s.sendmail(msg['From'], [msg['To']], msg.as_string())
