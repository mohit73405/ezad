from flask import Flask, request, session
from flask_restplus import Resource, Api, fields, Namespace
from model.ConnecsiModel import ConnecsiModel
from passlib.hash import sha256_crypt

import datetime
import smtplib
import email.message


ns_messages = Namespace('Messages', description='Messages Operations')

message_form = ns_messages.model('Message Details', {
    'from_email_id' : fields.String(required=True, description='From Email Id'),
    'to_email_id' : fields.String(required=True, description='To Email Id'),
    'date' : fields.String(required=True, description='Date'),
    'subject' : fields.String(required=True, description='Subject'),
    'message' : fields.String(required=True, description='Message')
})

conversation_form = ns_messages.model('Conversation Details', {
    # 'message_id' : fields.Integer(required=True, description='Message ID'),
    'conv_from_email_id' : fields.String(required=True, description='From Email Id'),
    'conv_to_email_id' : fields.String(required=True, description='To Email Id'),
    'conv_date' : fields.String(required=True, description='Date'),
    'conv_subject' : fields.String(required=True, description='Subject'),
    'conv_message' : fields.String(required=True, description='Message')
})


@ns_messages.route('/<string:user_id>/<string:user_type>')
class MailBox(Resource):
    @ns_messages.expect(message_form)
    def post(self,user_id,user_type):
        '''Send message'''
        form_data = request.get_json()
        from_email_id = form_data.get('from_email_id')
        to_email_id = form_data.get('to_email_id')
        channel_id = form_data.get('channel_id')
        date = form_data.get('date')
        subject = form_data.get('subject')
        message = form_data.get('message')
        campaign_id = ''
        try:
            campaign_id = form_data.get('campaign_id')
        except:
            pass

        columns = ['from_email_id', 'to_email_id','channel_id', 'date', 'subject', 'message','user_id','user_type']
        data = [from_email_id, to_email_id,channel_id, date, subject, message,user_id,user_type]
        print(data)
        result=0
        try:
            if user_type == 'brand':
                email_content='''
                <!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office"><head>  <title></title>  <!--[if !mso]><!-- -->  <meta http-equiv="X-UA-Compatible" content="IE=edge">  <!--<![endif]--><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><style type="text/css">  #outlook a { padding: 0; }  .ReadMsgBody { width: 100%; }  .ExternalClass { width: 100%; }  .ExternalClass * { line-height:100%; }  body { margin: 0; padding: 0; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }  table, td { border-collapse:collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; }  img { border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; }  p { display: block; margin: 13px 0; }</style><!--[if !mso]><!--><style type="text/css">  @media only screen and (max-width:480px) {    @-ms-viewport { width:320px; }    @viewport { width:320px; }  }</style><!--<![endif]--><!--[if mso]><xml>  <o:OfficeDocumentSettings>    <o:AllowPNG/>    <o:PixelsPerInch>96</o:PixelsPerInch>  </o:OfficeDocumentSettings></xml><![endif]--><!--[if lte mso 11]><style type="text/css">  .outlook-group-fix {    width:100% !important;  }</style><![endif]--><!--[if !mso]><!-->    <link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet" type="text/css"><link href="https://fonts.googleapis.com/css?family=Ubuntu:300,400,500,700" rel="stylesheet" type="text/css">    <style type="text/css">        @import url(https://fonts.googleapis.com/css?family=Roboto);  @import url(https://fonts.googleapis.com/css?family=Ubuntu:300,400,500,700);    </style>  <!--<![endif]--><style type="text/css">  @media only screen and (min-width:480px) {    .mj-column-per-100 { width:100%!important; }.mj-column-per-50 { width:50%!important; }  }</style></head><body style="background: #FFFFFF;">    <div class="mj-container" style="background-color:#FFFFFF;"><!--[if mso | IE]>      <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="600" align="center" style="width:600px;">        <tr>          <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">      <![endif]--><div style="margin:0px auto;max-width:600px;background:#FFFFFF;"><table role="presentation" cellpadding="0" cellspacing="0" style="font-size:0px;width:100%;background:#FFFFFF;" align="center" border="0"><tbody><tr><td style="text-align:center;vertical-align:top;direction:ltr;font-size:0px;padding:0px 0px 0px 0px;"><!--[if mso | IE]>      <table role="presentation" border="0" cellpadding="0" cellspacing="0">        <tr>          <td style="vertical-align:top;width:600px;">      <![endif]--><div class="mj-column-per-100 outlook-group-fix" style="vertical-align:top;display:inline-block;direction:ltr;font-size:13px;text-align:left;width:100%;"><table role="presentation" cellpadding="0" cellspacing="0" style="vertical-align:top;" width="100%" border="0"><tbody><tr><td style="word-wrap:break-word;font-size:0px;padding:20px 40px 0px 40px;" align="center"><table role="presentation" cellpadding="0" cellspacing="0" style="border-collapse:collapse;border-spacing:0px;" align="center" border="0"><tbody><tr><td style="width:240px;"><img alt height="auto" src="https://www.connecsi.live/static/img/logo_full.png" style="border:none;border-radius:0px;display:block;font-size:13px;outline:none;text-decoration:none;width:100%;height:auto;" width="240"></td></tr></tbody></table></td></tr><tr><td style="word-wrap:break-word;font-size:0px;padding:10px 30px 0px 30px;" align="center"><div style="cursor:auto;color:#4A90E2;font-family:PT Sans, Trebuchet MS, sans-serif;font-size:11px;line-height:1.5;text-align:center;"><p><span style="font-size:16px;"><strong>Congratulations! Brands are searching for you.</strong></span></p></div></td></tr><tr><td style="word-wrap:break-word;font-size:0px;padding:0px 30px 0px 30px;" align="left"><div style="cursor:auto;color:#000000;font-family:Roboto, Tahoma, sans-serif;font-size:11px;line-height:1.5;text-align:left;"><p><span style="font-size:14px;">A connecsi user wants to connect with you to explore collaboration opportunities. You may see the&#xA0;message by clicking the button below:</span></p></div></td></tr><tr><td style="word-wrap:break-word;font-size:0px;padding:16px 16px 16px 16px;" align="center"><table role="presentation" cellpadding="0" cellspacing="0" style="border-collapse:separate;width:auto;" align="center" border="0"><tbody><tr><td style="border:0px solid #000;border-radius:3px;color:#fff;cursor:auto;padding:10px 30px;" align="center" valign="middle" bgcolor="#A55FE2"><a href="https://www.connecsi.live/#influencer" style="text-decoration:none;background:#A55FE2;color:#fff;font-family:Ubuntu, Helvetica, Arial, sans-serif, Helvetica, Arial, sans-serif;font-size:15px;font-weight:normal;line-height:120%;text-transform:none;margin:0px;" target="_blank">See Message</a></td></tr></tbody></table></td></tr><tr><td style="word-wrap:break-word;font-size:0px;padding:10px 25px;padding-top:10px;padding-bottom:10px;padding-right:30px;padding-left:30px;"><p style="font-size:1px;margin:0px auto;border-top:1px solid #9A9A9A;width:100%;"></p><!--[if mso | IE]><table role="presentation" align="center" border="0" cellpadding="0" cellspacing="0" style="font-size:1px;margin:0px auto;border-top:1px solid #9A9A9A;width:100%;" width="600"><tr><td style="height:0;line-height:0;"> </td></tr></table><![endif]--></td></tr><tr><td style="word-wrap:break-word;font-size:0px;padding:0px 30px 0px 30px;" align="center"><div style="cursor:auto;color:#000000;font-family:Roboto, Tahoma, sans-serif;font-size:11px;line-height:1.5;text-align:center;"><p><span style="font-size:14px;"><strong>What is&#xA0; Connecsi?</strong></span></p></div></td></tr><tr><td style="word-wrap:break-word;font-size:0px;padding:0px 30px 0px 30px;" align="justify"><div style="cursor:auto;color:#000000;font-family:Roboto, Tahoma, sans-serif;font-size:11px;line-height:1.5;text-align:justify;"><p><span style="font-size: 14px;">Connecsi is an easy to use influencer marketing platform that helps brands and influencers to connect and collaborate in a safe ecosystem.</span></p></div></td></tr><tr><td style="word-wrap:break-word;font-size:0px;padding:0px 30px 0px 30px;" align="center"><div style="cursor:auto;color:#000000;font-family:Roboto, Tahoma, sans-serif;font-size:11px;line-height:1.5;text-align:center;"><p><span style="font-size: 14px;"><b>Benefits:</b></span></p></div></td></tr></tbody></table></div><!--[if mso | IE]>      </td></tr></table>      <![endif]--></td></tr></tbody></table></div><!--[if mso | IE]>      </td></tr></table>      <![endif]-->      <!--[if mso | IE]>      <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="600" align="center" style="width:600px;">        <tr>          <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">      <![endif]--><div style="margin:0px auto;max-width:600px;background:#FFFFFF;"><table role="presentation" cellpadding="0" cellspacing="0" style="font-size:0px;width:100%;background:#FFFFFF;" align="center" border="0"><tbody><tr><td style="text-align:center;vertical-align:top;direction:ltr;font-size:0px;padding:0px 0px 0px 0px;"><!--[if mso | IE]>      <table role="presentation" border="0" cellpadding="0" cellspacing="0">        <tr>          <td style="vertical-align:top;width:300px;">      <![endif]--><div class="mj-column-per-50 outlook-group-fix" style="vertical-align:top;display:inline-block;direction:ltr;font-size:13px;text-align:left;width:100%;"><table role="presentation" cellpadding="0" cellspacing="0" style="vertical-align:top;" width="100%" border="0"><tbody><tr><td style="word-wrap:break-word;font-size:0px;padding:0px 15px 0px 30px;" align="left"><div style="cursor:auto;color:#000000;font-family:Roboto, Tahoma, sans-serif;font-size:11px;line-height:1.5;text-align:left;"><p></p><p></p><p><span style="font-size:14px;">&#xA0;<img alt="*" draggable="false" src="http://www.pngmart.com/files/7/Check-PNG-Transparent-Image.png" style="width: 30px; height: 28px; float: left;">Free to use - No commissions or fee</span></p><p><span style="font-size:14px;"><img alt="*" draggable="false" src="http://www.pngmart.com/files/7/Check-PNG-Transparent-Image.png" style="width: 30px; float: left; height: 28px;">&#xA0;Respond to classified ads&#xA0;posted&#xA0;by Brands.</span></p><p><span style="font-size:14px;"><img alt="*" draggable="false" src="http://www.pngmart.com/files/7/Check-PNG-Transparent-Image.png" style="width: 30px; height: 28px; float: left;">&#xA0;Outreach Brands by posting your offers.</span></p></div></td></tr></tbody></table></div><!--[if mso | IE]>      </td><td style="vertical-align:top;width:300px;">      <![endif]--><div class="mj-column-per-50 outlook-group-fix" style="vertical-align:top;display:inline-block;direction:ltr;font-size:13px;text-align:left;width:100%;"><table role="presentation" cellpadding="0" cellspacing="0" style="vertical-align:top;" width="100%" border="0"><tbody><tr><td style="word-wrap:break-word;font-size:0px;padding:0px 15px 0px 30px;" align="left"><div style="cursor:auto;color:#000000;font-family:Roboto, Tahoma, sans-serif;font-size:11px;line-height:1.5;text-align:left;"><p><span style="font-size:14px;"><img alt="*" src="http://www.pngmart.com/files/7/Check-PNG-Transparent-Image.png" style="width: 30px; height: 28px; float: left;">&#xA0;Connect with&#xA0;thousands of Brands worldwide.</span></p><p><span style="font-size:14px;"><img alt="*" src="http://www.pngmart.com/files/7/Check-PNG-Transparent-Image.png" style="height: 28px; width: 30px; float: left;">&#xA0;Manage your campaigns seamlessly using automation.</span></p></div></td></tr></tbody></table></div><!--[if mso | IE]>      </td></tr></table>      <![endif]--></td></tr></tbody></table></div><!--[if mso | IE]>      </td></tr></table>      <![endif]-->      <!--[if mso | IE]>      <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="600" align="center" style="width:600px;">        <tr>          <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">      <![endif]--><table role="presentation" cellpadding="0" cellspacing="0" style="background:#FFFFFF;font-size:0px;width:100%;" border="0"><tbody><tr><td><div style="margin:0px auto;max-width:600px;"><table role="presentation" cellpadding="0" cellspacing="0" style="font-size:0px;width:100%;" align="center" border="0"><tbody><tr><td style="text-align:center;vertical-align:top;direction:ltr;font-size:0px;padding:9px 0px 9px 0px;"><!--[if mso | IE]>      <table role="presentation" border="0" cellpadding="0" cellspacing="0">        <tr>          <td style="vertical-align:top;width:600px;">      <![endif]--><div class="mj-column-per-100 outlook-group-fix" style="vertical-align:top;display:inline-block;direction:ltr;font-size:13px;text-align:left;width:100%;"><table role="presentation" cellpadding="0" cellspacing="0" style="vertical-align:top;" width="100%" border="0"><tbody><tr><td style="word-wrap:break-word;font-size:0px;padding:0px 30px 0px 30px;" align="center"><div style="cursor:auto;color:#000000;font-family:Roboto, Tahoma, sans-serif;font-size:11px;line-height:1.5;text-align:center;"><p><span style="font-size:14px;"><strong>&#xA0;How to get started?&#xA0;<a href="https://calendly.com/connecsi-team/free-demo" onclick="window.open(this.href, &apos;BookNow&apos;, &apos;resizable=yes,status=no,location=no,toolbar=no,menubar=no,fullscreen=no,scrollbars=no,dependent=no&apos;); return false;"><span style="color:#9b59b6;">Get Free Demo</span></a></strong></span></p><p></p><p></p></div></td></tr><tr><td style="word-wrap:break-word;font-size:0px;padding:0px 30px 0px 30px;" align="left"><div style="cursor:auto;color:#000000;font-family:Roboto, Tahoma, sans-serif;font-size:11px;line-height:1.5;text-align:left;"><p><strong><span style="font-size:12px;">Any doubts? Questions?</span></strong></p><p><span style="font-size:12px;">Send us an email to <span style="color:#3498db;">contact@connecsi.com</span> we will be happy to help. Have a great campaign!</span></p><p><span style="font-size:12px;">Connecsi Team</span></p></div></td></tr><tr><td style="word-wrap:break-word;font-size:0px;padding:10px 10px 10px 10px;" align="center"><div><!--[if mso | IE]>      <table role="presentation" border="0" cellpadding="0" cellspacing="0" align="undefined"><tr><td>      <![endif]--><table role="presentation" cellpadding="0" cellspacing="0" style="float:none;display:inline-table;" align="center" border="0"><tbody><tr><td style="padding:4px;vertical-align:middle;"><table role="presentation" cellpadding="0" cellspacing="0" style="background:none;border-radius:3px;width:30px;" border="0"><tbody><tr><td style="font-size:0px;vertical-align:middle;width:30px;height:30px;"><a href="https://www.facebook.com/connecsi/"><img alt="facebook" height="30" src="https://s3-eu-west-1.amazonaws.com/ecomail-assets/editor/social-icos/rounded/facebook.png" style="display:block;border-radius:3px;" width="30"></a></td></tr></tbody></table></td></tr></tbody></table><!--[if mso | IE]>      </td><td>      <![endif]--><table role="presentation" cellpadding="0" cellspacing="0" style="float:none;display:inline-table;" align="center" border="0"><tbody><tr><td style="padding:4px;vertical-align:middle;"><table role="presentation" cellpadding="0" cellspacing="0" style="background:none;border-radius:3px;width:30px;" border="0"><tbody><tr><td style="font-size:0px;vertical-align:middle;width:30px;height:30px;"><a href="https://twitter.com/Connecsi"><img alt="twitter" height="30" src="https://s3-eu-west-1.amazonaws.com/ecomail-assets/editor/social-icos/rounded/twitter.png" style="display:block;border-radius:3px;" width="30"></a></td></tr></tbody></table></td></tr></tbody></table><!--[if mso | IE]>      </td><td>      <![endif]--><table role="presentation" cellpadding="0" cellspacing="0" style="float:none;display:inline-table;" align="center" border="0"><tbody><tr><td style="padding:4px;vertical-align:middle;"><table role="presentation" cellpadding="0" cellspacing="0" style="background:none;border-radius:3px;width:30px;" border="0"><tbody><tr><td style="font-size:0px;vertical-align:middle;width:30px;height:30px;"><a href="https://www.linkedin.com/company/connecsi/"><img alt="linkedin" height="30" src="https://s3-eu-west-1.amazonaws.com/ecomail-assets/editor/social-icos/rounded/linkedin.png" style="display:block;border-radius:3px;" width="30"></a></td></tr></tbody></table></td></tr></tbody></table><!--[if mso | IE]>      </td><td>      <![endif]--><table role="presentation" cellpadding="0" cellspacing="0" style="float:none;display:inline-table;" align="center" border="0"><tbody><tr><td style="padding:4px;vertical-align:middle;"><table role="presentation" cellpadding="0" cellspacing="0" style="background:none;border-radius:3px;width:30px;" border="0"><tbody><tr><td style="font-size:0px;vertical-align:middle;width:30px;height:30px;"><a href="https://l.facebook.com/l.php?u=https%3A%2F%2Finstagram.com%2Fhttps%3A%2F%2Fwww.instagram.com%2Fconnecsi%2F%3Ffbclid%3DIwAR2RN3sT0RAOVsp24OrnxyeAGzHTI6HrC32F8I1S5IyIAVPPDfxMN19Thko&amp;h=AT3Iouff1G_C-p4r60OI3vVdbkIaxANq-mBGPicp6PE-BJq5hySHudzNn9GCF2RqCmjE7AaXiUYceSbvdf77jbAho3fhQ6X_8KNy2_ZnMAG60MhpQTezCU_MWzhhZkp0zXWKdLodb91lITIwji7GUd4Wz6CS0r3UUTQxQRE0edoGzG2GrXBSHZjUtaOkbGZ85kOHv_tv4DRcd9Wa9geoW5zGEB70f4PJizSOb3OVzyhj65ush0C2kf2nB8LQ4mZlQjmsStzn1D_8IeDJg1RDxOZGn4SarlBemYNwrmBlJL_R9SbHI5GN89Gw1EPn36ok0hlxO2OMoCbgzwturIwrLS-y8TLLKIc-5_OtoDGwLr7blIg1mvXsPEzs_BSB8b66p3TWh6Fb9IqowpAUtu-3KdMcHJqsQ_4ppwrop4LO3n57KT-YMB_xvQQ5c-ABMDnxOlQgk0TC8wQmHpQt0QKbGPsJGBWtfvIVa2ZP"><img alt="instagram" height="30" src="https://s3-eu-west-1.amazonaws.com/ecomail-assets/editor/social-icos/rounded/instagram.png" style="display:block;border-radius:3px;" width="30"></a></td></tr></tbody></table></td></tr></tbody></table><!--[if mso | IE]>      </td></tr></table>      <![endif]--></div></td></tr></tbody></table></div><!--[if mso | IE]>      </td></tr></table>      <![endif]--></td></tr></tbody></table></div></td></tr></tbody></table><!--[if mso | IE]>      </td></tr></table>      <![endif]--></div></body></html>
                '''
                self.send_mail(subject=subject,to_email_id=to_email_id,email_content=email_content)
            else:
                email_content = """
                        <html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>Connecsi</title></head><body>Connecsi User wants to connect with you...Please login to view the full message...<a href="#">Login</a></body></html>
                        """
                self.send_mail(subject=subject,to_email_id=to_email_id,email_content=email_content)
            connecsiObj = ConnecsiModel()
            message_id = connecsiObj.insert__(table_name='messages',columns=columns,data=data,IGNORE='IGNORE')
            if channel_id and campaign_id:
                channel_id = channel_id.split('@')
                channel_id = channel_id[0]
                connecsiObj.update_channel_campaign_message(campaign_id=campaign_id,channel_id=str(channel_id),message_id=str(message_id),status='Contacted')
            # elif channel_id:
            #     channel_id = channel_id.split('@')
            #     channel_id = channel_id[0]
            #     connecsiObj.update_channel_campaign_message(channel_id=str(channel_id),message_id=str(message_id),status='Contacted')
            return {'response': 1},200
        except Exception as e:
            print(e)
            return {'response': result},500

    def get(self,user_id,user_type):
        ''' get messages by user id and user type'''
        try:
            connecsiObj = ConnecsiModel()
            if user_type == 'brand':
                user = connecsiObj.get__(table_name='users_brands',STAR='*',WHERE='WHERE',compare_column='user_id',compare_value=str(user_id))
                print(user)
                print(user[0][3])
                email_id = user[0][3]
                data = connecsiObj.get_messages_by_email_id_and_user_type(email_id=str(email_id),user_type=user_type)
                print(data)
                columns = ['message_id','from_email_id', 'to_email_id','channel_id', 'date', 'subject', 'message', 'user_id', 'user_type',
                       'deleted','deleted_from_bin','deleted_from_user_id','deleted_from_bin_user_id','read']
                response_list = []
                for item in data:
                    dict_temp = dict(zip(columns, item))
                    response_list.append(dict_temp)
                return {'data': response_list}
            if user_type == 'influencer':
                user = connecsiObj.get__(table_name='users_influencers',STAR='*',WHERE='WHERE',compare_column='channel_id',compare_value=str(user_id))
                print(user)
                # print(user[0][2])
                email_id = user[0][2]
                data = connecsiObj.get_messages_by_email_id_and_user_type(email_id=str(email_id),user_type=user_type)
                print(data)
                columns = ['message_id','from_email_id', 'to_email_id','channel_id', 'date', 'subject', 'message', 'user_id', 'user_type',
                       'deleted','deleted_from_bin','deleted_from_user_id','deleted_from_bin_user_id','read']
                response_list = []
                for item in data:
                    dict_temp = dict(zip(columns, item))
                    response_list.append(dict_temp)
                return {'data': response_list}
        except Exception as e:
            return {"response": e},500


    def send_mail(self,subject,to_email_id,email_content):

        msg = email.message.Message()
        msg['Subject'] = subject
        msg['From'] = 'business@connecsi.com'
        msg['To'] = to_email_id
        password = "Ezadteam"
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(email_content)

        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        # Login Credentials for sending the mail
        server.login(msg['From'], password)
        server.sendmail(msg['From'], [msg['To']], msg.as_string())


