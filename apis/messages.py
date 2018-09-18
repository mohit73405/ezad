from flask import Flask, request, session
from flask_restplus import Resource, Api, fields, Namespace
from model.ConnecsiModel import ConnecsiModel
from passlib.hash import sha256_crypt
import datetime
import smtplib
import email.message


ns_messages = Namespace('Messages', description='Messages Operations')

message_form = ns_messages.model('Message Details', {
    'from_email_id' : fields.String(required=True, description='From Email Id'),
    'to_email_id' : fields.String(required=True, description='To Email Id'),
    'date' : fields.String(required=True, description='Date'),
    'subject' : fields.String(required=True, description='Subject'),
    'message' : fields.String(required=True, description='Message')
})



@ns_messages.route('/<string:user_id>/<string:user_type>')
class MailBox(Resource):
    @ns_messages.expect(message_form)
    def post(self,user_id,user_type):
        '''Send message'''
        form_data = request.get_json()
        from_email_id = form_data.get('from_email_id')
        to_email_id = form_data.get('to_email_id')
        date = form_data.get('date')
        subject = form_data.get('subject')
        message = form_data.get('message')

        columns = ['from_email_id', 'to_email_id', 'date', 'subject', 'message','user_id','user_type']
        data = [from_email_id, to_email_id, date, subject, message,user_id,user_type]
        result=0
        try:
            self.send_mail(subject=subject,to_email_id=to_email_id)
            connecsiObj = ConnecsiModel()
            result = connecsiObj.insert__(table_name='messages',columns=columns,data=data,IGNORE='IGNORE')
            return {'response': result},200
        except: return {'response': result},500

    def get(self,user_id,user_type):
        ''' get messages by user id and user type'''
        try:
            connecsiObj = ConnecsiModel()
            data = connecsiObj.get_messages_by_user_id_and_user_type(user_id=user_id,user_type=user_type)
            print(data)
            columns = ['message_id','from_email_id', 'to_email_id', 'date', 'subject', 'message', 'user_id', 'user_type']
            response_list = []
            for item in data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}
        except Exception as e:
            return {"response": e},500

    def send_mail(self,subject,to_email_id):
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
        msg['Subject'] = subject
        msg['From'] = 'business@connecsi.com'
        msg['To'] = to_email_id
        password = "Ezadteam"
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(email_content)

        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        # Login Credentials for sending the mail
        server.login(msg['From'], password)
        server.sendmail(msg['From'], [msg['To']], msg.as_string())
