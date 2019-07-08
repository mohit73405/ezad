import urllib.parse

from flask import Flask, request, session
from flask_restplus import Resource, Api, fields, Namespace
from model.ConnecsiModel import ConnecsiModel
from passlib.hash import sha256_crypt
import datetime

ns_graph_history = Namespace('GraphHistory', description='History details for graphs')

@ns_graph_history.route('/getNoOfFollowersHistory/<string:channel_name>/<string:channel_id>')
class History(Resource):
    def get(self,channel_name,channel_id):
        """get no of followers history by channel name and id"""
        modelObj = ConnecsiModel()
        if channel_name == 'youtube':
            columns = ['channel_id', 'subscriberCount_gained', 'inserted_date']
            channel_history_data = modelObj.get__(table_name='youtube_channels_history', columns=columns,WHERE='WHERE'
                                          ,compare_column='channel_id',compare_value=str(channel_id))
            response_list = []
            response_columns = ['channel_id','no_of_followers','date_time']
            print(channel_history_data)
            channel_history_data = list(channel_history_data)
            print(channel_history_data)
            # for item in channel_history_data:
            #     list(item)
            #     print(item)
            #     item[2] = item[2].strftime("%Y-%b-%d")
            #     dict_temp = dict(zip(response_columns, item))
            #     response_list.append(dict_temp)
            # for item in channel_history_data:
            #     dict_temp = dict(zip(response_columns, item))
            #     response_list.append(dict_temp)
            return {'data': response_list}


