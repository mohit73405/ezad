from flask import Flask, request, session
from flask_restplus import Resource, Api, fields, Namespace
from model.ConnecsiModel import ConnecsiModel
from passlib.hash import sha256_crypt
import datetime

ns_messages = Namespace('Messages', description='Messages Operations')

message_form = ns_messages.model('Message Details', {
    'from_email_id' : fields.String(required=True, description='From Email Id'),
    'to_email_id' : fields.String(required=True, description='To Email Id'),
    'date' : fields.String(required=True, description='Date'),
    'subject' : fields.String(required=True, description='Subject'),
    'message' : fields.String(required=True, description='Message')
})



@ns_messages.route('/')
class Message(Resource):
    @ns_messages.expect(message_form)
    def post(self):
        '''Send message'''
        form_data = request.get_json()
        from_email_id = form_data.get('from_email_id')
        to_email_id = form_data.get('to_email_id')
        date = form_data.get('date')
        subject = form_data.get('subject')
        message = form_data.get('message')

        columns = ['from_email_id', 'to_email_id', 'date', 'subject', 'message']
        data = [from_email_id, to_email_id, date, subject, message]
        result=0
        try:
            connecsiObj = ConnecsiModel()
            result = connecsiObj.insert__(table_name='messages',columns=columns,data=data,IGNORE='IGNORE')
            return {'response': result},200
        except: return {'response': result},500