@ns_messages.route('/conversations/<string:message_id>/<string:user_id>/<string:user_type>')
class MailBox(Resource):
    @ns_messages.expect(conversation_form)
    def post(self, message_id,user_id, user_type):
        '''Reply to message'''
        form_data = request.get_json()
        print('form data = ',form_data)
        print(type(form_data))
        from_email_id = form_data.get('conv_from_email_id')
        to_email_id = form_data.get('to_email_id')
        date = form_data.get('conv_date')
        print('conv_date = ',date)
        subject = form_data.get('subject')
        message = form_data.get('message')
        channel_id = form_data.get('channel_id')
        if '@' in channel_id:
            channel_id_list=channel_id.split('@')
            channel_id = channel_id_list[0]
        campaign_id = ''
        try:
            campaign_id = form_data.get('campaign_id')
        except:
            pass

        columns = ['message_id','conv_from_email_id', 'conv_to_email_id', 'conv_date', 'conv_subject', 'conv_message', 'user_id', 'user_type']
        data = [message_id,from_email_id, to_email_id, str(date), subject, message, user_id, user_type]
        print('data to insert = ',data)
        result = 0
        try:
            self.send_mail(subject=subject, to_email_id=to_email_id)
            connecsiObj = ConnecsiModel()
            result = connecsiObj.insert__(table_name='conversations', columns=columns, data=data, IGNORE='IGNORE')
            if channel_id and campaign_id:
                connecsiObj.update_channel_campaign_message_for_negotiations(channel_id=str(channel_id),message_id=str(message_id),status='Negotiations',campaign_id=campaign_id)
            return {'response': 1}, 200
        except Exception as e:
            print(e)
            return {'response': result}, 500

    def get(self,message_id,user_id,user_type):
        ''' Get Conversations by message id'''
        try:
            connecsiObj = ConnecsiModel()
            # user = connecsiObj.get__(table_name='users_brands', STAR='*', WHERE='WHERE', compare_column='user_id',
            #                          compare_value=str(user_id))
            # print(user)
            # print(user[0][3])
            # email_id = user[0][3]
            data = connecsiObj.get_conversations_by_message_id(message_id=str(message_id))
            print(data)
            columns = ['conv_id','message_id', 'date', 'from_email_id', 'to_email_id', 'subject', 'message', 'user_id',
                       'user_type','deleted','deleted_from_bin','deleted_from_user_id','deleted_from_bin_user_id','read']
            response_list = []
            for item in data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            print(response_list)
            return {'data': response_list}
        except Exception as e:
            return {"response": e}, 500

    def send_mail(self,subject,to_email_id):
        email_content = """
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
           <title>Connecsi</title>
        </head>
        <body>
        Connecsi User wants to connect with you...
        Please login to view the full message...
        <a href="#">Login</a>
        </body>
        </html>
        """
        msg = email.message.Message()
        msg['Subject'] = subject
        msg['From'] = 'business@connecsi.com'
        msg['To'] = to_email_id
        password = "Ezadteam"
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(email_content)

        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        # Login Credentials for sending the mail
        server.login(msg['From'], password)
        server.sendmail(msg['From'], [msg['To']], msg.as_string())


