import re
import urllib.parse

import schedule #pip install schedule
import time
import sys
# sys.path.append('/cryto_trading/CryptoMasterMindsApi/controller')
mypath = "/home/Connecsi/backend/ezad"
if mypath not in sys.path:
   sys.path.append(mypath)

from controller.twitter_module.TwitterApiController import TwitterApiController
from model.ConnecsiModel import ConnecsiModel

def get_data():
    conObj = TwitterApiController()
    conObj.get_data()

def get_data_by_screen_name():
    modelObj = ConnecsiModel()
    columns=['channel_id','twitter_url','country','facebook_url','insta_url']
    channel_data=modelObj.get__(table_name='youtube_channel_details',columns=columns)
    data_done = modelObj.get__(table_name='youtube_channel_ids_done_for_twitter', STAR='*')
    # data=(('UC-lHJZR3Gqxm24_Vd_AJ5Yw',),('UCfX-uO8iDdJRgFR2lrBWsYA',))
    # exit()
    channel_ids_done = []
    # total_channel_ids = []
    channel_ids_not_done = []
    for item2 in data_done:
        channel_ids_done.append(item2[0])
    # for item3 in channel_data:
    #     total_channel_ids.append(item3[0])
    for item4 in channel_data:
        if item4[0] not in channel_ids_done:
            channel_ids_not_done.append(item4)
    # print('TOTAL IDS = ', len(total_channel_ids))
    print('DONE = ', len(channel_ids_done))
    print('NOT DONE =', len(channel_ids_not_done))
    # print(total_channel_ids)
    # print(channel_ids_done)
    # print(channel_ids_not_done)
    # exit()
    # ratelimit_counter = 0
    for item in channel_ids_not_done:
        channel_id = item[0]
        country = item[2]
        facebook_url = item[3]
        insta_url= item[4]
        youtube_url = 'https://www.youtube.com/channel/'+channel_id
        if item[1]:
            vc_data=''
            screen_name = ''
            output=''
            try:
                print('twitter url = ',item[1])
                vc_data = modelObj.get_youtube_categories_by_channel_id(channel_id=channel_id)
                print(vc_data)
            except Exception as e:
                print(e)
                pass
            video_categories=[]
            if vc_data:
                try:
                    for vc_item in vc_data:
                        video_categories.append(vc_item[1])
                except Exception as e:
                    print(e)
                    print('VC DATA IS EMPTY')
                    pass
            try:
                twitter_url = item[1]
                # output = re.findall('http(.*)', twitter_url)
            except Exception as e:
                print(e)
                pass
            try:
                parsed = urllib.parse.urlsplit(twitter_url)
                path=parsed.path
                output=path.rsplit('/', 3)
            except Exception as e:
                print(e)
                pass
            try:
                screen_name = output[1]
                print(screen_name)
            except Exception as e:
                print(e)
                pass

            try:
                conObj = TwitterApiController()
                print('GETTING DATA FROM API = ', channel_id)
                conObj.get_data_by_screen_name(channel_id=channel_id,twitter_url=twitter_url,screen_name=screen_name,video_categories=video_categories
                                                   ,country=country,facebook_url=facebook_url,insta_url=insta_url,youtube_url=youtube_url)
            except Exception as e:
                print(e)
                pass

        else:
            try:
                print('DONT HAVE TWITTER URL = ',channel_id)
                # data = [channel_id, 'false']
                # modelObj.insert__(table_name='channels_mapper',columns=['youtube_channel_id','confirmed'],data=data)
                modelObj.insert_into_channels_mapper(youtube_channel_id=channel_id,confirmed='false')
            except Exception as e:
                print(e)
                pass
        print('INSERTING INTO DONE TABLE = ',channel_id)
        try:
            modelObj.insert__(table_name='youtube_channel_ids_done_for_twitter',columns=['channel_id'],IGNORE='IGNORE',data=[channel_id])
        except Exception as e:
            print(e)
            pass


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


