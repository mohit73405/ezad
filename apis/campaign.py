from flask import Flask, request, session
from flask_restplus import Resource, Api, fields, Namespace
from model.ConnecsiModel import ConnecsiModel
from passlib.hash import sha256_crypt
import datetime

ns_campaign = Namespace('Campaign', description='Brand Campaign')

brand_campaign_form = ns_campaign.model('Brand Campaign', {
    'campaign_name' : fields.String(required=True, description='Campaign Name'),
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
    'campaign_description': fields.String(required=True, description='Campaign description'),
    'arrangements': fields.String(required=True, description='Arrangements'),
    'kpis': fields.String(required=True, description='KPIs'),
    'is_classified_post': fields.String(required=False, description='Classified Post',default='false')

})




@ns_campaign.route('/<string:user_id>')
class Campaign(Resource):
    @ns_campaign.expect(brand_campaign_form)
    def post(self,user_id):
        ''' Add New Campaign'''
        data_json = request.get_json()
        campaign_name = data_json.get('campaign_name')
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
        campaign_description = data_json.get('campaign_description')
        arrangements = data_json.get('arrangements')
        kpis = data_json.get('kpis')
        is_classified_post = data_json.get('is_classified_post')
        data = [campaign_name, from_date, to_date, budget, currency, channels,
                regions, min_lower, max_upper, video_cat, target_url, campaign_description, arrangements,
                kpis, user_id,is_classified_post,files]
        columns = ['campaign_name', 'from_date', 'to_date', 'budget', 'currency', 'channels', 'regions',
                   'min_lower_followers', 'max_upper_followers', 'video_cat_id', 'target_url', 'campaign_description',
                   'arrangements', 'kpis', 'user_id','is_classified_post','files']
        connecsiObj = ConnecsiModel()
        res=''
        try:
            res=connecsiObj.insert__(table_name='brands_campaigns', columns=columns, data=data)
            return {'response' : res}
        except Exception as e:
            print(e)
            return {'response':res}

    def get(self,user_id):
        ''' get all campaings by user id'''
        try:
            connecsiObj = ConnecsiModel()
            all_campaigns_data = connecsiObj.get__(table_name='brands_campaigns', STAR='*', WHERE='WHERE', compare_column='user_id',compare_value=str(user_id))
            columns = ['campaign_id','user_id','campaign_name', 'from_date', 'to_date', 'budget', 'currency', 'channels', 'regions',
                       'min_lower_followers', 'max_upper_followers','files', 'video_cat_id', 'target_url',
                       'campaign_description',
                       'arrangements', 'kpis', 'is_classified_post']
            response_list = []
            for item in all_campaigns_data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}

        except Exception as e:
            print(e)







@ns_campaign.route('/<string:campaign_id>/<string:user_id>')
class Campaign(Resource):
    def get(self,campaign_id,user_id):
        ''' get Campaign details by campaign id'''
        try:
            connecsiObj = ConnecsiModel()
            campaign_data = connecsiObj.get_campaign_details_by_campaign_id_and_user_id(campaign_id=campaign_id,user_id=user_id)
            columns = ['campaign_id','user_id','campaign_name', 'from_date', 'to_date', 'budget', 'currency', 'channels', 'regions',
                       'min_lower_followers', 'max_upper_followers','files', 'video_cat_id', 'target_url',
                       'campaign_description',
                       'arrangements', 'kpis', 'is_classified_post']
            response_list = []
            for item in campaign_data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}

        except Exception as e:
            print(e)

    @ns_campaign.expect(brand_campaign_form)
    def put(self,campaign_id, user_id):
        data_json = request.get_json()
        campaign_name = data_json.get('campaign_name')
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
        campaign_description = data_json.get('campaign_description')
        arrangements = data_json.get('arrangements')
        kpis = data_json.get('kpis')
        is_classified_post = data_json.get('is_classified_post')
        data = [campaign_name, from_date, to_date, budget, currency, channels,
                regions, min_lower, max_upper, video_cat, target_url, campaign_description, arrangements,
                kpis, user_id, is_classified_post, files]
        columns = ['campaign_name', 'from_date', 'to_date', 'budget', 'currency', 'channels', 'regions',
                   'min_lower_followers', 'max_upper_followers', 'video_cat_id', 'target_url', 'campaign_description',
                   'arrangements', 'kpis', 'user_id', 'is_classified_post', 'files']
        connecsiObj = ConnecsiModel()
        res=''
        try:
            res = connecsiObj.update__(table_name='brands_campaigns', columns=columns, data=data,WHERE='WHERE',compare_column='campaign_id',compare_value=campaign_id)
            return {'response': res},201
        except Exception as e:
            print(e)
            return {'response': res},500


@ns_campaign.route('/channel_status_for_campaign/<string:channel_id>')
class Campaign(Resource):
    def get(self,channel_id):
        ''' get Channel details and status for campaigns by channel id'''
        try:
            connecsiObj = ConnecsiModel()
            channel_campaign_message_status_data=connecsiObj.get_channel_campaign_message_status(channel_id=channel_id)
            columns = ['campaign_id', 'campaign_name','message_id','status']
            response_list = []
            for item in channel_campaign_message_status_data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}

        except Exception as e:
            print(e)


@ns_campaign.route('/update_channel_status_for_campaign/<string:message_id>/<string:campaign_id>/<string:status>')
class Campaign(Resource):
    def put(self,message_id,campaign_id,status):
        ''' update Channel status campaigns by message id and campaign id'''
        try:
            connecsiObj = ConnecsiModel()
            connecsiObj.update_channel_campaign_message_status_by_message_id_campaign_id(message_id=message_id,campaign_id=campaign_id,status=status)

            return {'response': 1},201

        except Exception as e:
            print(e)