@ns_messages.route('/conversations/<string:to_email_id>')
class MailBox(Resource):
    def get(self,to_email_id):
        ''' Get Conversations by to email id'''
        try:
            connecsiObj = ConnecsiModel()
            data = connecsiObj.get_conversations_by_to_email_id(to_email_id=str(to_email_id))
            print(data)
            columns = ['conv_id','message_id', 'date', 'from_email_id', 'to_email_id', 'subject', 'message', 'user_id',
                       'user_type','deleted','deleted_from_bin','deleted_from_user_id','deleted_from_bin_user_id','read']
            response_list = []
            for item in data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}
        except Exception as e:
            return {"response": e}, 500


@ns_messages.route('/conversations/all/<string:user_type>')
class MailBox(Resource):
    def get(self,user_type):
        ''' Get Conversations by user type'''
        try:
            connecsiObj = ConnecsiModel()
            data = connecsiObj.get_conversations_by_user_type(user_type=str(user_type))
            print(data)
            columns = ['conv_id','message_id', 'date', 'from_email_id', 'to_email_id', 'subject', 'message', 'user_id',
                       'user_type','deleted','deleted_from_bin','deleted_from_user_id','deleted_from_bin_user_id','read']
            response_list = []
            for item in data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}
        except Exception as e:
            return {"response": e}, 500



