import re
import urllib.parse

import schedule #pip install schedule
import time
# import sys
# sys.path.append('/cryto_trading/CryptoMasterMindsApi/controller')
from controller.twitter.TwitterApiController import TwitterApiController
from model.ConnecsiModel import ConnecsiModel

def get_data():
    conObj = TwitterApiController()
    conObj.get_data()

def get_data_by_screen_name():
    modelObj = ConnecsiModel()
    columns=['channel_id','twitter_url']
    channel_data=modelObj.get__(table_name='youtube_channel_details',columns=columns)
    print(channel_data)
    for item in channel_data:
        if item[1]:
            try:
                screen_name=''
                print(item[1])
                twitter_url = item[1]
                # output = re.findall('http(.*)', twitter_url)
                parsed = urllib.parse.urlsplit(twitter_url)
                path=parsed.path
                output=path.rsplit('/', 3)
                screen_name = output[1]
                conObj = TwitterApiController()
                conObj.get_data_by_screen_name()
            except:pass
            exit()

def get_content_categories():
    conObj = TwitterApiController()
    conObj.get_user_categories()

def search_users():
    conObj = TwitterApiController()
    conObj.search_users()
# search_users()
# get_content_categories()
# get_data()
get_data_by_screen_name()

############change parameter for required periodic tasks###################
#default is 1 minute it can be changed as per requirement
#schedule.every(1).minutes.do(getCoinDetails,'coinmarketcap.com')
# schedule.every().day.at("07:00").do(del_and_update_events)
# schedule.every().day.at("05:00").do(get_fiat_daily_data)
#schedule.every(5).minutes.do(getDailyData_records,'coinmarketcap.com')
#schedule.every(1).minutes.do(getDailyData,'coinmarketcap.com')

#schedule.every().hour.do(periodic_task)
#schedule.every().day.at("10:30").do(getCoinDetails,'coinmarketcap.com')
#schedule.every(5).to(10).minutes.do(periodic_task)
#schedule.every().monday.do(periodic_task)
#schedule.every().wednesday.at("13:15").do(periodic_task)
#schedule.cancel_job(periodic_task())
###########################################################################
# while True:
#
#     schedule.run_pending()
#     time.sleep(1)


