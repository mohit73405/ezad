from flask import Flask, request, session
from flask_restplus import Resource, Api, fields, Namespace
from model.ConnecsiModel import ConnecsiModel
from passlib.hash import sha256_crypt
import datetime



ns_influencer = Namespace('Influencer', description='Influencer Operations')

influencer_register_form = ns_influencer.model('Influencer Details',{
    'channel_id': fields.String(required=True,description='channel id'),
    'business_email': fields.String(required=True,description='Business Email')
})

influencer_edit_form = ns_influencer.model('Influencer Details Update', {
    'first_name' : fields.String(required=True, description='First Name'),
    'last_name' : fields.String(required=True, description='Last Name'),
    'phone': fields.String(required=True, description='Phone'),
    'categories': fields.String(required=True, description='Categories'),
    'website': fields.String(required=True, description='Website'),
    'country': fields.String(required=True, description='Country'),
    'city': fields.String(required=True, description='City'),
})


@ns_influencer.route('/<string:user_id>')
class Influencer(Resource):
    def get(self,user_id):
        '''Influencer details by user_id'''
        connecsiObj = ConnecsiModel()
        columns = ['youtube_first_name', 'youtube_last_name', 'youtube_business_email','youtube_phone','youtube_categories',
                   'youtube_website','youtube_country','youtube_city','youtube_channel_id',
                   'twitter_first_name', 'twitter_last_name', 'twitter_business_email', 'twitter_phone','twitter_categories',
                   'twitter_website', 'twitter_country', 'twitter_city', 'twitter_channel_id',
                   'mapped_youtube_channel_id','mapped_twitter_channel_id','confirmed']

        data = connecsiObj.get_all_inf_channels(user_id=str(user_id))
        response_list = []
        for item in data:
            dict_temp = dict(zip(columns, item))
            response_list.append(dict_temp)
        return {'data': response_list}




    @ns_influencer.expect(influencer_edit_form)
    def put(self,user_id):
        '''Update Influencer Details'''
        form_data = request.get_json()
        first_name = form_data.get('first_name')
        last_name = form_data.get('last_name')
        phone = form_data.get('phone')
        categories = form_data.get('categories')
        website = form_data.get('website')
        country = form_data.get('country')
        city = form_data.get('city')

        columns = ['first_name', 'last_name','phone', 'categories', 'website',
                   'country','city']
        data=(first_name,last_name,phone,categories,website,country,city)
        try:
            connecsiObj = ConnecsiModel()
            connecsiObj.update__(table_name='users_influencers',columns=columns,WHERE='WHERE',data=data,compare_column='channel_id',compare_value=str(user_id))
            return {"response" : 1},200
        except Exception as e:
            return {"response": e},500



@ns_influencer.route('/saveInfluencer')
class Brand(Resource):
    @ns_influencer.expect(influencer_register_form)
    def post(self):
        '''Registers Influencer Details'''
        form_data = request.get_json()
        channel_id= form_data.get('channel_id')
        # password_sha = sha256_crypt.encrypt('influencer123')
        email = form_data.get('business_email')
        columns = ['channel_id','business_email']
        data = [channel_id, email]

        try:
            connecsiObj = ConnecsiModel()
            channel_ids = connecsiObj.get__(table_name='users_influencers',columns=['channel_id'])
            channels_mapped_youtube = connecsiObj.get__(table_name='channels_mapper',STAR='*',WHERE='WHERE',compare_column='youtube_channel_id',compare_value=str(channel_id))
            print(channels_mapped_youtube)
            if channels_mapped_youtube:
                for channels in channels_mapped_youtube:
                    print('mapped twitter channel = ',channels[1])
                    mapped_twitter_channel=channels[1]

            channels_mapped_twitter = connecsiObj.get__(table_name='channels_mapper', STAR='*', WHERE='WHERE',
                                                compare_column='twitter_channel_id', compare_value=str(channel_id))
            print(channels_mapped_twitter)
            if channels_mapped_twitter:
                for channels in channels_mapped_twitter:
                    print('mapped youtube channel = ',channels[0])
                    mapped_youtube_channels=channels[0]

            result = connecsiObj.insert__(table_name='users_influencers',columns=columns,data=data)
            return {'response': result},201

        except:
            result=0
            return {'response': result},500

@ns_influencer.route('/getMyCampaigns/<string:user_id>')
class Influencer(Resource):
    def get(self,user_id):
        ''' get all campaings by channel id'''
        try:
            connecsiObj = ConnecsiModel()
            influencer_campaigns_data = connecsiObj.getAllInfluencerCampaigns(channel_id=str(user_id))
            # columns = ['channel_id','campaign_id','brand_user_id','campaign_name', 'from_date', 'to_date', 'budget', 'currency', 'channels', 'regions',
            #            'min_lower_followers', 'max_upper_followers','files', 'target_url',
            #            'campaign_description',
            #            'arrangements', 'kpis']

            columns = ['campaign_id','campaign_name','youtube_channel_id','twitter_channel_id']
            response_list = []
            for item in influencer_campaigns_data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}

        except Exception as e:
            print(e)


@ns_influencer.route('/GetDetailsByEmailId/<string:email_id>')
class Influencer(Resource):
    def get(self,email_id):
        '''Influencer details by email id '''
        connecsiObj = ConnecsiModel()
        columns = ['first_name', 'last_name', 'business_email','phone','categories','website','country','city','channel_id']
        data = connecsiObj.get__(table_name='users_influencers',columns=columns,WHERE='WHERE',compare_column='business_email',compare_value=str(email_id))
        response_dict = dict(zip(columns, data[0]))
        print(response_dict)
        return {'data':response_dict},200



@ns_influencer.route('/getMappedChannels/<string:channel_id>')
class Influencer(Resource):
    def get(self,channel_id):
        '''get all mapped channels by channel id'''
        connecsiObj = ConnecsiModel()
        columns = ['mapped_youtube_channel_id','mapped_twitter_channel_id','confirmed']

        data = connecsiObj.get_all_inf_channels(user_id=str(channel_id))
        response_list = []
        for item in data:
            dict_temp = dict(zip(columns, item))
            response_list.append(dict_temp)
        return {'data': response_list}