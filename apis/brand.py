from flask import Flask, request, session
from flask_restplus import Resource, Api, fields, Namespace
from model.ConnecsiModel import ConnecsiModel
from passlib.hash import sha256_crypt
import datetime

ns_brand = Namespace('Brand', description='Brand Operations')

brand_form = ns_brand.model('Brand Details', {
    'first_name' : fields.String(required=True, description='First Name'),
    'last_name' : fields.String(required=True, description='Last Name'),
    'company_name' : fields.String(required=True, description='Company Name'),
    'email' : fields.String(required=True, description='Email'),
    'password' : fields.String(required=True, description='Password')
})

brand_change_password = ns_brand.model('Brand change passoword', {
    # 'old_password' : fields.String(required=True, description='Old Password'),
    'new_password' : fields.String(required=True, description='New Password'),
    # 'con_new_password' : fields.String(required=True, description='Confirm New Password')
})


brand_update_profile_pic = ns_brand.model('Brand update profile pic', {
    'profile_pic' : fields.String(required=True, description='Profile Pic'),
})
brand_create_alert_form = ns_brand.model('Brand create alert form', {
    'channel_id' : fields.String(required=True, description='Channel ID'),
    'alert_followers' : fields.String(required=False, description='Alert Followers'),
    'alert_views' : fields.String(required=False, description='Alert Views'),
    'alert_likes' : fields.String(required=False, description='Alert Likes'),
    'alert_comments' : fields.String(required=False, description='Alert Comments')
})


brand_edit_form = ns_brand.model('Brand Details Update', {
    'first_name' : fields.String(required=True, description='First Name'),
    'last_name' : fields.String(required=True, description='Last Name'),
    'phone': fields.String(required=True, description='Phone'),
    'position': fields.String(required=True, description='Position'),
    'company_name': fields.String(required=True, description='Company Name'),
    'url': fields.String(required=True, description='URL'),
    'country': fields.String(required=True, description='Country'),
    'no_of_employees': fields.String(required=True, description='No Of Employees'),
    'city': fields.String(required=True, description='City'),
    'monthly_budget': fields.String(required=True, description='Monthly Budget'),
    'business_sector': fields.String(required=True, description='Business Sector'),
    'facebook_url': fields.String(required=False, description='Facebook Url'),
    'twitter_url': fields.String(required=False, description='Twitter Url'),
    'insta_url': fields.String(required=False, description='Instegram Url'),
    'youtube_url': fields.String(required=False, description='Youtube Url')
})

@ns_brand.route('/register')
class Brand(Resource):
    @ns_brand.expect(brand_form)
    def post(self):
        '''Registers Brand Details'''
        form_data = request.get_json()
        password_sha = sha256_crypt.encrypt(str(form_data.get('password')))
        pass_dict = {'password':password_sha}
        role = {'role':'Admin'}
        form_data.update(pass_dict)
        form_data.update(role)
        first_name = form_data.get('first_name')
        last_name = form_data.get('last_name')
        company_name = form_data.get('company_name')
        email = form_data.get('email')
        password_sha = form_data.get('password')
        role = form_data.get('role')
        columns = ['first_name', 'last_name', 'email_id', 'company_name', 'password', 'role']
        data = [first_name, last_name, email, company_name, password_sha, role]
        result=0
        try:
            connecsiObj = ConnecsiModel()
            result = connecsiObj.insert__(table_name='users_brands',columns=columns,data=data,IGNORE='IGNORE')
            return {'response': result},201
        except: return {'response': result},500

@ns_brand.route('/')
class Brand(Resource):
    def get(self):
        '''List of all Brands'''
        connecsiObj = ConnecsiModel()
        columns = ['user_id','first_name','last_name','company_name','email_id','role']
        data = connecsiObj.get__(table_name='users_brands',columns=columns)
        return {'data':data},200

@ns_brand.route('/<string:user_id>')
class Brand(Resource):
    def get(self,user_id):
        '''Brand details by user_id'''
        connecsiObj = ConnecsiModel()
        columns = ['user_id', 'first_name', 'last_name', 'company_name', 'email_id', 'role','phone','position','url','country'
                   ,'no_of_employees','city','monthly_budget','business_sector','facebook_url','twitter_url',
                   'insta_url','youtube_url','profile_pic']
        data = connecsiObj.get__(table_name='users_brands',columns=columns,WHERE='WHERE',compare_column='user_id',compare_value=str(user_id))
        response_dict = dict(zip(columns, data[0]))
        print(response_dict)
        return {'data':response_dict},200

    @ns_brand.expect(brand_edit_form)
    def put(self,user_id):
        '''Update Brand Details'''
        form_data = request.get_json()
        first_name = form_data.get('first_name')
        last_name = form_data.get('last_name')
        phone = form_data.get('phone')
        position = form_data.get('position')
        url = form_data.get('url')
        country = form_data.get('country')
        no_of_employees = form_data.get('no_of_employees')
        city = form_data.get('city')
        monthly_budget = form_data.get('monthly_budget')
        business_sector = form_data.get('business_sector')
        company_name = form_data.get('company_name')
        facebook_url= form_data.get('facebook_url')
        twitter_url = form_data.get('twitter_url')
        insta_url = form_data.get('insta_url')
        youtube_url = form_data.get('youtube_url')
        columns = ['first_name', 'last_name', 'company_name', 'phone', 'position', 'url',
                   'country', 'no_of_employees', 'city', 'monthly_budget', 'business_sector','facebook_url','twitter_url',
                   'insta_url','youtube_url']
        data=(first_name,last_name,company_name,phone,position,url,country,no_of_employees,city,monthly_budget,business_sector,
              facebook_url,twitter_url,insta_url,youtube_url)
        try:
            connecsiObj = ConnecsiModel()
            connecsiObj.update__(table_name='users_brands',columns=columns,WHERE='WHERE',data=data,compare_column='user_id',compare_value=str(user_id))
            return {"response" : 1},200
        except Exception as e:
            return {"response": e},500


