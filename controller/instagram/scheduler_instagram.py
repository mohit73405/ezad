import re
import urllib.parse

import schedule #pip install schedule
import time
import sys
# sys.path.append('/cryto_trading/CryptoMasterMindsApi/controller')
mypath = "/home/Connecsi/backend/ezad"
if mypath not in sys.path:
   sys.path.append(mypath)

from controller.instagram.instagramCon import InstgramScrapper
from model.ConnecsiModel import ConnecsiModel


def get_data_by_insta_url():
    modelObj = ConnecsiModel()
    columns=['channel_id','insta_url','country','facebook_url','twitter_url']
    channel_data=modelObj.get__(table_name='youtube_channel_details',columns=columns)
    data_done = modelObj.get__(table_name='youtube_channel_ids_done_for_instagram', STAR='*')
    channel_ids_done = []
    channel_ids_not_done = []
    for item2 in data_done:
        channel_ids_done.append(item2[0])
    for item4 in channel_data:
        if item4[0] not in channel_ids_done:
            channel_ids_not_done.append(item4)
    print('DONE = ', len(channel_ids_done))
    print('NOT DONE =', len(channel_ids_not_done))
    # print(channel_ids_not_done)

    for item in channel_ids_not_done:
        channel_id = item[0]
        insta_url = item[1]
        country = item[2]
        facebook_url = item[3]
        twitter_url= item[4]
        youtube_url = 'https://www.youtube.com/channel/'+channel_id
        if insta_url:
            vc_data=''
            try:
                vc_data = modelObj.get_youtube_categories_by_channel_id(channel_id=channel_id)
                # print(vc_data)
            except:pass
            video_categories=[]
            try:
                for vc_item in vc_data:
                    video_categories.append(vc_item[1])
            except:pass

            try:
                conObj = InstgramScrapper(url=insta_url,channel_id=channel_id,twitter_url=twitter_url,video_categories=video_categories
                                                   ,country=country,facebook_url=facebook_url,insta_url=insta_url,youtube_url=youtube_url)
                conObj.set_insta_data()
                print('inserted')
            except Exception as e:
                print('not insterted')
                print(e)
                pass

        else:
            print(channel_id,' is not having insta url')
            try:
                data = [channel_id, 'false']
                # modelObj.insert__(table_name='channels_mapper',columns=['youtube_channel_id','confirmed'],data=data)
                modelObj.insert_youtube_id_into_channels_mapper(youtube_channel_id=channel_id,confirmed='true')
            except:pass
        modelObj.insert__(table_name='youtube_channel_ids_done_for_instagram', columns=['channel_id'], IGNORE='IGNORE',
                          data=[channel_id])

get_data_by_insta_url()

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


