from flask import Flask, request, session
from flask_restplus import Resource, Api, fields, Namespace
from model.ConnecsiModel import ConnecsiModel
from passlib.hash import sha256_crypt
import datetime

ns_notifications = Namespace('Notifications', description='Notifications')

notifications_form = ns_notifications.model('Notifications', {
    'display_message':fields.String(required=True, description='display message'),
    'read_unread' : fields.String(required=True, description='read unread')
})

@ns_notifications.route('/<string:user_id>')
class Notifications(Resource):
    @ns_notifications.expect(notifications_form)
    def post(self,user_id):
        form_data = request.get_json()
        display_message = form_data.get('display_message')
        read_unread = form_data.get('read_unread')

        connecsiObj = ConnecsiModel()
        columns = ['user_id','display_message','read_unread']

        data = [user_id, display_message, read_unread]
        notification_id = connecsiObj.insert__(table_name='notifications',columns=columns, data=data)
        return {'notification_id': notification_id },201

    def get(self,user_id):
        connecsiObj = ConnecsiModel()
        columns = ["notification_id", "user_id", "display_message", "read_unread"]
        data_tuple = connecsiObj.get__(table_name='notifications',columns=columns,WHERE='WHERE',compare_column='user_id',compare_value=str(user_id))
        response_list = []
        for item in data_tuple:
            dict_temp = dict(zip(columns, item))
            response_list.append(dict_temp)
        # print(response_list)
        return {'data': response_list},200

@ns_notifications.route('/<string:user_id>/<int:notification_id>')
class Notifications(Resource):
    def put(self,user_id,notification_id):
        connecsiObj = ConnecsiModel()
        res = connecsiObj.mark_notification_as_read(user_id=user_id,notification_id=notification_id)
        return {'response': res },201

    # def get(self,user_id,notification_id):
    #     connecsiObj = ConnecsiModel()
    #     columns = ["notification_id", "user_id", "display_message", "read_unread"]
    #     data_tuple = connecsiObj.get_notification_details()
    #     response_list = []
    #     for item in data_tuple:
    #         dict_temp = dict(zip(columns, item))
    #         response_list.append(dict_temp)
    #     # print(response_list)
    #     return {'data': response_list},200