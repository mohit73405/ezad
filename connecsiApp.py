from functools import wraps
import json
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging,jsonify
from model.ConnecsiModel import ConnecsiModel
from wtforms import Form, StringField, TextAreaField, PasswordField, validators,TextField
from passlib.hash import sha256_crypt
from flask_oauthlib.client import OAuth

connecsiApp = Flask(__name__)
# oauth = OAuth(connecsiApp)



# linkedin = oauth.remote_app(
#     'linkedin',
#     consumer_key='86ctp4ayian53w',
#     consumer_secret='3fdovLJRbWrQuu3u',
#     request_token_params={
#         'scope': 'r_basicprofile,r_emailaddress',
#         'state': 'RandomString',
#     },
#     base_url='https://api.linkedin.com/v1/',
#     request_token_url=None,
#     access_token_method='POST',
#     access_token_url='https://www.linkedin.com/uas/oauth2/accessToken',
#     authorize_url='https://www.linkedin.com/uas/oauth2/authorization',
# )

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('Unauthorized, Please login','danger')
            return redirect(url_for('index'))
    return wrap


@connecsiApp.route('/')
# @is_logged_in
def index():
    title='Connesi App Login Panel'
    data=[]
    data.append(title)
    return render_template('user/login.html',data=data)


# @connecsiApp.route('/loginLinkedin')
# def loginLinkedin():
#     return linkedin.authorize(callback=url_for('authorized', _external=True))

@connecsiApp.route('/registerBrand')
def registerBrand():
    return render_template('user/registerFormBrand.html')

@connecsiApp.route('/saveBrand',methods=['GET','POST'])
def saveBrand():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        company_name = request.form.get('company_name')
        password = request.form.get('password')
        password_sha = sha256_crypt.encrypt(str(password))
        data = [first_name,last_name,email,company_name,password_sha,'Admin']
        # print(data)

        columns = ['first_name','last_name','email_id','company_name','password','role']
        title = 'Connesi App Login Panel'
        try:
            connecsiObj = ConnecsiModel()
            res = connecsiObj.insert__(data=data,columns=columns,table_name='users_brands',IGNORE='IGNORE')
            print(res)
            if res == 1:
                flash("Brand Details Successfully Registered", 'success')
                title = 'Connesi App Login Panel'
                return render_template('user/login.html', title=title)
            else:
                flash("Internal error please try later", 'danger')
                return render_template('user/login.html', title=title)
        except:
            flash("Internal error please try later", 'danger')
            return render_template('user/login.html',title=title)



#Logout
@connecsiApp.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('index'))


# User login
@connecsiApp.route('/login',methods=['POST'])
def login():
    if request.method=='POST':
        if 'brand' in request.form:
            email_id = request.form.get('brand_email')
            password = request.form.get('brand_password')
            print(email_id)
            print(password)
            # password_sha = sha256_crypt.encrypt(str(password))
            connecsiObj = ConnecsiModel()
            data = connecsiObj.get_user_by_email_id(table_name='users_brands',email_id=email_id)
            print(data)

            if data!=None:
                if sha256_crypt.verify(password,data[4]):
                    session['logged_in']=True
                    session['email_id']=email_id
                    session['first_name'] = data[1]
                    session['last_name'] = data[2]
                    session['type'] = 'brand'
                    session['company_name'] = data[5]
                    session['user_id']=data[0]
                    print(session['user_id'])
                    flash('You are now logged in', 'success')
                    return redirect(url_for('admin'))
                else:
                    error = 'Invalid login'
                    flash(error,'danger')
            else:
                return render_template('user/login.html')

        elif 'influencer' in request.form:
            email_id = request.form.get('inf_username')
            password = request.form.get('inf_password')
            print(email_id)
            print(password)



@connecsiApp.route('/admin')
@is_logged_in
def admin():
    title='Dashboard'
    return render_template('index.html',title=title)


@connecsiApp.route('/profileView')
@is_logged_in
def profileView():
    title='Profile View'
    type = session['type']
    user_id = session['user_id']
    if type == 'brand':
        table_name = 'users_brands'
    else:
        table_name = 'users_inf'
    connecsiObj = ConnecsiModel()
    data = connecsiObj.get_user_by_user_id(table_name=table_name,user_id=str(user_id))
    print(data)
    return render_template('user/user-profile-page.html',data=data,title=title)