@ns_brand.route('/addToFavList/<string:channel_id>/<string:user_id>')
class Brand(Resource):
    def post(self,channel_id,user_id):
        '''add influencer to fav list'''
        columns = ['channel_id', 'user_id', 'alert_followers', 'alert_views', 'alert_likes', 'alert_comments']
        data = [channel_id, user_id, '', '', '', '']
        result = 0
        try:
            connecsiObj = ConnecsiModel()
            result = connecsiObj.insert__(table_name='brands_inf_fav_list', columns=columns, data=data,IGNORE='IGNORE')
            return {'response': result}, 201
        except:
            return {'response': result}, 500


@ns_brand.route('/getInfluencerFavList/<string:user_id>')
class Brand(Resource):
    def get(self,user_id):
        '''get all Fav influencer list by user_id'''
        columns = ['channel_id', 'title', 'channel_img', 'desc', 'subscriberCount_gained', 'subscriberCount_lost',
                   'business_email', 'total_100video_views',
                   'total_100video_views_unique', 'total_100video_likes', 'total_100video_dislikes',
                   'total_100video_comments', 'total_100video_shares',
                   'facebook_url', 'insta_url', 'twitter_url','alert_followers','alert_views','alert_likes','alert_comments']
        connecsiObj = ConnecsiModel()
        data = connecsiObj.get_fav_inf_list(user_id=user_id)
        response_list = []
        for item in data:
            dict_temp = dict(zip(columns, item))
            response_list.append(dict_temp)
        # print(response_list)
        return {'data': response_list}


@ns_brand.route('/changePassword/<string:user_id>')
class Brand(Resource):
    @ns_brand.expect(brand_change_password)
    def put(self,user_id):
        '''Update Brands password'''
        form_data = request.get_json()
        new_password = form_data.get('new_password')
        password_sha = sha256_crypt.encrypt(str(new_password))
        columns = ['password']
        data = (password_sha)
        try:
            connecsiObj = ConnecsiModel()
            connecsiObj.update__(table_name='users_brands', columns=columns, WHERE='WHERE', data=data,
                                 compare_column='user_id', compare_value=str(user_id))
            return {"response": 1}, 200
        except Exception as e:
            return {"response": e}, 500

@ns_brand.route('/updateProfilePic/<string:user_id>')
class Brand(Resource):
    @ns_brand.expect(brand_update_profile_pic)
    def put(self,user_id):
        '''Update Brands Profile Pic'''
        form_data = request.get_json()
        profile_pic = form_data.get('profile_pic')
        columns = ['profile_pic']
        data = (profile_pic)
        try:
            connecsiObj = ConnecsiModel()
            connecsiObj.update__(table_name='users_brands', columns=columns, WHERE='WHERE', data=data,
                                 compare_column='user_id', compare_value=str(user_id))
            return {"response": 1}, 200
        except Exception as e:
            return {"response": e}, 500


@ns_brand.route('/createInfluencerAlerts/<string:user_id>')
class Brand(Resource):
    @ns_brand.expect(brand_create_alert_form)
    def put(self,user_id):
        '''Create alerts for Fav Influencer'''
        form_data = request.get_json()
        channel_id = form_data.get('channel_id')
        alert_followers = form_data.get('alert_followers')
        alert_views = form_data.get('alert_views')
        alert_likes = form_data.get('alert_likes')
        alert_comments = form_data.get('alert_comments')
        columns = ['user_id','channel_id','alert_followers','alert_views','alert_likes','alert_comments']
        data = (user_id,channel_id,alert_followers,alert_views,alert_likes,alert_comments)
        connecsiObj = ConnecsiModel()
        fav_list = connecsiObj.get_fav_inf_list(user_id=user_id)
        present=0
        for item in fav_list:
            if item[0] == channel_id:
                present=1
                break

        if present == 1:
            try:
                connecsiObj = ConnecsiModel()
                connecsiObj.insert__(table_name='brands_inf_fav_list',columns=columns,data=data)
                return {"response": 1}, 200
            except Exception as e:
                return {"response": e}, 500

        else:
            try:
                connecsiObj = ConnecsiModel()
                connecsiObj.create_alert_for_fav_influencer(user_id=user_id,channel_id=channel_id,alert_followers=alert_followers
                                                            ,alert_views=alert_views,alert_likes=alert_likes,alert_comments=alert_comments)
                return {"response": 1}, 200
            except Exception as e:
                return {"response": e}, 500