@ns_messages.route('/conversations/sent/<string:from_email_id>')
class MailBox(Resource):
    def get(self,from_email_id):
        ''' Get Conversations by from email id'''
        try:
            connecsiObj = ConnecsiModel()
            data = connecsiObj.get_conversations_by_from_email_id(from_email_id=str(from_email_id))
            print(data)
            columns = ['conv_id','message_id', 'date', 'from_email_id', 'to_email_id', 'subject', 'message', 'user_id',
                       'user_type','deleted','deleted_from_bin','deleted_from_user_id','deleted_from_bin_user_id','read']
            response_list = []
            for item in data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}
        except Exception as e:
            return {"response": e}, 500

@ns_messages.route('/getSentMessages/<string:from_email_id>')
class MailBox(Resource):
    def get(self,from_email_id):
        ''' Get sent messages by from email id'''
        try:
            connecsiObj = ConnecsiModel()
            data = connecsiObj.get_messages_by_from_email_id(from_email_id=str(from_email_id))
            print(data)
            columns = ['message_id', 'from_email_id', 'to_email_id', 'channel_id', 'date', 'subject', 'message', 'user_id',
                       'user_type','deleted','deleted_from_bin','deleted_from_user_id','deleted_from_bin_user_id','read']
            response_list = []
            for item in data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}
        except Exception as e:
            return {"response": e}, 500