@connecsiApp.route('/searchInfluencers',methods=['POST','GET'])
@is_logged_in
def searchInfluencers():
    connecsiObj = ConnecsiModel()
    region_codes = connecsiObj.get__(table_name='youtube_region_codes', STAR='*')
    video_categories = connecsiObj.get__(table_name='youtube_video_categories', STAR='*')
    lookup_string = ''
    for cat in video_categories:
        lookup_string += ''.join(',' + cat[1])
    lookup_string = lookup_string.replace('&', 'and')
    if request.method=='POST':
        if 'search_inf' in request.form:
            string_word = request.form.get('string_word')
            # print(string_word)
            category = string_word.replace('and','&')
            # print(category)
            category_id=''
            try:
                category_details = connecsiObj.get__(table_name='youtube_video_categories',STAR='*',WHERE='WHERE',compare_column='video_cat_name',compare_value=category)
                category_id = category_details[0][0]
            except:pass
            print(category_id)
            channel = request.form.get('select_channel')
            country = request.form.get('select_country')
            min_lower = request.form.get('min_lower')
            max_upper = request.form.get('max_upper')
            data = connecsiObj.search_inf(channel_id=channel,
                                          min_lower=str(min_lower), max_upper=str(max_upper)
                                          , category_id=str(category_id), country=str(country))
            return render_template('search/search_influencers.html', title='Search Infulencers', data=data,
                                   string_word=string_word, channel=channel, country=country, min_lower=min_lower,
                                   max_upper=max_upper, region_codes=region_codes, lookup_string=lookup_string)
    else:
        connecsiObj = ConnecsiModel()
        data = connecsiObj.get__(table_name='youtube_channel_details',STAR='*')
        # print(data)
        region_codes = connecsiObj.get__(table_name='youtube_region_codes',STAR='*')
        video_categories = connecsiObj.get__(table_name='youtube_video_categories',STAR='*')
        lookup_string = ''
        for cat in video_categories:
            lookup_string+=''.join(','+cat[1])
        lookup_string=lookup_string.replace('&', 'and')
        return render_template('search/search_influencers.html',title='Search Infulencers',data=data,region_codes=region_codes,lookup_string=lookup_string)
















    # @connecsiApp.route('/search', methods=['POST', 'GET'])
    # @is_logged_in
    # def search():
    #     if request.method == 'POST':
    #         if 'search_inf' in request.form:
    #             string_word = request.form.get('string_word')
    #             channel = request.form.get('select_channel')
    #             country = request.form.get('select_country')
    #             min_lower = request.form.get('min_lower')
    #             max_upper = request.form.get('max_upper')
    #             print(string_word)
    #             print(channel)
    #             print(country)
    #             print(min_lower)
    #             print(max_upper)
    #             connecsiObj = ConnecsiModel()
    #             data = connecsiObj.search_inf(table_name='youtube_channel_details', channel_id=channel,
    #                                           min_lower=str(min_lower), max_upper=str(max_upper)
    #                                           , keyword=string_word, country=country)
    #             print('length of data =',len(data))
    #             print(data)
                # region_codes = connecsiObj.get__(table_name='youtube_region_codes', STAR='*')
                # video_categories = connecsiObj.get__(table_name='youtube_video_categories', STAR='*')
                # lookup_string = ''
                # for cat in video_categories:
                #     lookup_string += ''.join(',' + cat[1])
                # lookup_string = lookup_string.replace('&', 'and')
                # return render_template('search/search_influencers.html', title='Search Infulencers', data=data,
                #                        string_word=string_word, channel=channel, country=country, min_lower=min_lower,
                #                        max_upper=max_upper, region_codes=region_codes, lookup_string=lookup_string)
            # print("i m here")
            # return redirect(url_for('searchInfluencers'))


        # @connecsiApp.route('/login/authorized')
# def authorized():
#     resp = linkedin.authorized_response()
#     if resp is None:
#         return 'Access denied: reason=%s error=%s' % (
#             request.args['error_reason'],
#             request.args['error_description']
#         )
#     session['linkedin_token'] = (resp['access_token'], '')

    # me = linkedin.get('people/~')
    # email_linkedin = linkedin.get('people/~:(email-address)')
    # print(jsonify(email_linkedin.data))

    # email_id = email_linkedin.data['emailAddress']
    # data=[me.data['id'],me.data['firstName'],me.data['lastName'],email_id,'',me.data['headline'],'Admin']
    # print(me.data)
    # session['logged_in'] = True
    # session['type'] = 'brand'
    # session['user_id'] = me.data['id']
    # session['first_name']=me.data['firstName']
    # print(data)
    # return render_template('index.html',data=data)

# @linkedin.tokengetter
# def get_linkedin_oauth_token():
#     return session.get('linkedin_token')


# def change_linkedin_query(uri, headers, body):
#     auth = headers.pop('Authorization')
#     headers['x-li-format'] = 'json'
#     if auth:
#         auth = auth.replace('Bearer', '').strip()
#         if '?' in uri:
#             uri += '&oauth2_access_token=' + auth
#         else:
#             uri += '?oauth2_access_token=' + auth
#     return uri, headers, body
#
# linkedin.pre_request = change_linkedin_query

if __name__ == '__main__':
    connecsiApp.secret_key = 'connecsiSecretKey'
    connecsiApp.run(debug=True,host='localhost',port=8080)