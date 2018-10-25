import schedule #pip install schedule
import time
# import sys
# sys.path.append('/cryto_trading/CryptoMasterMindsApi/controller')
from controller.youtube.YoutubeApiController import YoutubeApiController


def get_regionCodes():
    conObj = YoutubeApiController()
    conObj.get_all_regionCodes()

def get_video_cat_ids():
    conObj = YoutubeApiController()
    conObj.get_all_video_categories()

def get_channel_ids():
    conObj = YoutubeApiController()
    conObj.get_all_channel_ids()

def get_channel_details():
    conObj = YoutubeApiController()
    conObj.get_data()

def get_business_email():
    conObj = YoutubeApiController()
    conObj.get_data_by_selinium()

# get_channel_ids()
get_channel_details()
# get_regionCodes()
# get_video_cat_ids()
# get_business_email()

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


