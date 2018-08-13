from flask import Flask, request, session
from flask_restplus import Resource, Api, fields, Namespace
from model.ConnecsiModel import ConnecsiModel
from passlib.hash import sha256_crypt
import datetime

ns_youtube = Namespace('Youtube', description='Youtube Apis')


@ns_youtube.route('/regionCodes')
class RegionCodes(Resource):
    def get(self):
        '''get all youtube region codes'''
        connecsiObj = ConnecsiModel()
        region_codes = connecsiObj.get__(table_name='youtube_region_codes', STAR='*')
        return {'data' : region_codes}

@ns_youtube.route('/regionCode/<string:regionCode>')
class RegionCode(Resource):
    def get(self,regionCode):
        '''get country name by region code'''
        connecsiObj = ConnecsiModel()
        data = connecsiObj.get__(table_name='youtube_region_codes',STAR='*',WHERE='WHERE',compare_column='regionCode',compare_value=str(regionCode))
        return {'data' : data}

@ns_youtube.route('/videoCategories')
class VideoCategories(Resource):
    def get(self):
        ''' get all video categories'''
        connecsiObj = ConnecsiModel()
        video_categories = connecsiObj.get__(table_name='youtube_video_categories', STAR='*')
        return {'data': video_categories}

