
from controller.twitter_module.TwitterApiController import TwitterApiController
from model.ConnecsiModel import ConnecsiModel

def search_users():
    conObj = TwitterApiController()
    data=conObj.search_only_users(raw_query='pew die pie')


search_users()