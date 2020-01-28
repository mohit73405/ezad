import uuid

import pandas as pd
import pymysql,pymysql.cursors
# import sshtunnel
import time
from sshtunnel import SSHTunnelForwarder
from configparser import ConfigParser
import os

class ConnecsiModel:
    def __init__(self):

        config = ConfigParser()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        config.read(dir_path+'/database_config.ini')
        host = config.get('auth', 'host')
        user = config.get('auth', 'user')
        password = config.get('auth', 'password')
        db = config.get('auth', 'db')
        # self.server = SSHTunnelForwarder(
        #     '46.28.109.89',
        #     ssh_username='kiran',
        #     ssh_password='vD2eV&^bKS(AB92G',
        #     ssh_pkey='C:/Users/Mika/.ssh/id_rsa',
        #     remote_bind_address=('127.0.0.1', 3306)
        # )
        # self.server.start()

        # sshtunnel.SSH_TIMEOUT = 5.0
        # sshtunnel.TUNNEL_TIMEOUT = 5.0
        #
        # with sshtunnel.SSHTunnelForwarder(
        #         ('ssh.pythonanywhere.com'),
        #         ssh_username='your PythonAnywhere username',
        #         ssh_password='the password you use to log in to the PythonAnywhere website',
        #         remote_bind_address=(
        #         'your PythonAnywhere database hostname, eg. yourusername.mysql.pythonanywhere-services.com', 3306)
        # ) as tunnel:
        #     connection = mysql.connector.connect(
        #         user='your PythonAnywhere username', password='your PythonAnywhere database password',
        #         host='127.0.0.1', port=tunnel.local_bind_port,
        #         database='your database name, eg yourusername$mydatabase',
        #     )

        self.cnx = pymysql.connect(
            host=host,
        #     port=self.server.local_bind_port,
            user=user,
            password=password,
            db=db,
            use_unicode=True, charset="utf8"

        )


    def search_youtube_inf(self,offset,sort_order,min_lower='',max_upper='',country='',category_id=''):
        try:

            with self.cnx.cursor() as cursor:
                category_id_join = ''
                if category_id:
                    category_id_join = ' JOIN youtube_channel_ids_video_categories_id t2 on t1.channel_id = t2.channel_id '
                # group_by=" group by t1.channel_id"
                # group_by =''
                category_id_filter = " t2.video_cat_id ="+category_id
                # country_filter = " t3.regionCode = '"+country+"'"
                country_filter = " t1.country = '" + country + "'"
                order='desc'
                if sort_order == 'High To Low':
                    order = 'desc'
                elif sort_order == 'Low To High':
                    order = 'asc'
                else:order='desc'
                order_by = " order by t1.subscriberCount_gained "+order + " LIMIT 20 OFFSET " +offset
                start_time = time.time()
                sql = "SELECT DISTINCT t1.channel_id ,t1.title, t1.channel_img, t1.desc, t1.subscriberCount_gained, " \
                "t1.subscriberCount_lost,t1.business_email, t1.total_100video_views, t1.total_100video_views_unique, " \
                "t1.total_100video_likes,t1.total_100video_dislikes, t1.total_100video_comments,t1.total_100video_shares, " \
                "t1.facebook_url,t1.insta_url,t1.twitter_url,t1.country " \
                "FROM youtube_channel_details t1 "+category_id_join+ \
                "WHERE t1.subscriberCount_gained > 1000 AND  t1.subscriberCount_gained BETWEEN "+min_lower+ " AND " + max_upper
                # "left join youtube_channel_ids_regioncode t3 on t1.channel_id = t3.channel_id " \

                if category_id and country:
                    sql = sql+ ' AND '+ category_id_filter + ' AND '+ country_filter + order_by
                elif category_id:
                    sql = sql+' AND '+category_id_filter + order_by
                elif country:
                    # sql = sql = sql + group_by
                    sql = sql+ ' AND '+country_filter  + order_by
                else: sql = sql + order_by

                # print(sql)

                cursor.execute(sql)
                data = cursor.fetchall()
                end_time = time.time()
                print('seconds took to run this sql ' + sql + ' = ', end_time - start_time)
            print("closing cnx")
            cursor.close()
            self.cnx.close()

            return data

        except Exception as e:
            print('i m here in model')
            print(e)



    def getTop10YoutubeInfluencers(self):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT t1.channel_id,t1.title, t1.channel_img, t1.subscriberCount_gained, " \
                "t1.total_100video_views," \
                "t1.total_100video_likes, t1.total_100video_comments,t1.total_100video_shares, " \
                "t1.facebook_url,t1.insta_url,t1.twitter_url,t1.country,count(t2.channel_id) " \
                "FROM (select * from youtube_channel_details WHERE total_100video_views != 0  ORDER BY subscriberCount_gained DESC LIMIT 10 ) as t1 " \
                "JOIN youtube_channel_ids_video_categories_id t2 on t1.channel_id = t2.channel_id GROUP BY t2.channel_id"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            # self.cnx.close()
            return data

        except Exception as e:
            print(e)

    # def getTop10TwitterInfluencers(self):
    #     try:
    #         with self.cnx.cursor() as cursor:
    #             sql = "SELECT t1.twitter_id,t1.screen_name,t1.title, t1.channel_img, t1.description, t1.no_of_followers, " \
    #             "t1.business_email, t1.no_of_views_recent100, " \
    #             "t1.no_of_likes_recent100, t1.no_of_comments_recent100,t1.no_of_retweets_recent100, " \
    #             "t1.facebook_url,t1.insta_url,t1.youtube_url,t1.twitter_url,t1.location " \
    #             "FROM (select * from twitter_channel_details WHERE total_100video_views != 0  ORDER BY no_of_followers DESC LIMIT 10 ) as t1 " \
    #             # "JOIN youtube_channel_ids_video_categories_id t2 on t1.channel_id = t2.channel_id GROUP BY t2.channel_id"
    #             print(sql)
    #             cursor.execute(sql)
    #             data = cursor.fetchall()
    #             # print(result)
    #         print("closing cnx")
    #         cursor.close()
    #         # self.cnx.close()
    #         return data
    #
    #     except Exception as e:
    #         print(e)

    # def getTop10InstaInfluencers(self):
    #     try:
    #         with self.cnx.cursor() as cursor:
    #             sql = "SELECT t1.channel_id,t1.title, t1.channel_img, t1.subscriberCount_gained, " \
    #             "t1.total_100video_views," \
    #             "t1.total_100video_likes, t1.total_100video_comments,t1.total_100video_shares, " \
    #             "t1.facebook_url,t1.insta_url,t1.twitter_url,t1.country,count(t2.channel_id) " \
    #             "FROM (select * from youtube_channel_details WHERE total_100video_views != 0  ORDER BY subscriberCount_gained DESC LIMIT 10 ) as t1 " \
    #             "JOIN youtube_channel_ids_video_categories_id t2 on t1.channel_id = t2.channel_id GROUP BY t2.channel_id"
    #             print(sql)
    #             cursor.execute(sql)
    #             data = cursor.fetchall()
    #             # print(result)
    #         print("closing cnx")
    #         cursor.close()
    #         # self.cnx.close()
    #         return data
    #
    #     except Exception as e:
    #         print(e)




    def getTotalVideos(self,channel_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT count(channel_id) FROM youtube_channel_ids_video_categories_id WHERE channel_id = '"+channel_id+"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            # self.cnx.close()
            return data

        except Exception as e:
            print(e)

    def search_twitter_inf(self,offset,sort_order,min_lower='',max_upper='',country='',category_id=''):
        try:

            with self.cnx.cursor() as cursor:
                group_by=" group by t1.twitter_id"
                # group_by =''
                category_id_filter = " t2.category_id ="+category_id
                # country_filter = " t3.regionCode = '"+country+"'"
                country_filter = " t1.country = '" + country + "'"
                order='desc'
                if sort_order == 'High To Low':
                    order = 'desc'
                elif sort_order == 'Low To High':
                    order = 'asc'
                else:order='desc'
                order_by = " order by t1.no_of_followers "+order + " LIMIT 20 OFFSET " +offset

                sql = "SELECT t1.twitter_id,t1.screen_name,t1.title, t1.channel_img, t1.description, t1.no_of_followers, " \
                "t1.business_email, t1.no_of_views_recent100, " \
                "t1.no_of_likes_recent100, t1.no_of_comments_recent100,t1.no_of_retweets_recent100, " \
                "t1.facebook_url,t1.insta_url,t1.youtube_url,t1.twitter_url,t1.location " \
                "FROM twitter_channel_details t1 " \
                "JOIN twitter_id_category_id t2 on t1.twitter_id = t2.twitter_id " \
                "WHERE t1.no_of_followers BETWEEN " + min_lower + " AND " + max_upper
                # "JOIN youtube_channel_ids_video_categories_id t2 on t1.channel_id = t2.channel_id " \

                # "left join youtube_channel_ids_regioncode t3 on t1.channel_id = t3.channel_id " \

                if category_id and country:
                    sql = sql+ ' AND '+ category_id_filter + ' AND '+ country_filter + group_by + order_by
                elif category_id:
                    sql = sql+' AND '+category_id_filter + group_by + order_by
                elif country:
                    # sql = sql = sql + group_by
                    sql = sql+ ' AND '+country_filter + group_by + order_by
                else: sql = sql + group_by + order_by

                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            # self.cnx.close()
            return data

        except Exception as e:
            print(e)

    def search_instagram_inf(self, offset, sort_order, min_lower='', max_upper='', country='', category_id=''):
        try:

            with self.cnx.cursor() as cursor:
                # group_by = " group by t3.insta_id"
                # group_by =''
                category_id_filter = " ic.category_id =" + category_id
                # country_filter = " t3.regionCode = '"+country+"'"
                country_filter = " icd.country = '" + country + "'"
                order = 'desc'
                if sort_order == 'High To Low':
                    order = 'desc'
                elif sort_order == 'Low To High':
                    order = 'asc'
                else:
                    order = 'desc'
                # order_by = " order by t1.no_of_followers " + order + " LIMIT 20 OFFSET " + offset

                sql = "SELECT t1.insta_id,t1.username,t1.title, t1.channel_img, t1.description, t1.no_of_followers, " \
                      "t1.business_email, t1.no_of_views_recent100, " \
                      "CAST(SUM(t3.no_of_post_likes) AS SIGNED) total_100video_likes, CAST(SUM(t3.no_of_post_comments) AS SIGNED) total_100video_comments,t1.no_of_shares_recent100, " \
                      "t1.facebook_url,t1.insta_url,t1.youtube_url,t1.twitter_url,t1.country,count(t3.post_id) as total_videos " \
                      "FROM (SELECT icd.insta_id,icd.username,icd.title, icd.channel_img, icd.description, icd.no_of_followers, " \
                      " icd.business_email, icd.no_of_views_recent100, " \
                      " icd.no_of_shares_recent100," \
                      " icd.facebook_url,icd.insta_url,icd.youtube_url,icd.twitter_url,icd.country " \
                      " FROM insta_channel_details icd " \
                      " JOIN insta_id_category_id ic on icd.insta_id = ic.insta_id " \
                      " WHERE (icd.no_of_followers BETWEEN " + min_lower + " AND " + max_upper + ") " \

                join =" group by ic.insta_id) as t1 " \
                      " JOIN insta_post_details t3 on t1.insta_id = t3.insta_id group by t3.insta_id " \
                      " order by t1.no_of_followers " + order + " LIMIT 20 OFFSET " + offset


                if category_id and country:
                    sql = sql + ' AND ' + category_id_filter + ' AND ' + country_filter + join
                elif category_id:
                    sql = sql + ' AND ' + category_id_filter + join
                elif country:
                    # sql = sql = sql + group_by
                    sql = sql + ' AND ' + country_filter + join
                else:
                    sql = sql + join

                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            # self.cnx.close()
            return data
        except Exception as e:
            print(e)


    def search_youtube_inf_get_total_rows(self, sort_order, min_lower='', max_upper='', country='', category_id=''):
        try:
            with self.cnx.cursor() as cursor:
                category_id_join = ''
                if category_id:
                    category_id_join = ' JOIN youtube_channel_ids_video_categories_id t2 on t1.channel_id = t2.channel_id '
                # group_by = " group by t1.channel_id"
                # group_by =''
                category_id_filter = " t2.video_cat_id =" + category_id
                # country_filter = " t3.regionCode = '"+country+"'"
                country_filter = " t1.country = '" + country + "'"
                order = 'desc'
                if sort_order == 'High To Low':
                    order = 'desc'
                elif sort_order == 'Low To High':
                    order = 'asc'
                else:
                    order = 'desc'
                # order_by = " order by t1.subscriberCount_gained " + order
                order_by = ''
                start_time = time.time()
                sql = "SELECT distinct(count(t1.channel_id)) FROM youtube_channel_details t1 "+category_id_join+ \
                      "WHERE t1.subscriberCount_gained > 1000 AND t1.subscriberCount_gained BETWEEN " + min_lower + " AND " + max_upper
                # "left join youtube_channel_ids_regioncode t3 on t1.channel_id = t3.channel_id " \

                if category_id and country:
                    # sql = sql + ' AND ' + category_id_filter + ' AND ' + country_filter + group_by + order_by
                    sql = sql + ' AND ' + category_id_filter + ' AND ' + country_filter  + order_by
                elif category_id:
                    # sql = sql + ' AND ' + category_id_filter + group_by + order_by
                    sql = sql + ' AND ' + category_id_filter + order_by
                elif country:
                    # sql = sql = sql + group_by
                    # sql = sql + ' AND ' + country_filter + group_by + order_by
                    sql = sql + ' AND ' + country_filter + order_by
                else:
                    # sql = sql + group_by + order_by
                    sql = sql + order_by

                # print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                end_time = time.time()
                print('seconds took to run this sql '+sql+ ' = ' ,end_time-start_time)
                # print(result)
            print("closing cnx")
            cursor.close()
            # self.cnx.close()
            return data

        except Exception as e:
            print(e)


    def search_twitter_inf_get_total_rows(self, sort_order, min_lower='', max_upper='', country='', category_id=''):
        try:
            with self.cnx.cursor() as cursor:
                group_by = " group by t1.twitter_id"
                # group_by =''
                category_id_filter = " t2.category_id =" + category_id
                # country_filter = " t3.regionCode = '"+country+"'"
                # country_filter = " location = '" + country + "'"
                country_filter = " t1.country = '" + country + "'"
                order = 'desc'
                if sort_order == 'High To Low':
                    order = 'desc'
                elif sort_order == 'Low To High':
                    order = 'asc'
                else:
                    order = 'desc'
                order_by = " order by t1.no_of_followers " + order


                      # "JOIN youtube_channel_ids_video_categories_id t2 on t1.channel_id = t2.channel_id " \
                sql = "SELECT * FROM twitter_channel_details t1 " \
                      "JOIN twitter_id_category_id t2 on t1.twitter_id = t2.twitter_id " \
                      "WHERE t1.no_of_followers BETWEEN " + min_lower + " AND " + max_upper
                # "left join youtube_channel_ids_regioncode t3 on t1.channel_id = t3.channel_id " \

                if category_id and country:
                    sql = sql + ' AND ' + category_id_filter + ' AND ' + country_filter + group_by + order_by
                elif category_id:
                    sql = sql + ' AND ' + category_id_filter + group_by + order_by
                elif country:
                    # sql = sql = sql + group_by
                    sql = sql + ' AND ' + country_filter + group_by + order_by
                else:
                    sql = sql + group_by + order_by

                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            # self.cnx.close()

            return data

        except Exception as e:
            print(e)


    def search_instagram_inf_get_total_rows(self, sort_order, min_lower='', max_upper='', country='', category_id=''):
        try:
            with self.cnx.cursor() as cursor:
                group_by = " group by t1.insta_id"
                # group_by =''
                category_id_filter = " t2.category_id =" + category_id
                # country_filter = " t3.regionCode = '"+country+"'"
                # country_filter = " location = '" + country + "'"
                country_filter = " t1.country = '" + country + "'"
                order = 'desc'
                if sort_order == 'High To Low':
                    order = 'desc'
                elif sort_order == 'Low To High':
                    order = 'asc'
                else:
                    order = 'desc'
                order_by = " order by t1.no_of_followers " + order


                      # "JOIN youtube_channel_ids_video_categories_id t2 on t1.channel_id = t2.channel_id " \
                sql = "SELECT * FROM insta_channel_details t1 " \
                      "JOIN insta_id_category_id t2 on t1.insta_id = t2.insta_id " \
                      "WHERE t1.no_of_followers BETWEEN " + min_lower + " AND " + max_upper
                # "left join youtube_channel_ids_regioncode t3 on t1.channel_id = t3.channel_id " \

                if category_id and country:
                    sql = sql + ' AND ' + category_id_filter + ' AND ' + country_filter + group_by + order_by
                elif category_id:
                    sql = sql + ' AND ' + category_id_filter + group_by + order_by
                elif country:
                    # sql = sql = sql + group_by
                    sql = sql + ' AND ' + country_filter + group_by + order_by
                else:
                    sql = sql + group_by + order_by

                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            # self.cnx.close()
            return data
        except Exception as e:
            print(e)


    def get__(self,table_name,columns='',STAR='',WHERE='',compare_column='',compare_value=''):

        columns_string=''
        if columns:
            for name in columns:
                #print(name)
                columns_string+=''.join('`'+name+'`'+',')
        columns_string = columns_string[:-1]

        where_string=''
        if WHERE:
            where_string+=''.join(WHERE+' ')
            where_string+=''.join(compare_column+' '+'=')
            where_string+=''.join("'"+compare_value+"'")

        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT "+ STAR + columns_string + " from " + table_name + " "+where_string
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                #print(result)
            print("closing cnx")
            cursor.close()
            return data

        except Exception as e:
            print(e)

    def get_infulencers(self):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT  * from youtube_channel_details ORDER BY subscriberCount_gained DESC"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data

        except Exception as e:
            print(e)


    def get_user_by_email_id(self,email_id,table_name):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT user_id,password,confirmed_email from " + table_name + " WHERE email_id = '" + email_id + "' "
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchone()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data

        except Exception as e:
            print(e)

    def get_user_by_user_id(self,user_id,table_name):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT  * from " + table_name + " WHERE user_id = '" + user_id + "' "
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchone()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data

        except Exception as e:
            print(e)


    def get_password_by_user_id(self,user_id,table_name):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT  password from " + table_name + " WHERE user_id = '" + user_id + "' "
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchone()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data

        except Exception as e:
            print(e)

    def insert__(self,data,table_name,columns,IGNORE=''):
        columns_string = ''
        values_string=''
        if columns:
            for name in columns:
                #print(name)
                columns_string+=''.join('`'+name+'`'+',')
                values_string+=''.join('%s'+',')
        columns_string = columns_string[:-1]
        values_string = values_string[:-1]
        inserted_id = ''
        try:
            with self.cnx.cursor() as cursor:

                sql = "INSERT " +IGNORE+ " INTO `" + table_name + "` ("+columns_string+") VALUES ("+values_string+")"
                print(sql)
                print(data)
                print(len(data))
                cursor.execute("set names utf8mb4")
                if table_name == 'users_brands':
                    cursor.execute(sql, data)
                elif table_name == 'youtube_channel_ids':
                    cursor.executemany(sql,data)
                elif table_name == 'youtube_channel_details':
                    cursor.execute(sql,data)
                elif table_name == 'youtube_region_codes':
                    cursor.executemany(sql,data)
                elif table_name == 'youtube_video_categories':
                    cursor.executemany(sql,data)
                elif table_name == 'youtube_channel_ids_regioncode':
                    cursor.executemany(sql, data)
                elif table_name == 'youtube_channel_ids_video_categories_id':
                    cursor.executemany(sql, data)
                elif table_name == 'users_brands_payments':
                    cursor.execute(sql, data)
                elif table_name == 'brands_campaigns':
                    cursor.execute(sql, data)
                    inserted_id = cursor.lastrowid
                elif table_name == 'messages':
                    cursor.execute(sql, data)
                    inserted_id = cursor.lastrowid
                elif table_name == 'conversations':
                    cursor.execute(sql, data)
                elif table_name == 'brands_inf_fav_list':
                    cursor.execute(sql, data)
                elif table_name == 'brads_inf_fav_list_only':
                    cursor.execute(sql, data)
                elif table_name == 'brands_classifieds':
                    cursor.execute(sql, data)
                elif table_name == 'channel_campaign_message':
                    cursor.execute(sql, data)
                elif table_name == 'message_campaigns':
                    cursor.execute(sql, data)
                elif table_name == 'campaign_proposal':
                    cursor.execute(sql, data)
                    inserted_id = cursor.lastrowid
                elif table_name == 'user_channel_message_files':
                    cursor.execute(sql, data)
                elif table_name == 'user_channel_message_agreements':
                    cursor.execute(sql, data)
                elif table_name == 'brand_campaign_report':
                    cursor.execute(sql, data)
                elif table_name == 'twitter_channel_details':
                    cursor.execute(sql, data)
                elif table_name == 'channels_mapper':
                    cursor.execute(sql, data)
                elif table_name == 'users_influencers':
                    cursor.execute(sql, data)
                elif table_name == 'inf_offers':
                    cursor.execute(sql, data)
                elif table_name == 'inf_campaign_report':
                    cursor.execute(sql, data)
                elif table_name == 'twitter_id_category_id':
                    cursor.execute(sql, data)
                elif table_name == 'insta_channel_details':
                    cursor.execute(sql, data)
                elif table_name == 'insta_id_category_id':
                    cursor.execute(sql, data)
                elif table_name == 'insta_post_details':
                    cursor.execute(sql, data)
                elif table_name == 'youtube_channels_history':
                    cursor.execute(sql, data)
                elif table_name == 'youtube_channel_ids_done':
                    cursor.execute(sql, data)
                elif table_name == 'youtube_channel_ids_done_for_twitter':
                    cursor.execute(sql, data)
                elif table_name == 'twitter_channels_history':
                    cursor.execute(sql, data)
                elif table_name == 'youtube_channel_ids_done_for_instagram':
                    cursor.execute(sql, data)
                elif table_name == 'insta_channels_history':
                    cursor.execute(sql, data)
                elif table_name == 'users_brands_payments':
                    cursor.execute(sql, data)
                elif table_name == 'notifications':
                    cursor.execute(sql, data)
                    inserted_id = cursor.lastrowid
                elif table_name == 'classified_comment_views_reaction':
                    cursor.execute(sql, data)
                elif table_name == 'offer_comment_views_reaction':
                    cursor.execute(sql, data)
                elif table_name == 'campaign_status_notification':
                    cursor.execute(sql, data)
                elif table_name == 'influencer_alert_milestone':
                    cursor.execute(sql, data)

                self.cnx.commit()
            print("closing cnx")

            cursor.close()

            res=1
        except Exception as e:
            res=0
            print(e)
            print("Exception Occured")
        if inserted_id:
           return inserted_id
        else:
            return res


    def update__(self,table_name,columns,data,WHERE,compare_column,compare_value):
        columns_string=''
        for column in columns:
            columns_string += ''.join(column+'=%s,')
        # print(columns_string)
        columns_string = columns_string[:-1]
        # print(columns_string)
        # exit()
        sql = 'UPDATE ' + table_name + ' SET ' + columns_string +' '+ WHERE +' '+ compare_column + ' = ' + str(compare_value)
        print(sql)
        try:
            with self.cnx.cursor() as cursor:
                cursor.execute(sql, data)
                self.cnx.commit()
                cursor.close()
        except Exception as e: print(e)


    def get_messages_by_email_id_and_user_type(self,email_id,user_type):
        try:
            with self.cnx.cursor() as cursor:
                table_name = 'messages'
                sql = "SELECT  * from " + table_name + " WHERE to_email_id = '" + email_id + "' OR from_email_id = '" + email_id + "' AND user_type = '"+ user_type + "' GROUP BY message_id DESC"
                # sql = "SELECT m.message_id, m.from_email_id, m.to_email_id, m.date,m.subject,m.message  from messages m left join conversations c on m.message_id = c.message_id"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data

        except Exception as e:
            print(e)



    def get_conversations_by_message_id(self,message_id):
        try:
            with self.cnx.cursor() as cursor:
                table_name = 'conversations'
                sql = "SELECT  * from " + table_name + " WHERE message_id = '" + message_id  + "' GROUP BY conv_id ASC"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data

        except Exception as e:
            print(e)

    def get_conversations_by_to_email_id(self,to_email_id):
        try:
            with self.cnx.cursor() as cursor:
                table_name = 'conversations'
                sql = "SELECT  * from " + table_name + " WHERE conv_to_email_id = '" + to_email_id  + "' ORDER BY conv_id DESC"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data

        except Exception as e:
            print(e)

    def get_all_unread_messages_by_to_email_id(self,to_email_id):
        try:
            with self.cnx.cursor() as cursor:
                total_unread_messages = 0
                table_name1 = 'messages'
                sql1 = "SELECT  count(*) from " + table_name1 + " WHERE `read` = 'false' AND " \
                      " to_email_id = '" + to_email_id  + "'"
                print(sql1)
                cursor.execute(sql1)
                data1 = cursor.fetchone()
                for item1 in data1:
                    total_unread_messages = total_unread_messages+item1
                print('data1 = ',data1)
                table_name2 = 'conversations'
                sql2 = "SELECT  count(*) from " + table_name2 + " WHERE `read` = 'false' AND " \
                                                        " conv_to_email_id = '" + to_email_id + "'"
                print(sql2)
                cursor.execute(sql2)
                data2 = cursor.fetchone()
                for item2 in data2:
                    total_unread_messages = total_unread_messages+item2
                print('data2= ',data2)
                # print(result)
                result = {'total_unread_messages':total_unread_messages}

            print("closing cnx")
            cursor.close()
            return result

        except Exception as e:
            print(e)

    def get_conversations_by_from_email_id(self,from_email_id):
        try:
            with self.cnx.cursor() as cursor:
                table_name = 'conversations'
                sql = "SELECT  * from " + table_name + " WHERE conv_from_email_id = '" + from_email_id  + "' ORDER BY conv_id DESC"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data

        except Exception as e:
            print(e)

    def get_messages_by_from_email_id(self,from_email_id):
        try:
            with self.cnx.cursor() as cursor:
                table_name = 'messages'
                sql = "SELECT  * from " + table_name + " WHERE from_email_id = '" + from_email_id  + "' ORDER BY message_id DESC"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data

        except Exception as e:
            print(e)




    def get_conversations_by_user_type(self,user_type):
        try:
            with self.cnx.cursor() as cursor:
                table_name = 'conversations'
                # sql = "SELECT  * from " + table_name + " WHERE user_type = '"+ str(user_type) + "'"
                sql = "SELECT  * from " + table_name
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)


    def get_campaign_details_by_campaign_id_and_user_id(self,campaign_id,user_id):
        try:
            with self.cnx.cursor() as cursor:
                table_name = 'brands_campaigns'
                sql = "SELECT  * from brands_campaigns" \
                      "  WHERE campaign_id = '" + campaign_id  + "' AND user_id = '" + user_id+"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data

        except Exception as e:
            print(e)

    def get_brand_classified_details_by_classified_id_and_user_id(self,classified_id,user_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT  * from brands_classifieds" \
                      "  WHERE classified_id = '" + classified_id +"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data

        except Exception as e:
            print(e)


    def get_inf_offer_details_by_offer_id_and_user_id(self,offer_id,user_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT " \
                      " io.offer_id,io.channel_id,io.offer_name, io.from_date,io.to_date,io.budget,io.currency," \
                      " io.channels,io.regions,io.min_lower_followers,io.max_upper_followers,io.files,io.video_cat_id," \
                      " io.offer_description,io.arrangements,io.kpis,io.no_of_views,io.no_of_replies,io.deleted,io.posted_date " \
                      " FROM inf_offers io" \
                      " WHERE io.offer_id='" +offer_id+ "'"
                     # " LEFT JOIN channels_mapper chm on io.channel_id = chm.youtube_channel_id " \
                     # (chm.youtube_channel_id = '" + user_id + "' OR chm.twitter_channel_id = '" + user_id + "')" \
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data

        except Exception as e:
            print(e)


    def get_all_offers_for_brands(self,channel_name,category_id,country,arrangements,min_lower,max_upper,currency,price_lower,price_upper):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT " \
                      " io.offer_id,io.channel_id,io.offer_name, io.from_date,io.to_date,io.budget,io.currency," \
                      " io.channels,io.regions,io.min_lower_followers,io.max_upper_followers,io.files,io.video_cat_id," \
                      " io.offer_description,io.arrangements,io.kpis,io.no_of_views,io.no_of_replies,io.deleted,io.posted_date," \
                      " ui.first_name,ui.last_name,ui.business_email,yvc.video_cat_name" \
                      " FROM inf_offers io" \
                      " JOIN users_influencers ui on ui.channel_id = io.channel_id " \
                      " JOIN youtube_video_categories yvc on yvc.video_cat_id = io.video_cat_id "
                conditions = []
                if channel_name:
                    conditions.append(" io.channels LIKE '%"+channel_name +"%'")
                if category_id:
                    conditions.append(" io.video_cat_id LIKE '"+category_id+"'")
                if country:
                    conditions.append(" io.country LIKE '%" + country + "%'")
                if arrangements:
                    conditions.append(" io.arrangements LIKE '%"+arrangements+"%'")
                if min_lower and max_upper:
                    conditions.append(" io.min_lower_followers >= " +min_lower+ " AND io.max_upper_followers <= " + max_upper )
                if currency:
                    conditions.append(" io.currency LIKE '%"+currency+"%'")
                if price_lower and price_upper:
                    conditions.append(" io.budget BETWEEN " +price_lower+ " AND " + price_upper )
                conditions.append(" io.deleted != 'true' OR io.deleted is NULL ")
                if conditions:
                    sql += " WHERE "
                    sql += " AND ".join(conditions)

                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data

        except Exception as e:
            print(e)


    def get_all_classifieds_for_influencers(self,channel_name,category_id,country,arrangements,min_lower,max_upper,currency,price_lower,price_upper):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT " \
                      " bc.classified_id,bc.user_id,bc.classified_name, bc.from_date,bc.to_date,bc.budget,bc.currency," \
                      " bc.channels,bc.regions,bc.min_lower_followers,bc.max_upper_followers,bc.files,bc.video_cat_id,bc.target_url," \
                      " bc.classified_description,bc.arrangements,bc.kpis,bc.no_of_views,bc.no_of_replies,bc.deleted,bc.posted_date," \
                      " ub.first_name,ub.last_name,ub.profile_pic,ub.email_id,yvc.video_cat_name" \
                      " FROM brands_classifieds bc" \
                      " JOIN users_brands ub on ub.user_id = bc.user_id " \
                      " JOIN youtube_video_categories yvc on yvc.video_cat_id = bc.video_cat_id "
                conditions = []
                if channel_name:
                    conditions.append(" bc.channels LIKE '%"+channel_name +"%'")
                if category_id:
                    conditions.append(" bc.video_cat_id LIKE '"+category_id+"'")
                if country:
                    conditions.append(" bc.country LIKE '%" + country + "%'")
                if arrangements:
                    conditions.append(" bc.arrangements LIKE '%"+arrangements+"%'")
                if min_lower and max_upper:
                    conditions.append(" bc.min_lower_followers >= " +min_lower+ " AND bc.max_upper_followers <= " + max_upper )
                if currency:
                    conditions.append(" bc.currency LIKE '%"+currency+"%'")
                if price_lower and price_upper:
                    conditions.append(" bc.budget BETWEEN " +price_lower+ " AND " + price_upper )
                conditions.append(" bc.deleted != 'true' OR bc.deleted is NULL ")
                if conditions:
                    sql += " WHERE "
                    sql += " AND ".join(conditions)

                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data

        except Exception as e:
            print(e)




    def get_all_classifieds_for_inf(self):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT " \
                      " io1.classified_id,io1.user_id,io1.classified_name, io1.from_date,io1.to_date,io1.budget,io1.currency," \
                      " io1.channels,io1.regions,io1.min_lower_followers,io1.max_upper_followers,io1.files,io1.video_cat_id," \
                      " io1.classified_description,io1.arrangements,io1.kpis,io1.no_of_views,io1.no_of_replies" \
                      " from brands_classifieds io1"

                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data

        except Exception as e:
            print(e)


    def delete_message_from_conversation(self, message_id,conv_id, user_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "UPDATE conversations SET deleted = 'true', deleted_from_user_id = CONCAT(IFNULL(deleted_from_user_id,''), ',' ,'"+ user_id +") WHERE message_id = '" + message_id + "' AND conv_id = '" + conv_id + "'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def delete_message_from_messages(self, message_id, user_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "UPDATE messages SET deleted = 'true', deleted_from_user_id = CONCAT(IFNULL(deleted_from_user_id,''), ',' ,'"+ user_id +") WHERE message_id = '" + message_id + "'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def get_fav_inf_list(self, user_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT bi.channel_id,bi.alert_followers,bi.alert_views,bi.alert_likes,bi.alert_comments,bi.channel_name " \
                      " FROM brands_inf_fav_list bi " \
                      " WHERE bi.user_id = '"+user_id +"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)

    def get_fav_inf_list_only(self, user_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT bi.channel_id,bi.channel_name " \
                      " FROM brads_inf_fav_list_only bi " \
                      " WHERE bi.user_id = '"+user_id +"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)

    def get_fav_inf_list_by_channel_name(self, user_id,channel_name):
        try:
            with self.cnx.cursor() as cursor:
                sql=''
                if channel_name == 'youtube':
                    sql = "SELECT bi.channel_id," \
                          "t1.title, t1.channel_img, t1.desc, t1.subscriberCount_gained, " \
                          "t1.subscriberCount_lost,t1.business_email, t1.total_100video_views, t1.total_100video_views_unique, " \
                          "t1.total_100video_likes,t1.total_100video_dislikes, t1.total_100video_comments,t1.total_100video_shares, " \
                          "t1.facebook_url,t1.insta_url,t1.twitter_url,t1.country,bi.alert_followers,bi.alert_views,bi.alert_likes,bi.alert_comments,bi.channel_name " \
                          " FROM brands_inf_fav_list bi " \
                          " LEFT JOIN youtube_channel_details t1 ON bi.channel_id = t1.channel_id " \
                          " WHERE bi.user_id = '"+user_id +"' AND bi.channel_name ='"+channel_name+"'"
                if channel_name == 'twitter':
                    sql = "SELECT bi.channel_id," \
                          "t1.screen_name, t1.title, t1.channel_img, t1.description, t1.no_of_followers," \
                          "t1.business_email, t1.no_of_views_recent100, " \
                          "t1.no_of_likes_recent100, t1.no_of_comments_recent100, t1.no_of_retweets_recent100, " \
                          "t1.facebook_url, t1.insta_url, t1.youtube_url, t1.twitter_url, t1.location,bi.alert_followers,bi.alert_views,bi.alert_likes,bi.alert_comments,bi.channel_name " \
                          " FROM brands_inf_fav_list bi " \
                          " LEFT JOIN twitter_channel_details t1 ON bi.channel_id = t1.twitter_id " \
                          " WHERE bi.user_id = '" + user_id + "' AND bi.channel_name ='" + channel_name + "'"
                if channel_name == 'instagram':
                    sql = "SELECT bi.channel_id," \
                          "t1.username,t1.title, t1.channel_img, t1.description, t1.no_of_followers, " \
                          "t1.business_email, t1.no_of_views_recent100, " \
                          "CAST(SUM(t3.no_of_post_likes) AS SIGNED) total_100video_likes, CAST(SUM(t3.no_of_post_comments) AS SIGNED) total_100video_comments,t1.no_of_shares_recent100, " \
                          "t1.facebook_url,t1.insta_url,t1.youtube_url,t1.twitter_url,t1.country, " \
                          "bi.alert_followers,bi.alert_views,bi.alert_likes,bi.alert_comments,bi.channel_name " \
                          " FROM brands_inf_fav_list bi " \
                          " JOIN insta_channel_details t1 ON bi.channel_id = t1.insta_id " \
                          " JOIN insta_post_details t3 ON t1.insta_id = t3.insta_id " \
                          " WHERE bi.user_id = '" + user_id + "' AND bi.channel_name ='" + channel_name + "'" \
                          " GROUP BY t3.insta_id"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)

    def get_fav_inf_list_by_channel_name_new(self, user_id,channel_name):
        try:
            with self.cnx.cursor() as cursor:
                sql=''
                if channel_name == 'youtube':
                    sql = "SELECT bi.channel_id," \
                          "t1.title, t1.channel_img, t1.desc, t1.subscriberCount_gained, " \
                          "t1.subscriberCount_lost,t1.business_email, t1.total_100video_views, t1.total_100video_views_unique, " \
                          "t1.total_100video_likes,t1.total_100video_dislikes, t1.total_100video_comments,t1.total_100video_shares, " \
                          "t1.facebook_url,t1.insta_url,t1.twitter_url,t1.country,bi.channel_id,bi.channel_name " \
                          " FROM brads_inf_fav_list_only bi " \
                          " LEFT JOIN youtube_channel_details t1 ON bi.channel_id = t1.channel_id " \
                          " WHERE bi.user_id = '"+user_id +"' AND bi.channel_name ='"+channel_name+"'"
                if channel_name == 'twitter':
                    sql = "SELECT bi.channel_id," \
                          "t1.screen_name, t1.title, t1.channel_img, t1.description, t1.no_of_followers," \
                          "t1.business_email, t1.no_of_views_recent100, " \
                          "t1.no_of_likes_recent100, t1.no_of_comments_recent100, t1.no_of_retweets_recent100, " \
                          "t1.facebook_url, t1.insta_url, t1.youtube_url, t1.twitter_url, t1.location,bi.channel_id,bi.channel_name " \
                          " FROM brads_inf_fav_list_only bi " \
                          " LEFT JOIN twitter_channel_details t1 ON bi.channel_id = t1.twitter_id " \
                          " WHERE bi.user_id = '" + user_id + "' AND bi.channel_name ='" + channel_name + "'"
                if channel_name == 'instagram':
                    sql = "SELECT bi.channel_id," \
                          "t1.username,t1.title, t1.channel_img, t1.description, t1.no_of_followers, " \
                          "t1.business_email, t1.no_of_views_recent100, " \
                          "CAST(SUM(t3.no_of_post_likes) AS SIGNED) total_100video_likes, CAST(SUM(t3.no_of_post_comments) AS SIGNED) total_100video_comments,t1.no_of_shares_recent100, " \
                          "t1.facebook_url,t1.insta_url,t1.youtube_url,t1.twitter_url,t1.country, " \
                          " bi.channel_id,bi.channel_name " \
                          " FROM brads_inf_fav_list_only bi " \
                          " JOIN insta_channel_details t1 ON bi.channel_id = t1.insta_id " \
                          " JOIN insta_post_details t3 ON t1.insta_id = t3.insta_id " \
                          " WHERE bi.user_id = '" + user_id + "' AND bi.channel_name ='" + channel_name + "'" \
                          " GROUP BY t3.insta_id"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)


    def create_alert_for_fav_influencer(self, user_id,channel_id,alert_followers,alert_views,alert_likes,alert_comments,channel_name):

        columns = ['user_id', 'channel_id', 'alert_followers', 'alert_views', 'alert_likes', 'alert_comments','channel_name']
        data = (user_id, channel_id, alert_followers, alert_views, alert_likes, alert_comments,channel_name)

        fav_inf_list = self.get_fav_inf_list(user_id=user_id)
        present = 0
        for item in fav_inf_list:
            print(item[0])
            if item[0] == channel_id:
                present = 1
                break
        print(present)
        # exit()
        if present == 0:
            try:
                connecsiObj = ConnecsiModel()
                connecsiObj.insert__(table_name='brands_inf_fav_list',columns=columns,data=data)
                return {"response": 1}, 200
            except Exception as e:
                return {"response": e}, 500

        else:
            try:
                with self.cnx.cursor() as cursor:
                    sql = "UPDATE brands_inf_fav_list SET alert_followers = " + alert_followers + " , " \
                          "alert_views = " + alert_views + ", alert_likes = " + alert_likes + \
                          ", alert_comments = " + alert_comments + " WHERE user_id = " + user_id +" AND channel_id = '" + channel_id + "'"
                    print(sql)
                    cursor.execute(sql)
                    self.cnx.commit()
                    # print(result)
                    print("closing cnx")
                    cursor.close()
                    return 1
            except Exception as e:
                print(e)
                return 0


    def update_youtube_channel_data(self, channel_id,country):
        try:
            with self.cnx.cursor() as cursor:
                sql = "UPDATE youtube_channel_details SET country = '"+ country +"' WHERE channel_id = '"+ channel_id + "'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def update_youtube_email(self, channel_id,business_email):
        try:
            with self.cnx.cursor() as cursor:
                sql = "UPDATE youtube_channel_details SET business_email = '"+ business_email +"' WHERE channel_id = '"+ channel_id + "'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def update_messages_to_email_id(self, message_id,to_email_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "UPDATE messages SET to_email_id = '"+ to_email_id +"' WHERE message_id = '"+ message_id + "'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def get_youtube_inf_list(self, campaign_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT ccm.channel_id,ycd.title,ycd.channel_img,ycd.business_email," \
                      " cp.ref_link,cp.proposal_channels,cp.proposal_price,ccm.channel_name,cp.proposal_id   FROM channel_campaign_message ccm" \
                      " JOIN youtube_channel_details ycd on ccm.channel_id = ycd.channel_id" \
                      " LEFT JOIN campaign_proposal cp on cp.campaign_id = ccm.campaign_id and cp.channel_id=ccm.channel_id " \
                      " WHERE ccm.campaign_id = '"+ campaign_id +"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)

    def get_channel_campaign_message_status(self, channel_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT ccm.campaign_id,bc.campaign_name,ccm.message_id,ccm.status FROM channel_campaign_message ccm" \
                      " JOIN youtube_channel_details ycd on ccm.channel_id = ycd.channel_id" \
                      " JOIN brands_campaigns bc on ccm.campaign_id = bc.campaign_id" \
                      " WHERE ccm.channel_id = '"+ channel_id +"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)

    def get_channel_campaign_message_status_by_channel_and_campaign_id(self, channel_id,campaign_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT ccm.campaign_id,bc.campaign_name,ccm.message_id,ccm.status FROM channel_campaign_message ccm" \
                      " JOIN youtube_channel_details ycd on ccm.channel_id = ycd.channel_id" \
                      " JOIN brands_campaigns bc on ccm.campaign_id = bc.campaign_id" \
                      " WHERE ccm.channel_id = '"+ channel_id +"'" + " AND ccm.campaign_id = "+ campaign_id
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)



    def get_channel_campaign_message_status_by_campaign_id(self, campaign_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT ccm.campaign_id,bc.campaign_name,ccm.message_id,ccm.status,ccm.channel_id,bc.user_id FROM channel_campaign_message ccm" \
                      " JOIN brands_campaigns bc on ccm.campaign_id = bc.campaign_id" \
                      " WHERE ccm.campaign_id = '"+ campaign_id +"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)

    def get_campaigns_added_to_message(self, message_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT * FROM brands_campaigns bc" \
                      " Left JOIN channel_campaign_message ccm on bc.campaign_id = ccm.campaign_id" \
                      " WHERE ccm.message_id = '"+ message_id +"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)


    def get_campaigns_added_to_message_by_channel_id(self, channel_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT * FROM brands_campaigns bc" \
                      " Left JOIN channel_campaign_message ccm on bc.campaign_id = ccm.campaign_id" \
                      " WHERE ccm.channel_id = '"+ channel_id +"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)

    def get_campaigns_added_to_message_by_message_id_and_channel_id(self, message_id,channel_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT * FROM brands_campaigns bc" \
                      " Left JOIN channel_campaign_message ccm on bc.campaign_id = ccm.campaign_id" \
                      " WHERE ccm.message_id = '"+ message_id +"' AND ccm.channel_id = '"+channel_id+"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)


    def update_channel_campaign_message(self, channel_id,message_id,status,campaign_id=''):
        try:
            with self.cnx.cursor() as cursor:
                print('channel id =',channel_id,type(channel_id))
                print('message id =', message_id,type(message_id))
                print('status = ',status,type(status))
                select_sql=''
                update_sql=''
                insert_sql=''
                # if campaign_id:
                select_sql = "SELECT 1 FROM channel_campaign_message WHERE channel_id ='"+channel_id+"'" \
                             " AND campaign_id ='"+campaign_id+"'"

                update_sql = "UPDATE channel_campaign_message SET message_id = " + str(message_id) + ", " \
                             "status = '" + status + "' WHERE channel_id = '" + str(channel_id) \
                             + "' AND status !='Proposal Sent' AND status !='Current Partner' AND campaign_id = '" + campaign_id + "'"

                insert_sql = "INSERT INTO channel_campaign_message(channel_id,campaign_id,message_id,status)" \
                             " VALUES('" + channel_id + "'," + campaign_id + "," + message_id + ",'" + status + "')"

                # else:
                #     select_sql = "SELECT 1 FROM channel_campaign_message WHERE channel_id ='" + channel_id + "'" \
                #                  " AND message_id ='" + message_id + "'"
                #
                #     update_sql = "UPDATE channel_campaign_message SET message_id = " + str(message_id) + ", " \
                #                  "status = '" + status + "' WHERE channel_id = '" + str(channel_id) \
                #              + "' AND status !='Proposal Sent' AND status !='Current Partner' AND campaign_id = '" + campaign_id + "'"
                #
                #     insert_sql = "INSERT INTO channel_campaign_message(channel_id,campaign_id,message_id,status)" \
                #                  " VALUES('" + channel_id + "'," + campaign_id + "," + message_id + ",'" + status + "')"



                # print(sql)
                res = cursor.execute(select_sql)
                print(res)
                if res == 1:
                   cursor.execute(update_sql)
                else:
                    cursor.execute(insert_sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0


    def update_channel_campaign_message_for_negotiations(self, channel_id,message_id,status,campaign_id):
        try:
            with self.cnx.cursor() as cursor:
                print('channel id =',channel_id,type(channel_id))
                print('message id =', message_id,type(message_id))
                print('status = ',status,type(status))
                print('campaign_id = ', campaign_id, type(campaign_id))
                sql = "UPDATE channel_campaign_message SET status = '"+ status +"' WHERE channel_id = '" + str(channel_id)\
                      + "' AND status !='Proposal Sent' AND status !='Current Partner' AND message_id = '"+message_id+"' " \
                       " AND campaign_id = '"+campaign_id+"'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0


    def update_channel_status_by_campaign_id(self, channel_id,message_id,status,campaign_id):
        try:
            with self.cnx.cursor() as cursor:
                print('channel id =',channel_id,type(channel_id))
                print('message id =', message_id,type(message_id))
                print('status = ',status,type(status))
                sql = "UPDATE channel_campaign_message SET status = '"+ str(status) +"' WHERE channel_id = '" + str(channel_id) +"' " \
                      " AND message_id = '"+str(message_id)+"' " \
                      " AND campaign_id = '"+str(campaign_id)+"'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def update_channel_campaign_message_status_by_message_id_campaign_id(self,message_id,status,campaign_id):
        try:
            with self.cnx.cursor() as cursor:
                print('message id =', message_id,type(message_id))
                print('status = ',status,type(status))
                sql = "UPDATE channel_campaign_message SET status = '"+ str(status) +"' WHERE message_id = '" + str(message_id) +"' " \
                      " AND campaign_id = '"+str(campaign_id)+"'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0


    def update_campaign_status(self,campaign_id,campaign_status):
        try:
            with self.cnx.cursor() as cursor:
                sql = "UPDATE brands_campaigns SET campaign_status = '"+ str(campaign_status) +"' WHERE campaign_id = '" + str(campaign_id) +"' "
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def get_all_proposal(self, user_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT " \
                      " cp.proposal_id,cp.campaign_id, bc.campaign_name, cp.message_id, cp.user_id, " \
                      " ub.company_name,ub.email_id," \
                      " ycd.channel_id,ycd.title,ycd.business_email," \
                      " cp.influencer_id, cp.proposal_description,cp.proposal_from_date,cp.proposal_to_date," \
                      " cp.proposal_channels,cp.proposal_arrangements,cp.proposal_kpis,cp.currency,cp.proposal_price,cp.target_url,cp.ref_link" \
                      " FROM campaign_proposal cp" \
                      " JOIN users_brands ub on cp.user_id = ub.user_id" \
                      " JOIN youtube_channel_details ycd on ycd.channel_id = cp.channel_id" \
                      " JOIN brands_campaigns bc on bc.campaign_id = cp.campaign_id" \
                      " WHERE cp.user_id = '"+ user_id +"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)

    def get_inf_details_by_email_id(self, email_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT ui.first_name, ui.last_name, ui.business_email,ui.channel_id,ycd.channel_img" \
                      " FROM users_influencers ui JOIN youtube_channel_details ycd ON ui.channel_id = ycd.channel_id" \
                      " WHERE ui.business_email = '"+email_id+"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)

    def get_proposal(self, proposal_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT " \
                      " cp.proposal_id,cp.campaign_id, bc.campaign_name, cp.message_id, cp.user_id, " \
                      " ub.company_name,ub.email_id," \
                      " ycd.channel_id,ycd.title,ycd.business_email," \
                      " cp.influencer_id, cp.proposal_description,cp.proposal_from_date,cp.proposal_to_date," \
                      " cp.proposal_channels,cp.proposal_arrangements,cp.proposal_kpis,cp.currency,cp.proposal_price,cp.target_url,cp.ref_link" \
                      " FROM campaign_proposal cp" \
                      " JOIN users_brands ub on cp.user_id = ub.user_id" \
                      " JOIN youtube_channel_details ycd on ycd.channel_id = cp.channel_id" \
                      " JOIN brands_campaigns bc on bc.campaign_id = cp.campaign_id" \
                      " WHERE cp.proposal_id = '"+ proposal_id +"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)

    def get_proposal_by_message_id_and_campaign_id(self, message_id,campaign_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT " \
                      " cp.proposal_id,cp.campaign_id, bc.campaign_name, cp.message_id, cp.user_id, " \
                      " ub.company_name,ub.email_id," \
                      " ycd.channel_id,ycd.title,ycd.business_email," \
                      " cp.influencer_id, cp.proposal_description,cp.proposal_from_date,cp.proposal_to_date," \
                      " cp.proposal_channels,cp.proposal_arrangements,cp.proposal_kpis,cp.currency,cp.proposal_price,cp.target_url,cp.ref_link" \
                      " FROM campaign_proposal cp" \
                      " JOIN users_brands ub on cp.user_id = ub.user_id" \
                      " JOIN youtube_channel_details ycd on ycd.channel_id = cp.channel_id" \
                      " JOIN brands_campaigns bc on bc.campaign_id = cp.campaign_id" \
                      " WHERE cp.message_id = '"+ message_id +"' AND cp.campaign_id = '"+campaign_id+"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)

    def update_classified_no_of_views(self,classified_id,user_id,no_of_views):
        try:
            with self.cnx.cursor() as cursor:

                sql = "UPDATE brands_classifieds SET no_of_views = '" + str(no_of_views) + "' WHERE classified_id = '"\
                      + str(classified_id) + "' AND user_id = '" + str(user_id) + "'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def update_offer_no_of_views(self,offer_id,user_id,no_of_views):
        try:
            with self.cnx.cursor() as cursor:

                sql = "UPDATE inf_offers SET no_of_views = '" + str(no_of_views) + "' WHERE offer_id = '"\
                      + str(offer_id) + "'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0



    def update_classified_no_of_replies(self,classified_id,user_id,no_of_replies):
        try:
            with self.cnx.cursor() as cursor:

                sql = "UPDATE brands_classifieds SET no_of_replies = '" + str(no_of_replies) + "' WHERE classified_id = '"\
                      + str(classified_id) + "' AND user_id = '" + str(user_id) + "'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def update_offer_no_of_replies(self, offer_id, user_id, no_of_replies):
        try:
            with self.cnx.cursor() as cursor:

                sql = "UPDATE inf_offers SET no_of_replies = '" + str(
                    no_of_replies) + "' WHERE offer_id = '" \
                      + str(offer_id) + "'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def confirm_brands_email(self,email_id,confirmed):
        try:
            with self.cnx.cursor() as cursor:

                sql = "UPDATE users_brands SET confirmed_email = '" + str(confirmed) + "' WHERE email_id = '"+ str(email_id) +"'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def get_brand_campaign_report(self, user_id,campaign_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT brand_campaign_report_id, user_id, campaign_id, revenue_generated,currency,new_users,channel_id,channel " \
                      " from brand_campaign_report WHERE user_id  = '"+ str(user_id) +"' AND campaign_id = '"+ str(campaign_id) +"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)

    def get_brand_campaign_report_by_channel_id(self, user_id,campaign_id,channel_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT brand_campaign_report_id, user_id, campaign_id, revenue_generated,currency,new_users,channel_id,channel " \
                      " from brand_campaign_report WHERE user_id  = '"+ str(user_id) +"' AND campaign_id = '"+ str(campaign_id) +"' AND channel_id = '"+ str(channel_id) +"' "
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)


    def update_brand_campaign_report(self,campaign_id,channel_id,data):
        try:
            with self.cnx.cursor() as cursor:
                sql = "UPDATE brand_campaign_report SET revenue_generated = %s, currency = %s," \
                      " new_users = %s WHERE campaign_id = '"+ str(campaign_id) + "'" +" AND channel_id = '"+ str(channel_id) +"'"
                print(sql)
                cursor.execute(sql,data)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0



    def getAllInfluencerCampaigns(self, channel_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT " \
                      " cp.campaign_id,bc.campaign_name,bc.campaign_status,bc.user_id,ub.first_name,ub.last_name,bc.regions,ub.profile_pic," \
                      " cp.proposal_id,cp.proposal_from_date, cp.proposal_to_date,cp.currency," \
                      " cp.proposal_price," \
                      " cp.proposal_channels," \
                      " ccm.status " \
                      " FROM campaign_proposal cp " \
                      " JOIN channel_campaign_message ccm on ccm.campaign_id=cp.campaign_id " \
                      " JOIN brands_campaigns bc on bc.campaign_id = cp.campaign_id " \
                      " JOIN users_brands ub on ub.user_id = bc.user_id " \
                      " WHERE ccm.status = 'Current Partner' AND cp.channel_id = '"+channel_id+"'" \
                      " GROUP BY cp.proposal_id "

                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)






    def getInfluencerCampaignDetails(self, channel_id,proposal_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT " \
                      " cp.campaign_id,bc.campaign_name,bc.campaign_status,bc.user_id,ub.first_name,ub.last_name," \
                      " bc.regions,ub.profile_pic,ub.email_id," \
                      " cp.proposal_id,cp.proposal_from_date, cp.proposal_to_date," \
                      " cp.currency,cp.proposal_price," \
                      " cp.proposal_description,cp.proposal_arrangements,cp.proposal_kpis,cp.target_url,cp.ref_link," \
                      " bc.files,bc.regions,bc.video_cat_id,yvc.video_cat_name," \
                      " chm.youtube_channel_id,chm.twitter_channel_id,chm.insta_channel_id,cp.proposal_channels," \
                      " chm.confirmed, ccm.status " \
                      " FROM channels_mapper chm" \
                      " JOIN campaign_proposal cp on cp.channel_id = chm.youtube_channel_id or cp.channel_id=chm.twitter_channel_id" \
                      " JOIN channel_campaign_message ccm on ccm.campaign_id=cp.campaign_id " \
                      " JOIN brands_campaigns bc on bc.campaign_id=cp.campaign_id " \
                      " JOIN users_brands ub on ub.user_id = bc.user_id " \
                      " JOIN youtube_video_categories yvc on yvc.video_cat_id = bc.video_cat_id" \
                      " WHERE ccm.status = 'Current Partner ' AND cp.proposal_id = '" + proposal_id + "'"

                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)





    def get_all_inf_channels(self, user_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT " \
                      " ui1.first_name as youtube_first_name,ui1.last_name as youtube_last_name,ui1.business_email as youtube_business_email," \
                      " ui1.phone as youtube_phone,ui1.categories as youtube_categories, ui1.website as youtube_website, ui1.country as youtube_country," \
                      " ui1.city as youtube_city,ui1.channel_id as youtube_channel_id," \
                      " ui2.first_name as twitter_first_name,ui2.last_name as twitter_last_name,ui2.business_email as twitter_business_email," \
                      " ui2.phone as twitter_phone,ui2.categories as twitter_categories, ui2.website as twitter_website, ui2.country as twitter_country," \
                      " ui2.city as twitter_city,ui2.channel_id as twitter_channel_id," \
                      " chm.youtube_channel_id as mapped_youtube_channel_id,chm.twitter_channel_id as mapped_twitter_channel_id," \
                      " chm.confirmed" \
                      " FROM channels_mapper chm" \
                      " LEFT JOIN users_influencers ui1 on ui1.channel_id = chm.youtube_channel_id" \
                      " LEFT JOIN users_influencers ui2 on ui2.channel_id = chm.twitter_channel_id" \
                      " WHERE ui1.channel_id = '" + user_id + "' OR ui2.channel_id = '"+ user_id +"'"


                # sql = " select ui1.first_name as youtube_first_name,ui2.first_name as twitter_first_name,chm.youtube_channel_id," \
                #       " chm.twitter_channel_id " \
                #       " FROM channels_mapper chm " \
                #       " LEFT JOIN users_influencers ui1 on ui1.channel_id = chm.youtube_channel_id " \
                #       " LEFT JOIN users_influencers ui2 on ui2.channel_id = chm.twitter_channel_id " \
                #       " WHERE ui1.channel_id = '"+ user_id +"' or ui2.channel_id = '"+ user_id +"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)


    def get_inf_and_channel_details(self, user_id):
        try:
            with self.cnx.cursor() as cursor:
                # sql = "SELECT " \
                #       " ui.first_name ,ui.last_name ,ui.business_email," \
                #       " ui.phone ,ui.categories , ui.website , ui.country ," \
                #       " ui.city ,ui.channel_id," \
                #       " chm.youtube_channel_id as mapped_youtube_channel_id,chm.twitter_channel_id as mapped_twitter_channel_id,chm.insta_channel_id as mapped_insta_channel_id," \
                #       " chm.confirmed," \
                #       " ycd.title, ycd.channel_img,ycd.country,ycd.facebook_url,ycd.twitter_url,ycd.insta_url," \
                #       " tcd.business_email,tcd.screen_name,tcd.title,tcd.channel_img,tcd.hashtags, icd.username as insta_username," \
                #       " GROUP_CONCAT(yvc.video_cat_name SEPARATOR ','),GROUP_CONCAT(yvc.video_cat_id SEPARATOR ',')" \
                #       " FROM youtube_channel_details ycd" \
                #       " left join users_influencers ui on ycd.channel_id = ui.channel_id" \
                #       " join youtube_channel_ids_video_categories_id ycivci on ycivci.channel_id = ycd.channel_id" \
                #       " join youtube_video_categories yvc on yvc.video_cat_id = ycivci.video_cat_id" \
                #       " left join channels_mapper chm on chm.youtube_channel_id = ycd.channel_id" \
                #       " left join twitter_channel_details tcd on tcd.twitter_id = chm.twitter_channel_id" \
                #       " JOIN insta_channel_details icd on icd.insta_id = chm.insta_channel_id " \
                #       " WHERE ycd.channel_id = '"+user_id+"'"

                sql = "SELECT " \
                      " ui.first_name ,ui.last_name ,ui.business_email," \
                      " ui.phone ,ui.categories , ui.website , ui.country ," \
                      " ui.city ,ui.channel_id," \
                      " chm.youtube_channel_id as mapped_youtube_channel_id,chm.twitter_channel_id as mapped_twitter_channel_id,chm.insta_channel_id as mapped_insta_channel_id," \
                      " chm.confirmed," \
                      " ycd.title, ycd.channel_img,ycd.country,ycd.facebook_url,ycd.twitter_url,ycd.insta_url," \
                      " tcd.business_email,tcd.screen_name,tcd.title,tcd.channel_img,tcd.hashtags, icd.username as insta_username,ui.default_currency " \
                      " FROM  channels_mapper chm " \
                      " LEFT JOIN users_influencers ui ON ui.channel_id = chm.youtube_channel_id " \
                      " LEFT JOIN insta_channel_details icd ON icd.insta_id = chm.insta_channel_id " \
                      " LEFT JOIN twitter_channel_details tcd ON tcd.twitter_id = chm.twitter_channel_id" \
                      " LEFT JOIN youtube_channel_details ycd ON chm.youtube_channel_id = ycd.channel_id " \
                      " WHERE ui.channel_id = '"+user_id+"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)

    def get_youtube_cetegories_id_and_name(self, user_id):
        try:
            with self.cnx.cursor() as cursor:

                sql = "SELECT " \
                      " GROUP_CONCAT(yvc.video_cat_name SEPARATOR ','),GROUP_CONCAT(ycivci.video_cat_id SEPARATOR ',')" \
                      " FROM  youtube_channel_ids_video_categories_id ycivci " \
                      " JOIN youtube_video_categories yvc ON yvc.video_cat_id = ycivci.video_cat_id " \
                      " WHERE ycivci.channel_id = '"+user_id+"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)


    def get_all_offers(self, channel_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT " \
                      " io.offer_id,io.channel_id,io.offer_name, io.from_date,io.to_date,io.budget,io.currency," \
                      " io.channels,io.regions,io.min_lower_followers,io.max_upper_followers,io.files,io.video_cat_id," \
                      " io.offer_description,io.arrangements,io.kpis,io.no_of_views,io.no_of_replies,io.deleted,io.posted_date " \
                      " FROM inf_offers io " \
                      " WHERE io.channel_id = '" + channel_id + "'"
                    # " LEFT JOIN channels_mapper chm on io.channel_id = chm.youtube_channel_id " \
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)

    def post_as_classified(self, campaign_id, user_id):
        try:
            with self.cnx.cursor() as cursor:

                sql = " UPDATE brands_campaigns SET is_classified_post = 'True' WHERE campaign_id = '" + str(campaign_id) + "'" \
                      " AND user_id = '"+ str(user_id) +"'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0


    def convert_to_campaign(self, classified_id, user_id):
        try:
            with self.cnx.cursor() as cursor:

                sql = " UPDATE brands_classifieds SET convert_to_campaign = 'True' WHERE classified_id = '" + str(classified_id) + "'" \
                      " AND user_id = '"+ str(user_id) +"'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0



    def get_inf_campaign_report(self, campaign_id,proposal_id,channel_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT icr.inf_campaign_report_id, icr.campaign_id, icr.proposal_id," \
                      " icr.channel_id, icr.channel_name,icr.date_posted, icr.link_posted,icr.content_type," \
                      " icr.post_views, icr.post_likes, icr.post_dislikes, icr.post_comments, icr.post_retweets," \
                      " icr.post_remarks,icr.post_clicks,icr.post_shares,ycd.subscriberCount_gained,tcd.no_of_followers," \
                      " icd.no_of_followers " \
                      " from inf_campaign_report icr" \
                      " LEFT JOIN youtube_channel_details ycd on ycd.channel_id = icr.channel_id " \
                      " LEFT JOIN twitter_channel_details tcd on tcd.twitter_id = icr.channel_id " \
                      " LEFT JOIN insta_channel_details icd on icd.insta_id = icr.channel_id " \
                      " WHERE icr.channel_id = '" + channel_id + "'" \
                      " AND icr.campaign_id = '" + campaign_id + "'" \
                      " AND icr.proposal_id = '" + proposal_id + "'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)


    def delete_inf_campaign_report(self, inf_campaign_report_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "Delete from  inf_campaign_report  WHERE inf_campaign_report_id = '"+ inf_campaign_report_id + "'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def delete_brand_campaign_report(self, campaign_id,channel_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "Delete from  brand_campaign_report  WHERE campaign_id = '"+ campaign_id + "' AND channel_id = '"+channel_id+"'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0


    def delete_fav_inf(self, channel_id,user_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "Delete from  brands_inf_fav_list  WHERE channel_id = '" + channel_id + "'" + " AND user_id = '" + user_id + "'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def delete_fav_inf_only(self, channel_id,user_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "Delete from  brads_inf_fav_list_only  WHERE channel_id = '" + channel_id + "'" + " AND user_id = '" + user_id + "'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0


    def delete_campaign(self, campaign_id, user_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "UPDATE brands_campaigns SET deleted = 'true' WHERE campaign_id = '" + campaign_id + "' AND user_id = '" + user_id + "'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0



    def delete_classified(self, classified_id, user_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "UPDATE brands_classifieds SET deleted = 'true' WHERE classified_id = '" + classified_id + "' AND user_id = '" + user_id + "'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0


    def delete_offer(self, offer_id, user_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "UPDATE inf_offers SET deleted = 'true' WHERE offer_id = '" + offer_id + "' AND channel_id = '" + user_id + "'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def update_inf_details(self, channel_id, data):
        try:
            with self.cnx.cursor() as cursor:
                sql = "UPDATE users_influencers SET first_name = %s, last_name = %s, phone = %s, categories=%s, website=%s,country=%s," \
                      " city = %s WHERE channel_id = '" + str(channel_id) + "'"
                print(sql)
                cursor.execute(sql, data)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def update_youtube_inf_country(self, channel_id, country):
        try:
            with self.cnx.cursor() as cursor:
                sql = "UPDATE youtube_channel_details SET country = '"+country+"' WHERE channel_id = '" + str(channel_id) + "'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def update_twitter_inf_country(self, twitter_id, country):
        try:
            with self.cnx.cursor() as cursor:
                sql = "UPDATE twitter_channel_details SET country = '"+country+"', location='"+country+"' WHERE twitter_id = '" + str(twitter_id) + "'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0


    def update_insta_inf_country(self, insta_id, country):
        try:
            with self.cnx.cursor() as cursor:
                sql = "UPDATE insta_channel_details SET country = '"+country+"' WHERE insta_id = '" + str(insta_id) + "'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def get_youtube_categories_by_channel_id(self, channel_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT vc.channel_id,vc.video_cat_id from youtube_channel_ids_video_categories_id vc " \
                      "WHERE vc.channel_id = '"+channel_id+"' GROUP BY vc.video_cat_id"

                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)

    def get_youtube_video_categories_id_and_name_by_channel_id(self, channel_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT vc.channel_id,vc.video_cat_id,yvc.video_cat_name,count(vc.video_cat_id) as category_count from youtube_channel_ids_video_categories_id vc JOIN youtube_video_categories yvc on vc.video_cat_id = yvc.video_cat_id " \
                      " WHERE vc.channel_id = '"+channel_id+"' group by vc.video_cat_id"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)



    def update_users_brands_password(self, email_id,password):
        try:
            with self.cnx.cursor() as cursor:
                sql = "UPDATE users_brands SET password = '"+ password +"' WHERE email_id = '"+ email_id + "'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def insert_categories_to_youtube_channel(self, channel_id, video_cat_id):
        try:
            with self.cnx.cursor() as cursor:
                video_id = lowercase_str = uuid.uuid4().hex
                sql = "INSERT INTO youtube_channel_ids_video_categories_id(channel_id, video_cat_id,video_id) SELECT * FROM " \
                      "(SELECT '"+channel_id+"', '"+video_cat_id+"', '"+video_id+"') AS tmp WHERE NOT EXISTS(SELECT channel_id,video_cat_id FROM youtube_channel_ids_video_categories_id" \
                      " WHERE channel_id = '"+channel_id+"' AND video_cat_id = '"+video_cat_id+"') LIMIT 1;"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0


    def delete_category_from_youtube_channel(self, channel_id,video_cat_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "Delete from  youtube_channel_ids_video_categories_id  WHERE channel_id = '" + channel_id + "'" + " AND video_cat_id = '" + video_cat_id + "'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0




    def insert_categories_to_twitter_channel(self, twitter_id, category_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "INSERT INTO twitter_id_category_id(twitter_id, category_id) SELECT * FROM " \
                      "(SELECT '"+twitter_id+"', '"+category_id+"') AS tmp WHERE NOT EXISTS(SELECT twitter_id,category_id FROM twitter_id_category_id" \
                      " WHERE twitter_id = '"+twitter_id+"' AND category_id = '"+category_id+"') LIMIT 1;"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0


    def insert_categories_to_insta_channel(self, insta_id, category_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "INSERT INTO insta_id_category_id(insta_id, category_id) SELECT * FROM " \
                      "(SELECT '"+insta_id+"', '"+category_id+"') AS tmp WHERE NOT EXISTS(SELECT insta_id,category_id FROM insta_id_category_id" \
                      " WHERE insta_id = '"+insta_id+"' AND category_id = '"+category_id+"') LIMIT 1;"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def insert_into_channels_mapper(self,youtube_channel_id='',twitter_channel_id='',confirmed=''):
        try:
            with self.cnx.cursor() as cursor:
                sql = " INSERT INTO channels_mapper(youtube_channel_id, twitter_channel_id,confirmed) SELECT * FROM " \
                      "(SELECT '"+youtube_channel_id+"', '"+twitter_channel_id+"', '"+confirmed+"') AS tmp " \
                      " WHERE NOT EXISTS(SELECT youtube_channel_id,twitter_channel_id,confirmed FROM channels_mapper" \
                      " WHERE youtube_channel_id = '"+youtube_channel_id+"' AND twitter_channel_id = '"+twitter_channel_id+"' " \
                      " AND confirmed = '"+confirmed+"') LIMIT 1;"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def insert_insta_id_into_channels_mapper(self,youtube_channel_id='',insta_channel_id='',confirmed=''):
        try:
            with self.cnx.cursor() as cursor:
                sql = " INSERT INTO channels_mapper(youtube_channel_id, insta_channel_id,confirmed) SELECT * FROM " \
                      "(SELECT '"+youtube_channel_id+"', '"+insta_channel_id+"', '"+confirmed+"') AS tmp " \
                      " WHERE NOT EXISTS(SELECT youtube_channel_id,insta_channel_id,confirmed FROM channels_mapper" \
                      " WHERE youtube_channel_id = '"+youtube_channel_id+"' AND insta_channel_id = '"+insta_channel_id+"' " \
                      " AND confirmed = '"+confirmed+"') LIMIT 1;"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def insert_youtube_id_into_channels_mapper(self,youtube_channel_id='',confirmed=''):
        try:
            with self.cnx.cursor() as cursor:
                sql = " INSERT INTO channels_mapper(youtube_channel_id,confirmed) SELECT * FROM " \
                      "(SELECT '"+youtube_channel_id+"', '"+confirmed+"') AS tmp " \
                      " WHERE NOT EXISTS(SELECT youtube_channel_id,confirmed FROM channels_mapper" \
                      " WHERE youtube_channel_id = '"+youtube_channel_id+"'" \
                      " AND confirmed = '"+confirmed+"') LIMIT 1;"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def delete_category_from_twitter_channel(self, twitter_id,category_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "Delete from  twitter_id_category_id  WHERE twitter_id = '" + twitter_id + "'" + " AND category_id = '" + category_id + "'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def delete_category_from_insta_channel(self, insta_id,category_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "Delete from  insta_id_category_id  WHERE insta_id = '" + insta_id + "'" + " AND category_id = '" + category_id + "'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def insert_update_youtube_details(self, data):
        try:
            with self.cnx.cursor() as cursor:
                # print(data)
                sql = 'INSERT INTO youtube_channel_details (channel_id, title, channel_img, ' \
                      '`desc`, subscriberCount_gained, subscriberCount_lost,' \
                      'business_email,total_100video_views, total_100video_views_unique, ' \
                      'total_100video_likes,total_100video_dislikes, total_100video_comments,' \
                      'total_100video_shares, facebook_url, insta_url, twitter_url, country)' \
                      ' VALUES("{d[0]}","{d[1]}","{d[2]}","{d[3]}",{d[4]},{d[5]},"{d[6]}",{d[7]},{d[8]},{d[9]},{d[10]},{d[11]},{d[12]},"{d[13]}","{d[14]}","{d[15]}","{d[16]}")' \
                      " ON DUPLICATE KEY UPDATE " \
                      " title = VALUES(title), channel_img=VALUES(channel_img),`desc`=VALUES(`desc`),subscriberCount_gained=COALESCE(VALUES(subscriberCount_gained),subscriberCount_gained)," \
                      "subscriberCount_lost=VALUES(subscriberCount_lost),business_email=COALESCE(business_email,VALUES(business_email)),total_100video_views=VALUES(total_100video_views),total_100video_views_unique=VALUES(total_100video_views_unique)," \
                      " total_100video_likes=VALUES(total_100video_likes),total_100video_dislikes=VALUES(total_100video_dislikes), total_100video_comments=VALUES(total_100video_comments)," \
                      "total_100video_shares=VALUES(total_100video_shares), facebook_url=COALESCE(facebook_url,VALUES(facebook_url)),insta_url=COALESCE(insta_url,VALUES(insta_url)),twitter_url=COALESCE(twitter_url,VALUES(twitter_url)),country=COALESCE(country,VALUES(country))".format(d=data)
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0


    def insert_update_twitter_details(self, data):
        try:
            with self.cnx.cursor() as cursor:
                # print(data)
                # 'twitter_id', 'screen_name', 'title', 'description', 'location', 'no_of_followers', 'no_of_likes_recent100',
                # 'no_of_retweets_recent100', 'website', 'twitter_url', 'hashtags', 'facebook_url', 'insta_url', 'youtube_url', \
                # 'country', 'channel_img', 'business_email'
                sql = 'INSERT INTO twitter_channel_details (twitter_id, screen_name, title, ' \
                      '`description`, location, no_of_followers,' \
                      'no_of_likes_recent100,no_of_retweets_recent100, website, ' \
                      'twitter_url,hashtags, facebook_url,' \
                      'insta_url, youtube_url, country, channel_img, business_email)' \
                      ' VALUES("{d[0]}","{d[1]}","{d[2]}","{d[3]}","{d[4]}",{d[5]},{d[6]},{d[7]},"{d[8]}","{d[9]}","{d[10]}","{d[11]}"' \
                      ' ,"{d[12]}","{d[13]}","{d[14]}","{d[15]}","{d[16]}")' \
                      " ON DUPLICATE KEY UPDATE " \
                      " screen_name = VALUES(screen_name), title=VALUES(title),`description`=VALUES(`description`)," \
                      " location=VALUES(location)," \
                      " no_of_followers=VALUES(no_of_followers),no_of_likes_recent100=VALUES(no_of_likes_recent100)," \
                      " no_of_retweets_recent100=VALUES(no_of_retweets_recent100)," \
                      " website=VALUES(website)," \
                      " twitter_url=VALUES(twitter_url)," \
                      " hashtags=VALUES(hashtags), " \
                      " facebook_url=VALUES(facebook_url)," \
                      " insta_url=VALUES(insta_url)," \
                      " youtube_url=VALUES(youtube_url),country=VALUES(country),channel_img=VALUES(channel_img)," \
                      " business_email=VALUES(business_email)".format(d=data)
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0



    def insert_update_insta_details(self, data):
        try:
            with self.cnx.cursor() as cursor:
                # columns = ['youtube_url', 'twitter_url', 'insta_url', 'facebook_url', 'country',
                #            'insta_id', 'username', 'title', 'business_category_name', 'channel_img', 'description',
                #            'no_of_followers']
                sql = 'INSERT INTO insta_channel_details ( youtube_url, twitter_url, insta_url, ' \
                      '`facebook_url`, country,business_email, insta_id,' \
                      'username,title, business_category_name, ' \
                      'channel_img,description, no_of_followers )' \
                      ' VALUES("{d[0]}","{d[1]}","{d[2]}","{d[3]}","{d[4]}","{d[5]}",{d[6]},"{d[7]}","{d[8]}","{d[9]}","{d[10]}",' \
                      ' "{d[11]}",{d[12]})' \
                      " ON DUPLICATE KEY UPDATE " \
                      " youtube_url = COALESCE( NULLIF(youtube_url, ''), values(youtube_url) ), twitter_url=COALESCE( NULLIF(twitter_url, ''), values(twitter_url) ),`insta_url`=VALUES(`insta_url`)," \
                      " facebook_url=COALESCE( NULLIF(facebook_url, ''), values(facebook_url) )," \
                      " country=COALESCE( NULLIF(country, ''), values(country) ),business_email=VALUES(business_email),username=VALUES(username)," \
                      " title=VALUES(title)," \
                      " business_category_name=VALUES(business_category_name)," \
                      " channel_img=VALUES(channel_img)," \
                      " description=VALUES(description), " \
                      " no_of_followers=VALUES(no_of_followers)".format(d=data)
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def insert_update_insta_post_details(self, data):
        try:
            with self.cnx.cursor() as cursor:
                # columns = ['insta_id', 'post_id', 'post_time', 'insta_hashtags', 'no_of_post_likes',
                #            'no_of_post_comments']
                sql = 'INSERT INTO insta_post_details ( insta_id, post_id, post_time, ' \
                      ' insta_hashtags, no_of_post_likes, no_of_post_comments ) ' \
                      ' VALUES("{d[0]}","{d[1]}","{d[2]}","{d[3]}",{d[4]},{d[5]})' \
                      " ON DUPLICATE KEY UPDATE " \
                      " insta_hashtags = VALUES(insta_hashtags), no_of_post_likes=VALUES(no_of_post_likes)," \
                      " no_of_post_comments=VALUES(no_of_post_comments)".format(d=data)
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0







    def insert_update_youtube_ids_video_cat_ids(self, data):
        try:
            with self.cnx.cursor() as cursor:
                # print(data)
                sql = "INSERT INTO youtube_channel_ids_video_categories_id (channel_id, video_id, video_cat_id) " \
                      " VALUES(%s,%s,%s)" \
                      " ON DUPLICATE KEY UPDATE " \
                      " channel_id = VALUES(channel_id), video_cat_id=VALUES(video_cat_id)"
                print(sql)
                cursor.executemany(sql,data)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def insert_update_youtube_video_details(self, data):
        try:
            with self.cnx.cursor() as cursor:
                # print(data)
                sql = " INSERT INTO youtube_video_details (video_id,channel_id,publishedAt,title,thumbnail," \
                      " tags,category_id, description,viewCount,likeCount,dislikeCount,favoriteCount,commentCount) " \
                      " VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" \
                      " ON DUPLICATE KEY UPDATE " \
                      " title = COALESCE(VALUES(title),title)," \
                      " thumbnail = COALESCE(VALUES(thumbnail),thumbnail)," \
                      " tags = COALESCE(VALUES(tags),tags)," \
                      " category_id = COALESCE(VALUES(category_id),category_id)," \
                      " description = COALESCE(VALUES(description),description)," \
                      " viewCount=COALESCE(VALUES(viewCount),viewCount)," \
                      " likeCount=COALESCE(VALUES(likeCount),likeCount)," \
                      " dislikeCount=COALESCE(VALUES(dislikeCount),dislikeCount)," \
                      " favoriteCount=COALESCE(VALUES(favoriteCount),favoriteCount)," \
                      " commentCount=COALESCE(VALUES(commentCount),commentCount)"
                print(sql)
                cursor.executemany(sql,data)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def insert_youtube_video_stats_data(self, data):
        try:
            with self.cnx.cursor() as cursor:
                # print(data)
                sql = " INSERT INTO youtube_video_statistics (video_id," \
                      " viewCount,likeCount,dislikeCount,favoriteCount,commentCount,channel_id) " \
                      " VALUES(%s,%s,%s,%s,%s,%s,%s)"
                print(sql)
                cursor.executemany(sql,data)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0


    def get_messages_by_to_email_id(self,to_email_id):
        try:
            with self.cnx.cursor() as cursor:
                table_name = 'messages'
                sql = "SELECT  message_id,user_id,channel_id,from_email_id,to_email_id,date,subject,message from " + table_name + " WHERE to_email_id = '" + to_email_id +"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data

        except Exception as e:
            print(e)



    def get_messages_by_message_id(self,message_id):
        try:
            with self.cnx.cursor() as cursor:
                table_name = 'messages'
                sql = "SELECT  message_id,from_email_id,to_email_id,subject,message from " + table_name + " WHERE message_id = '" + message_id +"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchone()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data

        except Exception as e:
            print(e)


    def update_insta_url_in_youtube_channel_details(self,insta_url,youtube_channel_id):
        try:
            with self.cnx.cursor() as cursor:

                sql = "UPDATE youtube_channel_details SET insta_url = '" + str(insta_url) + "' WHERE channel_id = '" \
                      + str(youtube_channel_id) + "'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def update_twitter_url_in_youtube_channel_details(self, twitter_url, youtube_channel_id):
        try:
            with self.cnx.cursor() as cursor:

                sql = "UPDATE youtube_channel_details SET twitter_url = '" + str(twitter_url) + "' WHERE channel_id = '" \
                      + str(youtube_channel_id) + "'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def mark_message_as_read(self, message_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "UPDATE messages SET `read` = 'true' WHERE message_id = '" + message_id + "'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def mark_conversation_as_read(self, conv_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "UPDATE conversations SET `read` = 'true' WHERE conv_id = '" + conv_id + "'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def mark_message_as_unread(self, message_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "UPDATE messages SET `read` = 'false' WHERE message_id = '" + message_id + "'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0


    def get_influencer_list(self):
        try:
            with self.cnx.cursor() as cursor:
                table_name = 'users_influencers'
                sql = "SELECT channel_id,first_name,last_name,business_email FROM " + table_name + " ORDER BY inserted_date DESC "
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data

        except Exception as e:
            print(e)


    def get_users_brands_google_analytics_credentials(self, user_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT ub_ga.user_id, ub_ga.access_token, ub_ga.refresh_token,ub_ga.expires_in,ub_ga.scope,ub_ga.token_type" \
                      " FROM users_brands_google_analytics_credentials ub_ga " \
                      " WHERE ub_ga.user_id = '"+user_id+"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)

    def insert_update_users_brands_google_analytics_credentials(self, data):
        try:
            with self.cnx.cursor() as cursor:
                # print(data)
                sql = "INSERT INTO users_brands_google_analytics_credentials (user_id, access_token, refresh_token, expires_in,scope,token_type) " \
                      " VALUES(%s,%s,%s,%s,%s,%s)" \
                      " ON DUPLICATE KEY UPDATE " \
                      " access_token = VALUES(access_token), refresh_token=VALUES(refresh_token),expires_in=VALUES(expires_in),scope=VALUES(scope),token_type=VALUES(token_type) "
                print(sql)
                cursor.execute(sql,data)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def get_users_influencers_youtube_analytics_credentials(self, user_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT ui_ya.channel_id, ui_ya.access_token, ui_ya.refresh_token,ui_ya.expires_in,ui_ya.scope,ui_ya.token_type" \
                      " FROM users_influencers_youtube_analytics_credentials ui_ya " \
                      " WHERE ui_ya.channel_id = '"+user_id+"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)

    def insert_update_users_influencers_youtube_analytics_credentials(self, data):
        try:
            with self.cnx.cursor() as cursor:
                # print(data)
                sql = "INSERT INTO users_influencers_youtube_analytics_credentials (channel_id, access_token, refresh_token, expires_in,scope,token_type) " \
                      " VALUES(%s,%s,%s,%s,%s,%s)" \
                      " ON DUPLICATE KEY UPDATE " \
                      " access_token = VALUES(access_token), refresh_token=VALUES(refresh_token),expires_in=VALUES(expires_in),scope=VALUES(scope),token_type=VALUES(token_type) "
                print(sql)
                cursor.execute(sql,data)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0


    def insert_update_users_influencers_twitter_analytics_credentials(self, data):
        try:
            with self.cnx.cursor() as cursor:
                # print(data)
                sql = "INSERT INTO users_influencers_twitter_analytics_credentials (twitter_id, access_token, access_token_secret, screen_name) " \
                      " VALUES(%s,%s,%s,%s)" \
                      " ON DUPLICATE KEY UPDATE " \
                      " access_token = VALUES(access_token), access_token_secret=VALUES(access_token_secret) "
                print(sql)
                cursor.execute(sql,data)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def get_users_influencers_twitter_analytics_credentials(self, twitter_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT ui_ta.twitter_id, ui_ta.access_token, ui_ta.access_token_secret,ui_ta.screen_name " \
                      " FROM users_influencers_twitter_analytics_credentials ui_ta " \
                      " WHERE ui_ta.twitter_id = '"+twitter_id+"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)


    def get_twitter_channel_details_by_screen_name(self, screen_name):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT t1.twitter_id,t1.screen_name,t1.title, t1.channel_img, t1.description, t1.no_of_followers, " \
                      "t1.business_email, t1.no_of_views_recent100, " \
                      "t1.no_of_likes_recent100, t1.no_of_comments_recent100,t1.no_of_retweets_recent100, " \
                      "t1.facebook_url,t1.insta_url,t1.youtube_url,t1.twitter_url,t1.location,t1.hashtags " \
                      "FROM twitter_channel_details t1 " \
                      "WHERE t1.screen_name = '" + screen_name + "'"
                      # "JOIN twitter_id_category_id t2 on t1.twitter_id = t2.twitter_id " \

                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)


    def insert_update_users_brands_subscription_package_details(self, data):
        try:
            with self.cnx.cursor() as cursor:
                # print(data)
                sql = "INSERT INTO subscriptions_package_for_brands (user_id, package_name, p_created_date, p_expiry_date,base_package) " \
                      " VALUES(%s,%s,%s,%s,%s)" \
                      " ON DUPLICATE KEY UPDATE " \
                      " package_name = VALUES(package_name), p_created_date=VALUES(p_created_date),p_expiry_date=VALUES(p_expiry_date),base_package = VALUES(base_package) "
                print(sql)
                cursor.execute(sql,data)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0



    def get_users_brands_subscription_package_with_feature_details(self, user_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT t1.user_id,t1.package_name,t1.p_created_date,t1.p_expiry_date,t2.feature_name,t2.units,t2.price,t2.customized_feature,t1.base_package,t2.added_units,t2.base_units " \
                      " FROM subscriptions_package_for_brands t1 LEFT JOIN subscriptions_for_brands t2 on t1.user_id = t2.user_id " \
                      " WHERE t1.user_id = '"+user_id+"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)
            return 0

    def get_subscription_feature_autofill_proposal_details(self, user_id,proposal_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT t1.user_id,t1.proposal_id,t1.auto_or_manual" \
                      " FROM subscription_feature_autofill_proposal t1" \
                      " WHERE t1.user_id = '"+user_id+"' AND t1.proposal_id = '"+proposal_id+"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)
            return 0


    def insert_update_subscription_feature_details(self, data):
        try:
            with self.cnx.cursor() as cursor:
                print(data)
                data_tuple = tuple(data)
                print(type(data_tuple))

                select_sql = "SELECT 1 from subscriptions_for_brands where user_id ='"+data[0]+"' and feature_name = '"+data[1]+"'"
                update_sql = "UPDATE subscriptions_for_brands SET units='"+data[2]+"' ,price= '"+data[3]+"' , customized_feature='"+data[4]+"'" \
                             ",added_units='"+data[5]+"',base_units='"+data[6]+"' WHERE user_id ='"+data[0]+"' and feature_name = '"+data[1]+"'"

                res = cursor.execute(select_sql)
                print(res)
                if res == 1:
                    cursor.execute(update_sql)
                else:
                    insert_sql = "INSERT INTO subscriptions_for_brands (user_id, feature_name, units, price,customized_feature,added_units,base_units)" \
                                 " VALUES(" + data[0] + ",'" + data[1] + "'," + data[2] + "," + data[3] + ",'" + data[4] + "'," + data[5] + "," + data[6] + ")"
                    print(insert_sql)
                    cursor.execute(insert_sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print('i m here exception',e)
            return 0

    def insert_autofill_proposal_subscription_feature(self, data):
        try:
            with self.cnx.cursor() as cursor:
                print(data)
                data_tuple = tuple(data)
                print(type(data_tuple))

                select_sql = "SELECT 1 from subscription_feature_autofill_proposal where user_id ='" + data[
                    0] + "' and proposal_id = '" + data[1] + "'"
                update_sql = "UPDATE subscription_feature_autofill_proposal SET auto_or_manual='" + data[2] + "'" \
                             " WHERE user_id ='" + data[0] + "' and proposal_id = '" + data[1] + "'"
                res = cursor.execute(select_sql)
                print(res)
                if res == 1:
                    cursor.execute(update_sql)
                else:
                    insert_sql = "INSERT INTO subscription_feature_autofill_proposal (user_id, proposal_id, auto_or_manual)" \
                                 " VALUES(" + data[0] + "," + data[1] + ",'" + data[2] + "')"
                    print(insert_sql)
                    cursor.execute(insert_sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print('i m here exception', e)
            return 0

    def update_subscription_feature_details(self, user_id,feature_name,units,price,customized_feature):
        try:
            with self.cnx.cursor() as cursor:
                # print(data)
                sql = "UPDATE subscriptions_for_brands SET units="+units+", price="+price+" , customized_feature= '"+customized_feature+"' WHERE user_id = "+user_id+" AND feature_name = '"+feature_name+"'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0



    def reinitiateClassifiedAd(self,classified_id,user_id,posted_date):
        try:
            with self.cnx.cursor() as cursor:

                sql = "UPDATE brands_classifieds SET posted_date = '" + str(posted_date) + "' WHERE classified_id = '"\
                      + str(classified_id) + "' AND user_id = '" + str(user_id) + "'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0

    def reinitiateOffer(self,offer_id,channel_id,posted_date):
        try:
            with self.cnx.cursor() as cursor:

                sql = "UPDATE inf_offers SET posted_date = '" + str(posted_date) + "' WHERE offer_id = '"\
                      + str(offer_id) + "' AND channel_id = '" + str(channel_id) + "'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0





    def mark_notification_as_read(self, user_id,notification_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "UPDATE notifications SET `read_unread` = 'read' WHERE user_id = '" + user_id + "' and notification_id = '"+notification_id+"'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0



    def get_ccvr_by_user_id_and_classified_id(self, user_id,classified_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT ccvr_id,inserted_date,user_id,classified_id,inf_id,no_of_views,comment_message,reaction,notification_id" \
                      " FROM classified_comment_views_reaction" \
                      " WHERE user_id = '"+user_id+"' AND classified_id = '"+classified_id+"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)
            return 0

    def get_csn_by_campaign_id(self, campaign_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT csn_id,campaign_id,status_date,notification_id" \
                      " FROM campaign_status_notification" \
                      " WHERE campaign_id = '"+campaign_id+"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)
            return 0




    def get_ocvr_by_inf_id_and_offer_id(self, inf_id,offer_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT ocvr_id,inserted_date,user_id,offer_id,inf_id,no_of_views,comment_message,reaction,notification_id" \
                      " FROM offer_comment_views_reaction" \
                      " WHERE inf_id = '"+inf_id+"' AND offer_id = '"+offer_id+"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)
            return 0



    def update_notification_id_in_ccvr(self, user_id,ccvr_id,notification_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "UPDATE classified_comment_views_reaction SET `notification_id` = '"+notification_id+"'" \
                      " WHERE user_id = '" + user_id + "' and ccvr_id = '"+ccvr_id+"'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0
        
        
    def update_notification_id_in_ocvr(self, inf_id,ocvr_id,notification_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "UPDATE offer_comment_views_reaction SET `notification_id` = '"+notification_id+"'" \
                      " WHERE inf_id = '" + inf_id + "' and ocvr_id = '"+ocvr_id+"'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0



    def update_notification_id_in_csn(self, campaign_id,csn_id,notification_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "UPDATE campaign_status_notification SET `notification_id` = '"+notification_id+"'" \
                      " WHERE campaign_id = '" + campaign_id + "' and csn_id = '"+csn_id+"'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0


    def get_iam_by_user_id_and_inf_id(self, user_id,inf_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT iam_id,inserted_date,user_id,inf_id,notification_id" \
                      " FROM influencer_alert_milestone" \
                      " WHERE user_id = '"+user_id+"' AND inf_id = '"+inf_id+"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)
            return 0


    def update_notification_id_in_iam(self, user_id,iam_id,notification_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "UPDATE influencer_alert_milestone SET `notification_id` = '"+notification_id+"'" \
                      " WHERE user_id = '" + user_id + "' and iam_id = '"+iam_id+"'"
                print(sql)
                cursor.execute(sql)
                self.cnx.commit()
                # print(result)
                print("closing cnx")
                cursor.close()
                return 1
        except Exception as e:
            print(e)
            return 0


    def get_insta_channel_details_by_channel_id(self, channel_id):
        try:
            with self.cnx.cursor() as cursor:
                # sql = "SELECT " \
                #       " ui.first_name ,ui.last_name ,ui.business_email," \
                #       " ui.phone ,ui.categories , ui.website , ui.country ," \
                #       " ui.city ,ui.channel_id," \
                #       " chm.youtube_channel_id as mapped_youtube_channel_id,chm.twitter_channel_id as mapped_twitter_channel_id,chm.insta_channel_id as mapped_insta_channel_id," \
                #       " chm.confirmed," \
                #       " ycd.title, ycd.channel_img,ycd.country,ycd.facebook_url,ycd.twitter_url,ycd.insta_url," \
                #       " tcd.business_email,tcd.screen_name,tcd.title,tcd.channel_img,tcd.hashtags, icd.username as insta_username " \
                #       " FROM  channels_mapper chm " \
                #       " LEFT JOIN users_influencers ui ON ui.channel_id = chm.youtube_channel_id " \
                #       " LEFT JOIN insta_channel_details icd ON icd.insta_id = chm.insta_channel_id " \
                #       " LEFT JOIN twitter_channel_details tcd ON tcd.twitter_id = chm.twitter_channel_id" \
                #       " LEFT JOIN youtube_channel_details ycd ON chm.youtube_channel_id = ycd.channel_id " \
                #       " WHERE ui.channel_id = '"+user_id+"'"
                sql = "SELECT username from insta_channel_details where insta_id = '"+channel_id+"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)

    def get_twitter_channel_details_by_channel_id(self, channel_id):
        try:
            with self.cnx.cursor() as cursor:
                # sql = "SELECT " \
                #       " ui.first_name ,ui.last_name ,ui.business_email," \
                #       " ui.phone ,ui.categories , ui.website , ui.country ," \
                #       " ui.city ,ui.channel_id," \
                #       " chm.youtube_channel_id as mapped_youtube_channel_id,chm.twitter_channel_id as mapped_twitter_channel_id,chm.insta_channel_id as mapped_insta_channel_id," \
                #       " chm.confirmed," \
                #       " ycd.title, ycd.channel_img,ycd.country,ycd.facebook_url,ycd.twitter_url,ycd.insta_url," \
                #       " tcd.business_email,tcd.screen_name,tcd.title,tcd.channel_img,tcd.hashtags, icd.username as insta_username " \
                #       " FROM  channels_mapper chm " \
                #       " LEFT JOIN users_influencers ui ON ui.channel_id = chm.youtube_channel_id " \
                #       " LEFT JOIN insta_channel_details icd ON icd.insta_id = chm.insta_channel_id " \
                #       " LEFT JOIN twitter_channel_details tcd ON tcd.twitter_id = chm.twitter_channel_id" \
                #       " LEFT JOIN youtube_channel_details ycd ON chm.youtube_channel_id = ycd.channel_id " \
                #       " WHERE ui.channel_id = '"+user_id+"'"
                sql = "SELECT screen_name from twitter_channel_details where twitter_id = '"+channel_id+"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)


    def get_platform_analysis_details_by_user_id(self, user_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "select t6.proposal_id,t1.campaign_id,t8.first_name,t8.last_name,t8.categories,t8.country,t6.proposal_price,t6.proposal_from_date,t6.proposal_to_date,t1.regions,t1.video_cat_id,t1.campaign_status,t2.channel_id," \
                      "t2.revenue_generated,t2.new_users,t7.date_posted," \
                      "t7.link_posted," \
                      "t2.channel,t3.title as youtube_title,t4.username as insta_username,t5.screen_name as twitter_screen_name " \
                      "FROM campaign_proposal t6 " \
                      "JOIN brand_campaign_report t2 ON t6.user_id = t2.user_id " \
                      "LEFT JOIN youtube_channel_details t3 ON t3.channel_id = t2.channel_id " \
                      "LEFT JOIN insta_channel_details t4 ON t4.insta_id = t2.channel_id  " \
                      "LEFT JOIN twitter_channel_details t5 ON t5.twitter_id = t2.channel_id  " \
                      "LEFT JOIN brands_campaigns t1 ON t6.campaign_id = t1.campaign_id  " \
                      "JOIN inf_campaign_report t7 ON t2.channel_id = t7.channel_id " \
                      "LEFT JOIN users_influencers t8 ON t3.channel_id = t8.channel_id " \
                      "WHERE t1.user_id = '"+user_id+"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)



    def get_messages_by_user_id_and_user_type(self, email_id):
        try:
            with self.cnx.cursor(pymysql.cursors.DictCursor) as cursor:

                sql = "SELECT m.message_id, m.from_email_id, m.to_email_id, m.channel_id, m.date," \
                      " m.subject, m.message,m.user_id,m.user_type,m.deleted, m.deleted_from_bin," \
                      " m.deleted_from_user_id,m.deleted_from_bin_user_id,m.read," \
                      " ub.first_name as brand_first_name,ub.profile_pic as brand_profile_pic, " \
                      " ui.first_name as inf_first_name, ycd.channel_img as inf_youtube_profile_pic " \
                      " FROM messages m " \
                      " LEFT JOIN users_brands ub ON ub.email_id = m.from_email_id OR ub.email_id = m.to_email_id " \
                      " LEFT JOIN youtube_channel_details ycd ON ycd.business_email = m.from_email_id OR ycd.business_email = m.to_email.id " \
                      " LEFT JOIN users_influencers ui ON ui.business_email = m.from_email_id OR ui.business_email = m.to_email_id " \
                      " WHERE m.to_email_id = '"+email_id+"' OR m.from_email_id = '"+email_id+"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)


    def get_conversations_by_mess_id(self, message_id):
        try:
            with self.cnx.cursor(pymysql.cursors.DictCursor) as cursor:

                sql = "SELECT m.conv_id,m.message_id, m.conv_from_email_id, m.conv_to_email_id, m.conv_date," \
                      " m.conv_subject, m.conv_message,m.user_id,m.user_type,m.deleted, m.deleted_from_bin," \
                      " m.deleted_from_user_id,m.deleted_from_bin_user_id,m.read " \
                      " FROM conversations m " \
                      " WHERE m.message_id = '"+message_id+"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)


    def get_youtube_channel_ids_greater_than_1k(self):
        try:
            with self.cnx.cursor() as cursor:

                sql = "SELECT t1.channel_id from youtube_channel_ids t1" \
                      " JOIN youtube_channel_details t2 ON t1.channel_id = t2.channel_id " \
                      " WHERE t2.subscriberCount_gained > 1000 ORDER BY t2.subscriberCount_gained DESC"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)