@ns_messages.route('/conversations/delete/<string:message_id>/<string:conv_id>/<string:user_id>')
class Delete(Resource):
    def put(self,message_id,conv_id,user_id):
        ''' Delete message from Conversations by  message_id,conv_id and from user_id'''
        try:
            connecsiObj = ConnecsiModel()
            data = connecsiObj.delete_message_from_conversation(message_id=message_id,conv_id=conv_id,user_id=user_id)
            print(data)
            return {'data': data}
        except Exception as e:
            return {"response": e}, 500

@ns_messages.route('/delete/<string:message_id>/<string:user_id>')
class Delete(Resource):
    def put(self,message_id,user_id):
        ''' Delete message from messages by message_id and from user_id'''
        try:
            connecsiObj = ConnecsiModel()
            data = connecsiObj.delete_message_from_messages(message_id=message_id,user_id=user_id)
            print(data)
            return {'data': data}
        except Exception as e:
            return {"response": e}, 500




@ns_messages.route('/sentWelcomeEmail/<string:user_id>/<string:user_type>')
class MailBox(Resource):
    @ns_messages.expect(message_form)
    def post(self,user_id,user_type):
        '''Send welcome email message'''
        form_data = request.get_json()
        from_email_id = form_data.get('from_email_id')
        to_email_id = form_data.get('to_email_id')
        date = form_data.get('date')
        subject = form_data.get('subject')
        message = form_data.get('message')

        columns = ['from_email_id', 'to_email_id', 'date', 'subject', 'message','user_id','user_type']
        data = [from_email_id, to_email_id, date, subject, message,user_id,user_type]
        print(data)
        result=0
        try:
            self.send_mail(subject=subject,to_email_id=to_email_id,message=message)
            connecsiObj = ConnecsiModel()
            result = connecsiObj.insert__(table_name='messages',columns=columns,data=data,IGNORE='IGNORE')
            return {'response': 1},200
        except Exception as e:
            print(e)
            return {'response': result},500


    def send_mail(self,subject,to_email_id,message):
        email_content = """
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
           <title>Connecsi</title>
        </head>
        <body>
        """+ message +"""
        </body>
        </html>
        """
        msg = email.message.Message()
        msg['Subject'] = subject
        msg['From'] = 'business@connecsi.com'
        msg['To'] = to_email_id
        password = "Ezadteam"
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(email_content)

        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        # Login Credentials for sending the mail
        server.login(msg['From'], password)
        server.sendmail(msg['From'], [msg['To']], msg.as_string())


