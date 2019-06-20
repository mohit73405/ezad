from flask import Flask, request, session
from flask_restplus import Resource, Api, fields, Namespace
from model.ConnecsiModel import ConnecsiModel
from passlib.hash import sha256_crypt
import datetime

ns_classified = Namespace('Classified', description='Classified')

brand_classified_form = ns_classified.model('Classified', {
    'classified_name' : fields.String(required=True, description='Classified Name'),
    'from_date' : fields.String(required=True, description='From Date'),
    'to_date' : fields.String(required=True, description='To Date'),
    'budget' : fields.Integer(required=True, description='Budget'),
    'currency' : fields.String(required=True, description='Currency'),
    # 'channels' : fields.List(required=True, description='Channels',cls_or_instance=fields.String),
    'channels' : fields.String(required=True, description='Channels'),
    'regions' : fields.String(required=True, description='Regions'),
    'min_lower': fields.Integer(required=True, description='Min Followers'),
    'max_upper': fields.Integer(required=True, description='Max Followers'),
    'files': fields.String(required=False, description='Files'),
    'video_cat': fields.String(required=True, description='Video Category'),
    'target_url': fields.Url(required=True, description='Target URL'),
    'classified_description': fields.String(required=True, description='Classified description'),
    'arrangements': fields.String(required=True, description='Arrangements'),
    'kpis': fields.String(required=True, description='KPIs'),
    'convert_to_campaign': fields.String(required=False, description='Convert to Campaign',default='false')

})

@ns_classified.route('/<string:user_id>')
class Classified(Resource):
    @ns_classified.expect(brand_classified_form)
    def post(self,user_id):
        ''' Add New Classified'''
        data_json = request.get_json()
        classified_name = data_json.get('classified_name')
        from_date = data_json.get('from_date')
        to_date = data_json.get('to_date')
        budget = data_json.get('budget')
        currency = data_json.get('currency')
        channels = data_json.get('channels')
        regions = data_json.get('regions')
        min_lower = data_json.get('min_lower')
        max_upper = data_json.get('max_upper')
        files = data_json.get('files')
        video_cat = data_json.get('video_cat')
        target_url = data_json.get('target_url')
        classified_description = data_json.get('classified_description')
        arrangements = data_json.get('arrangements')
        kpis = data_json.get('kpis')
        convert_to_campaign = data_json.get('convert_to_campaign')
        posted_date = datetime.date.today()
        posted_date = datetime.date.strftime(posted_date, '%Y-%m-%d')
        data = [classified_name, from_date, to_date, budget, currency, channels,
                regions, min_lower, max_upper, video_cat, target_url, classified_description, arrangements,
                kpis, user_id,convert_to_campaign,files,posted_date]
        columns = ['classified_name', 'from_date', 'to_date', 'budget', 'currency', 'channels', 'regions',
                   'min_lower_followers', 'max_upper_followers', 'video_cat_id', 'target_url', 'classified_description',
                   'arrangements', 'kpis', 'user_id','convert_to_campaign','files','posted_date']
        connecsiObj = ConnecsiModel()
        try:
            connecsiObj.insert__(table_name='brands_classifieds', columns=columns, data=data)
            res = 1
            return {'response':res}
        except Exception as e:
            print(e)
            res = 0
            return {'response':res}

    def get(self,user_id):
        ''' get all Classifieds by user id'''
        try:
            connecsiObj = ConnecsiModel()
            all_classifieds_data = connecsiObj.get__(table_name='brands_classifieds', STAR='*', WHERE='WHERE', compare_column='user_id',compare_value=str(user_id))
            columns = ['classified_id','user_id','classified_name', 'from_date', 'to_date', 'budget', 'currency', 'channels', 'regions',
                       'min_lower_followers', 'max_upper_followers','files', 'video_cat_id', 'target_url',
                       'classified_description',
                       'arrangements', 'kpis', 'convert_to_campaign','no_of_views','no_of_replies','deleted','posted_date']
            response_list = []
            for item in all_classifieds_data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}

        except Exception as e:
            print(e)


