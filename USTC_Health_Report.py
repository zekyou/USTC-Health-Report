import requests
import time
import re
import schedule
import smtplib


def main():
    usr = open('usrpara.txt','r')
    for line in usr:
        if '#' in line:
            continue
        try:
            usrpara = line.strip(" \n\t\r").split( )
            '''
            usrname = usrpara[0]
            usrpwd = usrpara[1]
            now_address = usrpara[2]
            now_province = usrpara[3]
            now_city = usrpara[4]
            is_inschool = usrpara[5]
            body_condition = usrpara[6] # 1forNormal;2forPossible;3forConfirm;4forOthers
            now_status =  usrpara[7]  # 1forNormalinSchool;2forHome;3forHomeObs;4forCenterObs;5forHospital;6forOthers
            has_fever = usrpara[8]  # 0forNo;1forYes
            last_touch_sars = usrpara[9]  # 0forNo;1forYes
            '''
            emailaddress = usrpara[10]
        except IndexError:
            continue
        try:
            wltlogin()
        except RuntimeError:
            print('Can not connect to the network')
        for i in range(0, 2):
            try:
                webreport(usrpara)
                flag = 0
                break
            except RuntimeError:
                flag = 1
                print('Can not post '+usrpara[0]+"'s report")
        try:
            sendmail(emailaddress, flag)
        except RuntimeError:
            print('Something error about sending email')


def sendmail(emailaddress, flag):
    from email.mime.text import MIMEText
    from email.header import Header
    mailhost = 'smtp.163.com'
    neteasemail = smtplib.SMTP()
    neteasemail.connect(mailhost,25)
    account = '你的邮箱账号'
    pwd = '你的SMTP登录码'
    neteasemail.login(account,password=pwd)
    sender = '邮箱账号@163.com'
    receiver = emailaddress
    if flag ==0:
        content = 'Congratulation from Robot.'
    else:
        content = 'Sorry, something error today about your report, please contact the admin!'
    message = MIMEText(content,'plain','utf-8')
    subject = 'USTC_HR_Result'
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = '<邮箱账号@163.com>'
    message['To'] = "'<"+emailaddress+">'"
    neteasemail.sendmail(sender, receiver, message.as_string())
    neteasemail.quit()


def timereport():
    schedule.every().day.at("12:00").do(main)
    while True:
        schedule.run_pending()
        time.sleep(200)


def webreport(usrpara):
    session = requests.session()
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/85.0.4183.121 '
            'Safari/537.36'
    }
    loginurl = 'https://passport.ustc.edu.cn/login?service=\
    https%3A%2F%2Fweixine.ustc.edu.cn%2F2020%2Fcaslogin'
    reporturl = 'https://weixine.ustc.edu.cn/2020/daliy_report'
    username = usrpara[0]; password = usrpara[1]
    logindata = {'username': username, 'password': password}
    loginresponse = session.post(loginurl, headers = headers, data = logindata)
    ini_token = re.search(r'<input type="hidden" name="_token" value=".*">', loginresponse.text).group(0)
    token = ini_token[ini_token.find('value="') + len('value="') : -2]
    reportpara = {
        "_token":token,
        "now_address":usrpara[2],#1forCNmainland;2forHk;3forforeign;4forMO;5forTW
        "gps_now_address":"",
        "now_province":usrpara[3],#forAnhui
        "gps_province":"",
        "now_city":usrpara[4],#for Hefei
        "gps_city":"",
        "now_detail":"",
        "is_inschool":usrpara[5],#2forEast;3forSouth;4forMid;5forNorth;6forWest;7forXian;0forOut
        "body_condition":usrpara[6],#1forNormal;2forPossible;3forConfirm;4forOthers
        "body_condition_detail":"",
        "now_status":usrpara[7],#1forNormalinSchool;2forHome;3forHomeObs;4forCenterObs;5forHospital;6forOthers
        "now_status_detail":"",
        "has_fever":usrpara[8],#0forNo;1forYes
        "last_touch_sars":usrpara[9],#0forNo;1forYes
        "last_touch_sars_date":"",
        "last_touch_sars_detail":"",
        "other_detail":""
    }
    reportrespone = session.post(reporturl, headers = headers, data = reportpara)


def wltlogin():
    rawurl = 'http://wlt.ustc.edu.cn/cgi-bin/ip'
    cmd = 'login'
    ip = '你的主机ip'
    set = '%D2%BB%BC%FC%C9%CF%CD%F8'
    name = '你的网络通账号'
    pwd = '你的网络密码'
    wlturl = rawurl+'?'+'cmd='+cmd+'&url=URL&ip='+ip+'&name='+name+'&password='+pwd\
    +'&savepass=on&set='+set
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/85.0.4183.121 '
            'Safari/537.36'
    }
    logindata = requests.post(wlturl, headers = headers)


if __name__ == '__main__':
    timereport()
