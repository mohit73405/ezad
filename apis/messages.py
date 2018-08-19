from flask import Flask, request, session
from flask_restplus import Resource, Api, fields, Namespace
from model.ConnecsiModel import ConnecsiModel
from passlib.hash import sha256_crypt
import datetime

ns_messages = Namespace('Messages', description='Messages Operations')

message_form = ns_messages.model('Message Details', {
    'first_name' : fields.String(required=True, description='First Name'),
    'last_name' : fields.String(required=True, description='Last Name'),
    'company_name' : fields.String(required=True, description='Company Name'),
    'email' : fields.String(required=True, description='Email'),
    'password' : fields.String(required=True, description='Password')
})