@ns_classified.route('/<string:classified_id>/<string:user_id>')
class Classified(Resource):
    def get(self,classified_id,user_id):
        ''' get Classified details by classified id'''
        try:
            connecsiObj = ConnecsiModel()
            classified_data = connecsiObj.get_brand_classified_details_by_classified_id_and_user_id(classified_id=classified_id,user_id=user_id)
            columns = ['classified_id','user_id','classified_name', 'from_date', 'to_date', 'budget', 'currency', 'channels', 'regions',
                       'min_lower_followers', 'max_upper_followers','files', 'video_cat_id', 'target_url',
                       'classified_description',
                       'arrangements', 'kpis','convert_to_campaign','no_of_views','no_of_replies','deleted','posted_date']
            response_list = []
            for item in classified_data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}

        except Exception as e:
            print(e)

    @ns_classified.expect(brand_classified_form)
    def put(self, classified_id,user_id):
        ''' Edit Classified'''
        data_json = request.get_json()
        classified_name = data_json.get('classified_name')
        from_date = data_json.get('from_date')
        to_date = data_json.get('to_date')
        budget = data_json.get('budget')
        currency = data_json.get('currency')
        channels = data_json.get('channels')
        regions = data_json.get('regions')
        min_lower = data_json.get('min_lower')
        max_upper = data_json.get('max_upper')
        files = data_json.get('files')
        video_cat = data_json.get('video_cat')
        target_url = data_json.get('target_url')
        classified_description = data_json.get('classified_description')
        arrangements = data_json.get('arrangements')
        kpis = data_json.get('kpis')
        convert_to_campaign = data_json.get('convert_to_campaign')
        data = [classified_name, from_date, to_date, budget, currency, channels,
                regions, min_lower, max_upper, video_cat, target_url, classified_description, arrangements,
                kpis, user_id, convert_to_campaign, files]
        columns = ['classified_name', 'from_date', 'to_date', 'budget', 'currency', 'channels', 'regions',
                   'min_lower_followers', 'max_upper_followers', 'video_cat_id', 'target_url', 'classified_description',
                   'arrangements', 'kpis', 'user_id', 'convert_to_campaign', 'files']
        connecsiObj = ConnecsiModel()
        try:
            connecsiObj.update__(table_name='brands_classifieds', columns=columns, data=data, WHERE='WHERE',
                                 compare_column='classified_id', compare_value=classified_id)
            res = 1
            return {'response': res}
        except Exception as e:
            print(e)
            res = 0
            return {'response': res}

    def delete(self, classified_id, user_id):
        '''Delete Classified'''
        try:
            connecsiObj = ConnecsiModel()
            connecsiObj.delete_classified(classified_id=classified_id, user_id=user_id)
            res = 1
            return {'response': res}, 201
        except Exception as e:
            print(e)
            res = 0
            return {'response': res}, 500



@ns_classified.route('/NumberOfViews/<string:classified_id>/<string:user_id>/<string:no_of_views>')
class Classified(Resource):
    def put(self,classified_id,user_id,no_of_views):
        try:
            connecsiObj=ConnecsiModel()
            connecsiObj.update_classified_no_of_views(classified_id,user_id,no_of_views)
            res = 1
            return {'response': res},201
        except Exception as e:
            print(e)
            res = 0
            return {'response': res},500


@ns_classified.route('/NumberOfReplies/<string:classified_id>/<string:user_id>/<string:no_of_replies>')
class Classified(Resource):
    def put(self,classified_id,user_id,no_of_replies):
        try:
            connecsiObj=ConnecsiModel()
            connecsiObj.update_classified_no_of_replies(classified_id,user_id,no_of_replies)
            res = 1
            return {'response': res},201
        except Exception as e:
            print(e)
            res = 0
            return {'response': res},500

@ns_classified.route('/convertToCampaign/<string:classified_id>/<string:user_id>/')
class Classified(Resource):
    def put(self,classified_id,user_id):
        try:
            connecsiObj=ConnecsiModel()
            connecsiObj.convert_to_campaign(classified_id=classified_id,user_id=user_id)
            res = 1
            return {'response': res},201
        except Exception as e:
            print(e)
            res = 0
            return {'response': res},500


@ns_classified.route('/getAllClassifieds')
class Classified(Resource):
    def get(self):
        ''' get All Classifieds for Influencers'''
        try:
            connecsiObj = ConnecsiModel()
            offer_data = connecsiObj.get_all_classifieds_for_inf()
            columns = ['classified_id', 'user_id', 'classified_name', 'from_date', 'to_date', 'budget', 'currency',
                       'channels',
                       'regions',
                       'min_lower_followers', 'max_upper_followers', 'files', 'video_cat_id',
                       'classified_description',
                       'arrangements', 'kpis', 'no_of_views', 'no_of_replies'
                       ]
            response_list = []
            for item in offer_data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}

        except Exception as e:
            print(e)




@ns_classified.route('/searchClassifieds')
class Classified(Resource):
    def post(self):
        ''' Search Classifieds for Influencers'''
        try:
            form_data = request.get_json()
            channel_name = form_data.get('channel_name')
            category_id = form_data.get('video_cat')
            country = form_data.get('country')
            arrangements = form_data.get('arrangements')
            min_lower = form_data.get('min_lower')
            max_upper = form_data.get('max_upper')
            currency = form_data.get('currency')
            price_lower = form_data.get('min_lower_price')
            price_upper = form_data.get('max_upper_price')

            connecsiObj = ConnecsiModel()
            offer_data = connecsiObj.get_all_classifieds_for_influencers(channel_name,category_id,country,arrangements,min_lower,
                                                               max_upper,currency,price_lower,price_upper)
            columns = ['classified_id', 'user_id', 'classified_name', 'from_date', 'to_date', 'budget', 'currency',
                       'channels',
                       'regions',
                       'min_lower_followers', 'max_upper_followers', 'files', 'video_cat_id','target_url',
                       'classified_description',
                       'arrangements', 'kpis', 'no_of_views', 'no_of_replies','deleted','posted_date','first_name','last_name','profile_pic','email_id','video_cat_name'
                       ]
            response_list = []
            for item in offer_data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}

        except Exception as e:
            print(e)

