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
        # columns = ['channel_id', 'twitter_url', 'country', 'facebook_url', 'insta_url']
        # channel_data = modelObj.get__(table_name='youtube_channel_details', columns=columns,WHERE='WHERE'
        #                               ,compare_column='channel_id',compare_value=str(youtube_channel_id))
        #
        # response_list = []
        # columns = ['total_videos']
        # for item in data:
        #     dict_temp = dict(zip(columns, item))
        #     response_list.append(dict_temp)
        # return {'data': response_list}


