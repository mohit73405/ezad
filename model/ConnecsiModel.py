import pandas as pd
import pymysql,pymysql.cursors
from sshtunnel import SSHTunnelForwarder

class ConnecsiModel:
    def __init__(self):
        #self.URL = URL
        print("")
        # self.server = SSHTunnelForwarder(
        #     '46.28.109.89',
        #     ssh_username='kiran',
        #     ssh_password='vD2eV&^bKS(AB92G',
        #     ssh_pkey='C:/Users/Mika/.ssh/id_rsa',
        #     remote_bind_address=('127.0.0.1', 3306)
        # )
        # self.server.start()

        self.cnx = pymysql.connect(
            host='127.0.0.1',
        #     port=self.server.local_bind_port,
            user='root',
            password='',
            db='connecsi_admin',
            use_unicode=True, charset="utf8"

        )


    def get__(self,table_name,columns,STAR='',WHERE='',compare_column='',compare_value=''):
        columns_string=''
        if columns:
            for name in columns:
                #print(name)
                columns_string+=''.join('`'+name+'`'+',')
        columns_string = columns_string[:-1]
        where_string=''
        if WHERE:
            where_string+=''.join(WHERE)
            where_string+=' '.join('`'+compare_column+'`')
            where_string+=' '.join("'"+compare_value+"'")
        try:
            with self.cnx.cursor() as cursor:
                sql = "SELECT "+ STAR + columns_string + " from " + table_name + "` "+where_string
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                #print(result)
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
                cursor.execute(sql, data)
                self.cnx.commit()
            print("closing cnx")
            cursor.close()
        except Exception as e:
            print(e)
            print("Exception Occured")