@ns_messages.route('/addCampaignIdToMessageId/<string:message_id>/<string:campaign_id>/<string:channel_id>')
class MailBox(Resource):
    def post(self,message_id,campaign_id,channel_id):
        '''add campaign id to message'''
        # columns=['channel_id','message_id','campaign_id','status']
        # data=(channel_id,message_id,campaign_id,'Negotiations')
        connecsiObj = ConnecsiModel()
        result=0
        try:
            # connecsiObj.insert__(table_name='channel_campaign_message',columns=columns,data=data)
            connecsiObj.update_channel_campaign_message(channel_id=channel_id,message_id=message_id,status='Negotiations',campaign_id=campaign_id)

            return {'response': 1}, 200
        except Exception as e:
            print(e)
            return {'response': result}, 500

@ns_messages.route('/getCampaignsAddedToMessage/<string:message_id>')
class MailBox(Resource):
    def get(self,message_id):
        ''' Get campaigns added to message by from message id'''
        try:
            connecsiObj = ConnecsiModel()
            data = connecsiObj.get_campaigns_added_to_message(message_id=str(message_id))
            print(data)
            columns = ['campaign_id','user_id', 'campaign_name', 'from_date', 'to_date', 'budget', 'currency', 'channels',
                       'regions','min_lower_followers','max_upper_followers','files','video_cat_id'
                       ,'target_url','campaign_description','arrangements','kpis','is_classified_post','deleted','campaign_status','channel_id','campaign_id','message_id','status']
            response_list = []
            for item in data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}
        except Exception as e:
            return {"response": e}, 500

