import pandas as pd
import pymysql,pymysql.cursors
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

        self.cnx = pymysql.connect(
            host=host,
        #     port=self.server.local_bind_port,
            user=user,
            password=password,
            db=db,
            use_unicode=True, charset="utf8"

        )


    def search_inf(self,channel_id,sort_order,min_lower='',max_upper='',country='',category_id=''):
        try:

            with self.cnx.cursor() as cursor:
                group_by=" group by t1.channel_id"
                category_id_filter = " t2.video_cat_id ="+category_id
                country_filter = " t3.regionCode = '"+country+"'"
                order='desc'
                if sort_order == 'High To Low':
                    order = 'desc'
                elif sort_order == 'Low To High':
                    order = 'asc'
                else:order='desc'
                order_by = " order by t1.subscriberCount_gained "+order

                sql = "SELECT t1.channel_id,t1.title, t1.channel_img, t1.desc, t1.subscriberCount_gained, " \
                "t1.subscriberCount_lost,t1.business_email, t1.total_100video_views, t1.total_100video_views_unique, " \
                "t1.total_100video_likes,t1.total_100video_dislikes, t1.total_100video_comments,t1.total_100video_shares, " \
                "t1.facebook_url,t1.insta_url,t1.twitter_url " \
                "FROM youtube_channel_details t1 " \
                "left join youtube_channel_ids_video_categories_id t2 on t1.channel_id = t2.channel_id " \
                "left join youtube_channel_ids_regioncode t3 on t1.channel_id = t3.channel_id " \
                "WHERE subscriberCount_gained BETWEEN "+min_lower+ " AND " + max_upper

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
                sql = "SELECT  * from " + table_name + " WHERE email_id = '" + email_id + "' "
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
                self.cnx.commit()
            print("closing cnx")
            cursor.close()
            res=1
        except Exception as e:
            res=0
            print(e)
            print("Exception Occured")
        return res