from flask import Flask, request, session
from flask_restplus import Resource, Api, fields, Namespace
from model.ConnecsiModel import ConnecsiModel
from passlib.hash import sha256_crypt
import datetime

ns_user = Namespace('User', description='User')

login_form = ns_user.model('Login', {
    'email' : fields.String(required=True, description='Email'),
    'password' : fields.String(required=True, description='Password')
})

@ns_user.route('/login')
class Login(Resource):
    @ns_user.expect(login_form)
    # @api.param('password')
    # @api.param('username')
    def post(self):
        # languages.append(api.payload)
        '''checks the login details and sets session variables'''
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        # username=flask.request.args.get("username")
        connecsiObj = ConnecsiModel()
        data = connecsiObj.get_user_by_email_id(table_name='users_brands', email_id=email)
        # print(data)
        if data != None:
            if sha256_crypt.verify(password, data[4]):
                # session['logged_in'] = True
                # session['email_id'] = email
                # session['first_name'] = data[1]
                # session['last_name'] = data[2]
                # session['type'] = 'brand'
                # session['company_name'] = data[5]
                # session['user_id'] = data[0]
                # print(session['user_id'])
                return {'user_id': data[0]},200
            else:
                error = 'Invalid login'
                return {'error': error},404
        else:
            return {'error':'No such Username'},404

# @ns_user.route('/logout/<string:user_id>')
# class Logout(Resource):
#     def post(self,user_id):
#         '''clear all session of user_id'''
#         session.clear()
#         return {'Logged out':'Success'},200

