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
        '''Influencer login  details by user_id'''
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
        data=(first_name,last_name,phone,categories,website,country,city)
        try:
            connecsiObj = ConnecsiModel()
            connecsiObj.update_inf_details(channel_id=user_id,data=data)
            connecsiObj.update_youtube_inf_country(channel_id=user_id,country=country)
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
                    print('mapped twitter_module channel = ',channels[1])
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
            columns = ['campaign_id','campaign_name','campaign_status','user_id','brand_first_name',
                       'brand_last_name','regions','profile_pic',
                       'proposal_id','proposal_from_date','proposal_to_date','currency',
                       'proposal_price','mapped_youtube_channel_id','mapped_twitter_channel_id','proposal_channels',
                       'confirmed','channel_campaign_status']
            response_list = []
            for item in influencer_campaigns_data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}

        except Exception as e:
            print(e)


@ns_influencer.route('/getMyCampaignDetails/<string:user_id>/<string:proposal_id>')
class Influencer(Resource):
    def get(self,user_id,proposal_id):
        ''' get Influencer campaing by channel id and proposal id'''
        try:
            connecsiObj = ConnecsiModel()
            influencer_campaigns_data = connecsiObj.getInfluencerCampaignDetails(channel_id=str(user_id),proposal_id=str(proposal_id))

            columns = ['campaign_id','campaign_name','campaign_status','user_id','brand_first_name',
                       'brand_last_name','regions','profile_pic','email_id',
                       'proposal_id','proposal_from_date','proposal_to_date','currency',
                       'proposal_price','proposal_description','proposal_arrangements','proposal_kpis','proposal_target_url',
                       'proposal_ref_link','campaign_files','regions','video_cat_id','video_cat_name',
                       'mapped_youtube_channel_id','mapped_twitter_channel_id',
                       'proposal_channels','confirmed','channel_campaign_status']
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
        columns = ['youtube_channel_id','twitter_channel_id','confirmed']

        data = connecsiObj.get__(table_name='channels_mapper',WHERE='WHERE',columns=columns,compare_column='youtube_channel_id',compare_value=channel_id)
        response_list = []
        for item in data:
            dict_temp = dict(zip(columns, item))
            response_list.append(dict_temp)
        return {'data': response_list}


@ns_influencer.route('/getDetailsByUserId/<string:user_id>')
class Influencer(Resource):
    def get(self, user_id):
        '''Influencer and channel details by user_id'''
        connecsiObj = ConnecsiModel()
        columns = ['first_name', 'last_name', 'business_email', 'phone',
                   'categories','website', 'country', 'city', 'channel_id',
                   'mapped_youtube_channel_id', 'mapped_twitter_channel_id','mapped_insta_channel_id',
                   'confirmed','title','channel_img','youtube_country','facebook_url','twitter_url','insta_url',
                   'twitter_business_email','twitter_screen_name','twitter_title','twitter_channel_img',
                   'twitter_hashtags','insta_username']
        data = connecsiObj.get_inf_and_channel_details(user_id=str(user_id))

        columns_categories=['youtube_video_cat','youtube_video_cat_id']
        data_categories = connecsiObj.get_youtube_cetegories_id_and_name(user_id=user_id)

        response_list = []
        for item in data:
            dict_temp = dict(zip(columns, item))
            response_list.append(dict_temp)
        for item in data_categories:
            dict_temp = dict(zip(columns_categories, item))
            response_list.append(dict_temp)
        print('categories =',data_categories)

        return {'data': response_list}


@ns_influencer.route('/addCategoriesToChannel/<string:user_id>/<string:video_cat_id>')
class Influencer(Resource):
    def get(self,user_id,video_cat_id):
        '''add Categories to channel user id '''
        connecsiObj = ConnecsiModel()
        response = connecsiObj.insert_categories_to_youtube_channel(channel_id=user_id,video_cat_id=video_cat_id)
        return response

    def delete(self,user_id,video_cat_id):
        '''remove Category from youtube channel user id '''
        connecsiObj = ConnecsiModel()
        response = connecsiObj.delete_category_from_youtube_channel(channel_id=user_id,video_cat_id=video_cat_id)
        return response


@ns_influencer.route('/addCategoriesToTwitterChannel/<string:twitter_id>/<string:category_id>')
class Influencer(Resource):
    def get(self,twitter_id,category_id):
        '''add Categories to twitter channel by twitter id '''
        connecsiObj = ConnecsiModel()
        response = connecsiObj.insert_categories_to_twitter_channel(twitter_id=twitter_id, category_id=category_id)
        return response

    def delete(self,twitter_id,category_id):
        '''remove Category from twitter channel twitter id '''
        connecsiObj = ConnecsiModel()
        response = connecsiObj.delete_category_from_twitter_channel(twitter_id=twitter_id,category_id=category_id)
        return response