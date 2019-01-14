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
        channel_id = form_data.get('channel_id')
        date = form_data.get('date')
        subject = form_data.get('subject')
        message = form_data.get('message')

        columns = ['from_email_id', 'to_email_id','channel_id', 'date', 'subject', 'message','user_id','user_type']
        data = [from_email_id, to_email_id,channel_id, date, subject, message,user_id,user_type]
        print(data)
        result=0
        try:
            self.send_mail(subject=subject,to_email_id=to_email_id)
            connecsiObj = ConnecsiModel()
            message_id = connecsiObj.insert__(table_name='messages',columns=columns,data=data,IGNORE='IGNORE')
            if channel_id:
                connecsiObj.update_channel_campaign_message(channel_id=str(channel_id),message_id=str(message_id),status='Contacted')
            return {'response': result},200
        except Exception as e:
            print(e)
            return {'response': result},500

    def get(self,user_id,user_type):
        ''' get messages by user id and user type'''
        try:
            connecsiObj = ConnecsiModel()
            if user_type == 'brand':
                user = connecsiObj.get__(table_name='users_brands',STAR='*',WHERE='WHERE',compare_column='user_id',compare_value=str(user_id))
                print(user)
                print(user[0][3])
                email_id = user[0][3]
                data = connecsiObj.get_messages_by_email_id_and_user_type(email_id=str(email_id),user_type=user_type)
                print(data)
                columns = ['message_id','from_email_id', 'to_email_id','channel_id', 'date', 'subject', 'message', 'user_id', 'user_type',
                       'deleted','deleted_from_bin','deleted_from_user_id','deleted_from_bin_user_id']
                response_list = []
                for item in data:
                    dict_temp = dict(zip(columns, item))
                    response_list.append(dict_temp)
                return {'data': response_list}
            if user_type == 'influencer':
                user = connecsiObj.get__(table_name='users_influencers',STAR='*',WHERE='WHERE',compare_column='channel_id',compare_value=str(user_id))
                print(user)
                # print(user[0][2])
                email_id = user[0][2]
                data = connecsiObj.get_messages_by_email_id_and_user_type(email_id=str(email_id),user_type=user_type)
                print(data)
                columns = ['message_id','from_email_id', 'to_email_id','channel_id', 'date', 'subject', 'message', 'user_id', 'user_type',
                       'deleted','deleted_from_bin','deleted_from_user_id','deleted_from_bin_user_id']
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
        print('form data = ',form_data)
        print(type(form_data))
        from_email_id = form_data.get('conv_from_email_id')
        to_email_id = form_data.get('to_email_id')
        date = form_data.get('conv_date')
        print('conv_date = ',date)
        subject = form_data.get('subject')
        message = form_data.get('message')
        channel_id = form_data.get('channel_id')

        columns = ['message_id','conv_from_email_id', 'conv_to_email_id', 'conv_date', 'conv_subject', 'conv_message', 'user_id', 'user_type']
        data = [message_id,from_email_id, to_email_id, str(date), subject, message, user_id, user_type]
        print('data to insert = ',data)
        result = 0
        try:
            self.send_mail(subject=subject, to_email_id=to_email_id)
            connecsiObj = ConnecsiModel()
            result = connecsiObj.insert__(table_name='conversations', columns=columns, data=data, IGNORE='IGNORE')
            if channel_id:
                connecsiObj.update_channel_campaign_message(channel_id=str(channel_id),message_id=str(message_id),status='Negotiations')
            return {'response': result}, 200
        except Exception as e:
            print(e)
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
                       'user_type','deleted','deleted_from_bin','deleted_from_user_id','deleted_from_bin_user_id']
            response_list = []
            for item in data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}
        except Exception as e:
            return {"response": e}, 500


@ns_messages.route('/conversations/all/<string:user_type>')
class MailBox(Resource):
    def get(self,user_type):
        ''' Get Conversations by user type'''
        try:
            connecsiObj = ConnecsiModel()
            data = connecsiObj.get_conversations_by_user_type(user_type=str(user_type))
            print(data)
            columns = ['conv_id','message_id', 'date', 'from_email_id', 'to_email_id', 'subject', 'message', 'user_id',
                       'user_type','deleted','deleted_from_bin','deleted_from_user_id','deleted_from_bin_user_id']
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
                       'user_type','deleted','deleted_from_bin','deleted_from_user_id','deleted_from_bin_user_id']
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