@ns_messages.route('/getCampaignsAddedToMessageByMessageIdAndChannelId/<string:message_id>/<string:channel_id>')
class MailBox(Resource):
    def get(self,message_id,channel_id):
        ''' Get campaigns added to message by  message id and channel id'''
        try:
            connecsiObj = ConnecsiModel()
            data = connecsiObj.get_campaigns_added_to_message_by_message_id_and_channel_id(message_id=str(message_id),channel_id=str(channel_id))
            print(data)
            columns = ['campaign_id','user_id', 'campaign_name', 'from_date', 'to_date', 'budget', 'currency', 'channels',
                       'regions','min_lower_followers','max_upper_followers','files','video_cat_id'
                       ,'target_url','campaign_description','arrangements','kpis','is_classified_post','deleted','campaign_status','channel_id','campaign_id','message_id','status']
            response_list = []
            for item in data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}
        except Exception as e:
            return {"response": e}, 500

@ns_messages.route('/getCampaignsAddedToMessageByChannelId/<string:channel_id>')
class MailBox(Resource):
    def get(self,channel_id):
        ''' Get campaigns added to message by channel id'''
        try:
            connecsiObj = ConnecsiModel()
            data = connecsiObj.get_campaigns_added_to_message_by_channel_id(channel_id=str(channel_id))
            print(data)
            columns = ['campaign_id','user_id', 'campaign_name', 'from_date', 'to_date', 'budget', 'currency', 'channels',
                       'regions','min_lower_followers','max_upper_followers','files','video_cat_id'
                       ,'target_url','campaign_description','arrangements','kpis','is_classified_post','deleted','campaign_status','channel_id','campaign_id','message_id','status']
            response_list = []
            for item in data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}
        except Exception as e:
            return {"response": e}, 500





@ns_messages.route('/uploadMessageFiles/<string:message_id>')
class MailBox(Resource):
    def post(self,message_id):
        '''Upload Files for messages id '''
        columns=['user_id','channel_id','message_id','message_files']
        form_data = request.get_json()
        user_id = form_data.get('user_id')
        channel_id = form_data.get('channel_id')
        # message_id = form_data.get('message_id')
        message_files = form_data.get('message_files')

        data=(user_id,channel_id,message_id,message_files)
        connecsiObj = ConnecsiModel()
        result=0
        try:
            connecsiObj.insert__(table_name='user_channel_message_files',columns=columns,data=data)

            return {'response': 1}, 200
        except Exception as e:
            print(e)
            return {'response': result}, 500


    def get(self,message_id):
        ''' Get uploaded message files by message id'''
        try:
            connecsiObj = ConnecsiModel()
            data = connecsiObj.get__(table_name='user_channel_message_files',STAR='*',WHERE='WHERE',compare_column='message_id',compare_value=str(message_id))
            print(data)
            # columns = ['campaign_id','user_id', 'campaign_name', 'from_date', 'to_date', 'budget', 'currency', 'channels',
            #            'regions','min_lower_followers','max_upper_followers','files','video_cat_id'
            #            ,'target_url','campaign_description','arrangements','kpis','is_classified_post','channel_id','campaign_id','message_id','status']
            columns = ['user_id', 'channel_id', 'message_id', 'message_files']
            response_list = []
            for item in data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}
        except Exception as e:
            return {"response": e}, 500



@ns_messages.route('/uploadMessageAgreements/<string:message_id>')
class MailBox(Resource):
    def post(self,message_id):
        '''Upload Agreements for messages id '''
        columns=['user_id','channel_id','message_id','message_agreements']
        form_data = request.get_json()
        user_id = form_data.get('user_id')
        channel_id = form_data.get('channel_id')
        # message_id = form_data.get('message_id')
        message_agreements = form_data.get('message_agreements')

        data=(user_id,channel_id,message_id,message_agreements)
        connecsiObj = ConnecsiModel()
        result=0
        try:
            connecsiObj.insert__(table_name='user_channel_message_agreements',columns=columns,data=data)
            result=1
            return {'response': result}, 200
        except Exception as e:
            print(e)
            return {'response': result}, 500


    def get(self,message_id):
        ''' Get uploaded message Agreements by message id'''
        try:
            connecsiObj = ConnecsiModel()
            data = connecsiObj.get__(table_name='user_channel_message_agreements',STAR='*',WHERE='WHERE',compare_column='message_id',compare_value=str(message_id))
            print(data)
            # columns = ['campaign_id','user_id', 'campaign_name', 'from_date', 'to_date', 'budget', 'currency', 'channels',
            #            'regions','min_lower_followers','max_upper_followers','files','video_cat_id'
            #            ,'target_url','campaign_description','arrangements','kpis','is_classified_post','channel_id','campaign_id','message_id','status']
            columns = ['user_id', 'channel_id', 'message_id', 'message_agreements']
            response_list = []
            for item in data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}
        except Exception as e:
            return {"response": e}, 500





