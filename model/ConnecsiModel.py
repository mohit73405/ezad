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
                # country_filter = " t3.regionCode = '"+country+"'"
                country_filter = " t1.country = '" + country + "'"
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
                "t1.facebook_url,t1.insta_url,t1.twitter_url,t1.country " \
                "FROM youtube_channel_details t1 " \
                "left join youtube_channel_ids_video_categories_id t2 on t1.channel_id = t2.channel_id " \
                "WHERE subscriberCount_gained BETWEEN "+min_lower+ " AND " + max_upper
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
                elif table_name == 'messages':
                    cursor.execute(sql, data)
                    inserted_id = cursor.lastrowid
                elif table_name == 'conversations':
                    cursor.execute(sql, data)
                elif table_name == 'brands_inf_fav_list':
                    cursor.execute(sql, data)
                elif table_name == 'brands_classifieds':
                    cursor.execute(sql, data)
                elif table_name == 'channel_campaign_message':
                    cursor.execute(sql, data)
                elif table_name == 'message_campaigns':
                    cursor.execute(sql, data)
                elif table_name == 'campaign_proposal':
                    cursor.execute(sql, data)
                elif table_name == 'user_channel_message_files':
                    cursor.execute(sql, data)
                elif table_name == 'user_channel_message_agreements':
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
                sql = "SELECT  * from " + table_name + " WHERE conv_to_email_id = '" + to_email_id  + "' GROUP BY message_id DESC"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data

        except Exception as e:
            print(e)

    def get_conversations_by_from_email_id(self,from_email_id):
        try:
            with self.cnx.cursor() as cursor:
                table_name = 'conversations'
                sql = "SELECT  * from " + table_name + " WHERE conv_from_email_id = '" + from_email_id  + "' GROUP BY message_id DESC"
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
                      "  WHERE classified_id = '" + classified_id  + "' AND user_id = '" + user_id+"'"
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
                sql = "UPDATE conversations SET deleted = 'true', deleted_from_user_id = CONCAT(IFNULL(deleted_from_user_id,''), ',"+ user_id +"') WHERE message_id = '" + message_id + "' AND conv_id = '" + conv_id + "'"
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
                sql = "UPDATE messages SET deleted = 'true', deleted_from_user_id = CONCAT(IFNULL(deleted_from_user_id,''), ',"+ user_id +"') WHERE message_id = '" + message_id + "'"
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
                sql = "SELECT bi.channel_id,ycd.title,ycd.channel_img,ycd.desc,ycd.subscriberCount_gained,ycd.subscriberCount_lost,ycd.business_email" \
                      ",ycd.total_100video_views,ycd.total_100video_views_unique,ycd.total_100video_likes,ycd.total_100video_dislikes," \
                      "ycd.total_100video_comments,ycd.total_100video_shares,ycd.facebook_url,ycd.insta_url,ycd.twitter_url," \
                      "bi.alert_followers,bi.alert_views,bi.alert_likes,bi.alert_comments " \
                      " FROM brands_inf_fav_list bi JOIN youtube_channel_details ycd on bi.channel_id = ycd.channel_id" \
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

    def create_alert_for_fav_influencer(self, user_id,channel_id,alert_followers,alert_views,alert_likes,alert_comments):

        columns = ['user_id', 'channel_id', 'alert_followers', 'alert_views', 'alert_likes', 'alert_comments']
        data = (user_id, channel_id, alert_followers, alert_views, alert_likes, alert_comments)

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


    def get_youtube_inf_list(self, campaign_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT ccm.channel_id,ycd.title,ycd.channel_img FROM channel_campaign_message ccm" \
                      " JOIN youtube_channel_details ycd on ccm.channel_id = ycd.channel_id" \
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

    def update_channel_campaign_message(self, channel_id,message_id,status):
        try:
            with self.cnx.cursor() as cursor:
                print('channel id =',channel_id,type(channel_id))
                print('message id =', message_id,type(message_id))
                print('status = ',status,type(status))
                sql = "UPDATE channel_campaign_message SET message_id = "+ str(message_id) +", status = '"+ status +"' WHERE channel_id = '" + str(channel_id)\
                      +"' AND status !='Proposal Sent' AND status !='Current Partner'"
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


    def get_all_proposal(self, user_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT " \
                      " cp.proposal_id,cp.campaign_id, cp.campaign_name, cp.message_id, cp.user_id, " \
                      " ub.company_name,ub.email_id," \
                      " ycd.channel_id,ycd.title,ycd.business_email," \
                      " cp.influencer_id, cp.proposal_description,cp.proposal_from_date,cp.proposal_to_date," \
                      " cp.proposal_channels,cp.proposal_arrangements,cp.proposal_kpis,cp.currency,cp.proposal_price" \
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


    def get_proposal(self, proposal_id):
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT " \
                      " cp.proposal_id,cp.campaign_id, cp.campaign_name, cp.message_id, cp.user_id, " \
                      " ub.company_name,ub.email_id," \
                      " ycd.channel_id,ycd.title,ycd.business_email," \
                      " cp.influencer_id, cp.proposal_description,cp.proposal_from_date,cp.proposal_to_date," \
                      " cp.proposal_channels,cp.proposal_arrangements,cp.proposal_kpis,cp.currency,cp.proposal_price" \
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
                      " cp.proposal_channels,cp.proposal_arrangements,cp.proposal_kpis,cp.currency,cp.proposal_price" \
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

    def confirm_brands_email(self,user_id,confirmed):
        try:
            with self.cnx.cursor() as cursor:

                sql = "UPDATE users_brands SET confirmed_email = '" + str(confirmed) + "' WHERE user_id = '"+ str(user_id) +"'"
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
                sql = "SELECT * from brand_campaign_report WHERE user_id  = '"+ user_id +"' AND campaign_id = '"+ campaign_id +"'"
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)
            print("closing cnx")
            cursor.close()
            return data
        except Exception as e:
            print(e)


    def update_brand_campaign_report(self,user_id,campaign_id,data):
        try:
            with self.cnx.cursor() as cursor:
                sql = "UPDATE brand_campaign_report SET revenue_generated = '%s', currency = '%s', target_url = '%s'" \
                      " new_users = '%s' WHERE user_id = '"+ user_id + "'" +"AND campaign_id = '"+ campaign_id +"'"
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