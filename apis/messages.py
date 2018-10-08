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

conversation_form = ns_messages.model('Conversation Details', {
    # 'message_id' : fields.Integer(required=True, description='Message ID'),
    'conv_from_email_id' : fields.String(required=True, description='From Email Id'),
    'conv_to_email_id' : fields.String(required=True, description='To Email Id'),
    'conv_date' : fields.String(required=True, description='Date'),
    'conv_subject' : fields.String(required=True, description='Subject'),
    'conv_message' : fields.String(required=True, description='Message')
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
        print(data)
        result=0
        try:
            self.send_mail(subject=subject,to_email_id=to_email_id)
            connecsiObj = ConnecsiModel()
            result = connecsiObj.insert__(table_name='messages',columns=columns,data=data,IGNORE='IGNORE')
            return {'response': result},200
        except Exception as e:
            print(e)
            return {'response': result},500

    def get(self,user_id,user_type):
        ''' get messages by user id and user type'''
        try:
            connecsiObj = ConnecsiModel()
            user = connecsiObj.get__(table_name='users_brands',STAR='*',WHERE='WHERE',compare_column='user_id',compare_value=str(user_id))
            print(user)
            print(user[0][3])
            email_id = user[0][3]
            data = connecsiObj.get_messages_by_email_id_and_user_type(email_id=str(email_id),user_type=user_type)
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
        password = "ezadteam123"
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(email_content)

        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        # Login Credentials for sending the mail
        server.login(msg['From'], password)
        server.sendmail(msg['From'], [msg['To']], msg.as_string())


@ns_messages.route('/conversations/<string:message_id>/<string:user_id>/<string:user_type>')
class MailBox(Resource):
    @ns_messages.expect(conversation_form)
    def post(self, message_id,user_id, user_type):
        '''Reply to message'''
        form_data = request.get_json()
        from_email_id = form_data.get('conv_from_email_id')
        to_email_id = form_data.get('conv_to_email_id')
        date = form_data.get('conv_date')
        subject = form_data.get('conv_subject')
        message = form_data.get('conv_message')

        columns = ['message_id','conv_from_email_id', 'conv_to_email_id', 'conv_date', 'conv_subject', 'conv_message', 'user_id', 'user_type']
        data = [message_id,from_email_id, to_email_id, date, subject, message, user_id, user_type]
        result = 0
        try:
            self.send_mail(subject=subject, to_email_id=to_email_id)
            connecsiObj = ConnecsiModel()
            result = connecsiObj.insert__(table_name='conversations', columns=columns, data=data, IGNORE='IGNORE')
            return {'response': result}, 200
        except:
            return {'response': result}, 500

    def get(self,message_id,user_id,user_type):
        ''' Get Conversations by message id'''
        try:
            connecsiObj = ConnecsiModel()
            # user = connecsiObj.get__(table_name='users_brands', STAR='*', WHERE='WHERE', compare_column='user_id',
            #                          compare_value=str(user_id))
            # print(user)
            # print(user[0][3])
            # email_id = user[0][3]
            data = connecsiObj.get_conversations_by_message_id(message_id=str(message_id))
            print(data)
            columns = ['conv_id','message_id', 'date', 'from_email_id', 'to_email_id', 'subject', 'message', 'user_id',
                       'user_type','deleted','deleted_from_bin','deleted_from_user_id','deleted_from_bin_user_id']
            response_list = []
            for item in data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            print(response_list)
            return {'data': response_list}
        except Exception as e:
            return {"response": e}, 500

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
        password = "ezadteam123"
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(email_content)

        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        # Login Credentials for sending the mail
        server.login(msg['From'], password)
        server.sendmail(msg['From'], [msg['To']], msg.as_string())


@ns_messages.route('/conversations/<string:to_email_id>')
class MailBox(Resource):
    def get(self,to_email_id):
        ''' Get Conversations by to email id'''
        try:
            connecsiObj = ConnecsiModel()
            data = connecsiObj.get_conversations_by_to_email_id(to_email_id=str(to_email_id))
            print(data)
            columns = ['conv_id','message_id', 'date', 'from_email_id', 'to_email_id', 'subject', 'message', 'user_id',
                       'user_type']
            response_list = []
            for item in data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}
        except Exception as e:
            return {"response": e}, 500

@ns_messages.route('/conversations/sent/<string:from_email_id>')
class MailBox(Resource):
    def get(self,from_email_id):
        ''' Get Conversations by from email id'''
        try:
            connecsiObj = ConnecsiModel()
            data = connecsiObj.get_conversations_by_from_email_id(from_email_id=str(from_email_id))
            print(data)
            columns = ['conv_id','message_id', 'date', 'from_email_id', 'to_email_id', 'subject', 'message', 'user_id',
                       'user_type']
            response_list = []
            for item in data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}
        except Exception as e:
            return {"response": e}, 500




@ns_messages.route('/conversations/delete/<string:message_id>/<string:conv_id>/<string:user_id>')
class Delete(Resource):
    def put(self,message_id,conv_id,user_id):
        ''' Delete message from Conversations by  message_id,conv_id and from user_id'''
        try:
            connecsiObj = ConnecsiModel()
            data = connecsiObj.delete_message_from_conversation(message_id=message_id,conv_id=conv_id,user_id=user_id)
            print(data)
            return {'data': data}
        except Exception as e:
            return {"response": e}, 500

@ns_messages.route('/delete/<string:message_id>/<string:user_id>')
class Delete(Resource):
    def put(self,message_id,user_id):
        ''' Delete message from messages by message_id and from user_id'''
        try:
            connecsiObj = ConnecsiModel()
            data = connecsiObj.delete_message_from_messages(message_id=message_id,user_id=user_id)
            print(data)
            return {'data': data}
        except Exception as e:
            return {"response": e}, 500