@ns_messages.route('/sentWelcomeEmail/<string:user_id>/<string:user_type>')
class MailBox(Resource):
    @ns_messages.expect(message_form)
    def post(self,user_id,user_type):
        '''Send welcome email message'''
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


    def send_mail(self,subject,to_email_id):
        email_content = """
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
           <title>Connecsi</title>
        </head>
        <body>
        Welcome To Connecsi
        Thank you
        Connesi Team
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


@ns_messages.route('/addCampaignIdToMessageId/<string:message_id>/<string:campaign_id>/<string:channel_id>')
class MailBox(Resource):
    def post(self,message_id,campaign_id,channel_id):
        '''add campaign id to message'''
        columns=['channel_id','message_id','campaign_id','status']
        data=(channel_id,message_id,campaign_id,'Negotiations')
        connecsiObj = ConnecsiModel()
        result=0
        try:
            connecsiObj.insert__(table_name='channel_campaign_message',columns=columns,data=data)
            result=1
            return {'response': result}, 200
        except Exception as e:
            print(e)
            return {'response': result}, 500

@ns_messages.route('/getCampaignsAddedToMessage/<string:message_id>')
class MailBox(Resource):
    def get(self,message_id):
        ''' Get campaigns added to message by from message id'''
        try:
            connecsiObj = ConnecsiModel()
            data = connecsiObj.get_campaigns_added_to_message(message_id=str(message_id))
            print(data)
            columns = ['campaign_id','user_id', 'campaign_name', 'from_date', 'to_date', 'budget', 'currency', 'channels',
                       'regions','min_lower_followers','max_upper_followers','files','video_cat_id'
                       ,'target_url','campaign_description','arrangements','kpis','is_classified_post','deleted','campaign_status','channel_id','campaign_id','message_id','status']
            response_list = []
            for item in data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}
        except Exception as e:
            return {"response": e}, 500



@ns_messages.route('/uploadMessageFiles/<string:message_id>')
class MailBox(Resource):
    def post(self,message_id):
        '''Upload Files for messages id '''
        columns=['user_id','channel_id','message_id','message_files']
        form_data = request.get_json()
        user_id = form_data.get('user_id')
        channel_id = form_data.get('channel_id')
        # message_id = form_data.get('message_id')
        message_files = form_data.get('message_files')

        data=(user_id,channel_id,message_id,message_files)
        connecsiObj = ConnecsiModel()
        result=0
        try:
            connecsiObj.insert__(table_name='user_channel_message_files',columns=columns,data=data)
            result=1
            return {'response': result}, 200
        except Exception as e:
            print(e)
            return {'response': result}, 500


    def get(self,message_id):
        ''' Get uploaded message files by message id'''
        try:
            connecsiObj = ConnecsiModel()
            data = connecsiObj.get__(table_name='user_channel_message_files',STAR='*',WHERE='WHERE',compare_column='message_id',compare_value=str(message_id))
            print(data)
            # columns = ['campaign_id','user_id', 'campaign_name', 'from_date', 'to_date', 'budget', 'currency', 'channels',
            #            'regions','min_lower_followers','max_upper_followers','files','video_cat_id'
            #            ,'target_url','campaign_description','arrangements','kpis','is_classified_post','channel_id','campaign_id','message_id','status']
            columns = ['user_id', 'channel_id', 'message_id', 'message_files']
            response_list = []
            for item in data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}
        except Exception as e:
            return {"response": e}, 500



@ns_messages.route('/uploadMessageAgreements/<string:message_id>')
class MailBox(Resource):
    def post(self,message_id):
        '''Upload Agreements for messages id '''
        columns=['user_id','channel_id','message_id','message_agreements']
        form_data = request.get_json()
        user_id = form_data.get('user_id')
        channel_id = form_data.get('channel_id')
        # message_id = form_data.get('message_id')
        message_agreements = form_data.get('message_agreements')

        data=(user_id,channel_id,message_id,message_agreements)
        connecsiObj = ConnecsiModel()
        result=0
        try:
            connecsiObj.insert__(table_name='user_channel_message_agreements',columns=columns,data=data)
            result=1
            return {'response': result}, 200
        except Exception as e:
            print(e)
            return {'response': result}, 500


    def get(self,message_id):
        ''' Get uploaded message Agreements by message id'''
        try:
            connecsiObj = ConnecsiModel()
            data = connecsiObj.get__(table_name='user_channel_message_agreements',STAR='*',WHERE='WHERE',compare_column='message_id',compare_value=str(message_id))
            print(data)
            # columns = ['campaign_id','user_id', 'campaign_name', 'from_date', 'to_date', 'budget', 'currency', 'channels',
            #            'regions','min_lower_followers','max_upper_followers','files','video_cat_id'
            #            ,'target_url','campaign_description','arrangements','kpis','is_classified_post','channel_id','campaign_id','message_id','status']
            columns = ['user_id', 'channel_id', 'message_id', 'message_agreements']
            response_list = []
            for item in data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}
        except Exception as e:
            return {"response": e}, 500





@ns_messages.route('/ForgotPassword/<string:email_id>')
class MailBox(Resource):
    def post(self,email_id):
        '''Send password to given email id'''
        new_password=''
        connecsiObj = ConnecsiModel()

        new_password= email_id+'_111'
        password_sha = sha256_crypt.encrypt(str(new_password))
        columns = ['password']
        data = (password_sha)
        try:
            connecsiObj.update__(table_name='users_brands', columns=columns, WHERE='WHERE', data=data,
                                 compare_column='email_id', compare_value=str(email_id))
        except Exception as e:
            print(e)
        to_email_id = email_id
        subject = 'Your Password for Connecsi Admin'
        message = 'Your Password for Connecsi is '+ new_password + ', You can now login with this new temporary password and then change it'
        try:
            self.send_mail(subject=subject,to_email_id=to_email_id,message=message)
            result=1
            return {'response': result},200
        except Exception as e:
            print(e)
            result=0
            return {'response': result},500


    def send_mail(self,subject,to_email_id,message):
        email_content = '<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>Connecsi</title></head><body>' \
                        +message+ \
                        '</body></html>'
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