@ns_messages.route('/ForgotPassword/<string:email_id>')
class MailBox(Resource):
    def post(self,email_id):
        '''Send password to given email id'''
        new_password=''
        connecsiObj = ConnecsiModel()

        new_password = email_id+'_111'
        password_sha = sha256_crypt.encrypt(str(new_password))
        # columns = ['password']
        # data = (password_sha)
        try:
            # connecsiObj.update__(table_name='users_brands', columns=columns, WHERE='WHERE', data=data,
            #                      compare_column='email_id', compare_value=str(email_id))
            connecsiObj.update_users_brands_password(email_id=email_id,password=password_sha)

        except Exception as e:
            print(e)
        to_email_id = email_id
        subject = 'Your Password for Connecsi Admin'
        message = 'Your Password for Connecsi is '+ new_password + ', You can now login with this new temporary password and then change it'
        try:
            self.send_mail(subject=subject,to_email_id=to_email_id,message=message)
            result=1
            return {'response': result},200
        except Exception as e:
            print(e)
            result=0
            return {'response': result},500


    def send_mail(self,subject,to_email_id,message):
        email_content = '<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>Connecsi</title></head><body>' \
                        +message+ \
                        '</body></html>'
        msg = email.message.Message()
        msg['Subject'] = subject
        msg['From'] = 'business@connecsi.com'
        msg['To'] = to_email_id
        password = "Ezadteam"
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(email_content)

        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        # Login Credentials for sending the mail
        server.login(msg['From'], password)
        server.sendmail(msg['From'], [msg['To']], msg.as_string())



@ns_messages.route('/getMessagesByToEmailId/<string:to_email_id>')
class MailBox(Resource):
    def get(self,to_email_id):
        ''' Get all messages by to_email_id'''
        try:
            connecsiObj = ConnecsiModel()
            data = connecsiObj.get_messages_by_to_email_id(to_email_id=str(to_email_id))
            print(data)
            columns = ['message_id','user_id', 'channel_id', 'from_email_id', 'to_email_id','date','subject','message']
            response_list = []
            for item in data:
                dict_temp = dict(zip(columns, item))
                response_list.append(dict_temp)
            return {'data': response_list}
        except Exception as e:
            return {"response": e}, 500


@ns_messages.route('/update_and_send_email_youtube/<channel_id>/<message_id>/<email_id>/<subject>/<message>')
class MailBox(Resource):
    def get(self,channel_id,message_id,email_id,subject,message):
        ''' update and send email of youtube channel'''
        try:
            self.send_mail(subject=subject,to_email_id=email_id)
        except Exception as e:
            print(e)
            pass
        try:
            connecsiObj = ConnecsiModel()
            res = connecsiObj.update_youtube_email(channel_id=channel_id,business_email=email_id)
            res = connecsiObj.update_messages_to_email_id(message_id=message_id,to_email_id=email_id)
            return {'data': res},200
        except Exception as e:
            return {"response": e}, 500


    def send_mail(self,subject,to_email_id):
        email_content = """
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
           <title>Connecsi</title>
        </head>
        <body>
        Connecsi User wants to connect with you...
        Please login to view the full message...
        <a href="#">Login</a>
        </body>
        </html>
        """
        msg = email.message.Message()
        msg['Subject'] = subject
        msg['From'] = 'business@connecsi.com'
        msg['To'] = to_email_id
        password = "Ezadteam"
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(email_content)

        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        # Login Credentials for sending the mail
        server.login(msg['From'], password)
        server.sendmail(msg['From'], [msg['To']], msg.as_string())


@ns_messages.route('/update_message_as_read/<message_id>')
class MailBox(Resource):
    def get(self,message_id):
        ''' update message as read'''
        try:
            connecsiObj = ConnecsiModel()
            res = connecsiObj.mark_message_as_read(message_id=message_id)
            return {'data': res},200
        except Exception as e:
            return {"response": e}, 500

@ns_messages.route('/update_conversation_as_read/<conv_id>')
class MailBox(Resource):
    def get(self,conv_id):
        ''' update conversation as read'''
        try:
            connecsiObj = ConnecsiModel()
            res = connecsiObj.mark_conversation_as_read(conv_id=conv_id)
            return {'data': res},200
        except Exception as e:
            return {"response": e}, 500


@ns_messages.route('/update_message_as_unread/<message_id>')
class MailBox(Resource):
    def get(self,message_id):
        ''' update message as unread'''
        try:
            connecsiObj = ConnecsiModel()
            res = connecsiObj.mark_message_as_unread(message_id=message_id)
            return {'data': res},200
        except Exception as e:
            return {"response": e}, 500


@ns_messages.route('/getAllUnreadMessages/<string:to_email_id>')
class MailBox(Resource):
    def get(self,to_email_id):
        ''' Get all unread messages by to_email_id'''
        try:
            connecsiObj = ConnecsiModel()
            data = connecsiObj.get_all_unread_messages_by_to_email_id(to_email_id=str(to_email_id))
            print(data)
            # columns = ['conv_id','message_id', 'date', 'from_email_id', 'to_email_id', 'subject', 'message', 'user_id',
            #            'user_type','deleted','deleted_from_bin','deleted_from_user_id','deleted_from_bin_user_id','read']
            # columns=['total_unread_messages']
            # response_list = []
            # for item in data:
            #     dict_temp = dict(zip(columns, item))
            #     response_list.append(dict_temp)
            return data
        except Exception as e:
            return {"error": e}, 500


@ns_messages.route('/inbox/<string:email_id>')
class MailBox(Resource):
    def get(self,email_id):
        data=[]
        data_dict = {}
        data.append(data_dict)
        print(email_id)
        connecsiObj = ConnecsiModel()
        res = connecsiObj.get_messages_by_user_id_and_user_type(email_id=str(email_id))
        print(res)
        # columns = ['message_id', 'from_email_id', 'to_email_id', 'channel_id', 'date', 'subject', 'message',
        #            'user_id','user_type','deleted', 'deleted_from_bin', 'deleted_from_user_id',     'deleted_from_bin_user_id', 'read']
        # response_list = []
        # for item in data_tuple:
        #     dict_temp = dict(zip(columns, item))
        #     response_list.append(dict_temp)
        return {'data': res}
