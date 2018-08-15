from flask import Flask, request, session
from flask_restplus import Resource, Api, fields, Namespace
from model.ConnecsiModel import ConnecsiModel
from passlib.hash import sha256_crypt
import datetime

ns_youtube = Namespace('Youtube', description='Youtube Apis')

search_channels_form = ns_youtube.model('Search Channels', {
    'category_id' : fields.String(required=False, description='Category ID'),
    'country' : fields.String(required=False, description='Country'),
    'min_lower' : fields.Integer(required=False, description='Min Followers'),
    'max_upper' : fields.Integer(required=False, description='Max Followers'),
    'sort_order' : fields.String(required=False, description='Sort Order')
})


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

@ns_youtube.route('/searchChannels/<string:channel>')
class SearchChannels(Resource):
    @ns_youtube.expect(search_channels_form)
    def post(self,channel):
        '''search channels'''
        form_data = request.get_json()
        category_id = form_data.get('category_id')
        country = form_data.get('country')
        min_lower = form_data.get('min_lower')
        max_upper = form_data.get('max_upper')
        sort_order = form_data.get('sort_order')
        connecsiObj=ConnecsiModel()
        data = connecsiObj.search_inf(channel_id=channel,
                                      min_lower=str(min_lower), max_upper=str(max_upper)
                                      , category_id=str(category_id), country=str(country), sort_order=sort_order)
        return {'data':data}

