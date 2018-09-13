from flask import Flask, request, session
from flask_restplus import Resource, Api, fields, Namespace
from model.ConnecsiModel import ConnecsiModel
from passlib.hash import sha256_crypt
import datetime
from flask_mail import Mail,Message
# import app
from apis.flaskMail import mail_app


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
            # mail = Mail(app)
            # msg = Message("Hello",
            #               sender=from_email_id,
            #               recipients=[to_email_id])
            # msg.html = "<b>testing</b>"
            # mail.send(msg)
            try:
                # mail_app.send_email(from_email=from_email_id,to_email=to_email_id,subject=subject)

                mail_app.config.update(dict(
                    MAIL_SERVER='smtp.gmail.com',
                    MAIL_PORT=587,
                    MAIL_USE_TLS=True,
                    MAIL_USE_SSL=False,
                    MAIL_USERNAME='padwalkiran1985@gmail.com',
                    MAIL_PASSWORD='ironman6@123786',
                ))
                print(mail_app.config)
                mail = Mail(mail_app)
                msg = Message("Hello",
                              recipients=[to_email_id])
                msg.html = "<b>testing</b>"
                print(msg)
                mail.send(msg)
            except Exception as e:
                print(e)
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
            columns = ['from_email_id', 'to_email_id', 'date', 'subject', 'message', 'user_id', 'user_type']
            response_list = []
            for item in data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}
        except Exception as e:
            return {"response": e},500

