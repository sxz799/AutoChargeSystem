# -*- coding:UTF-8 -*-
# @Time 2019年8月17日19:03:27
# @Author sxz799
import pymysql
import configparser
import time
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf8')
def charge():
 localtime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
 str="\n任何使用问题请联系QQ:1102041547 程序当前版本V1.4\n%s 充值详情：\n"%(localtime)
 f= open("chargelog.txt","a")
 f.write(str)
 cf = configparser.ConfigParser()
 cf.read("./config.ini") #配置文件获得数据库信息和账号信息
 secs = cf.sections()
 HOST = cf.get("mysql-datebase", "HOST")
 USER = cf.get("mysql-datebase", "USER")
 PASSWD = cf.get("mysql-datebase", "PASSWD")
 DB = cf.get("mysql-datebase", "DB")
 CHARGE_NUM = cf.getint("mysql-datebase", "CHARGE_NUM")
 isFullGold = cf.getint("mysql-datebase", "isFullGold")
 user_account = cf.items("USER_ACCOUNT")
 temp=len(user_account)
 db = pymysql.connect(HOST,USER,PASSWD,DB) #链接数据库
 cursor = db.cursor()
 for i in range(0,temp):
  cursor.execute("SELECT IFNULL((SELECT '1' from dl_adb_all.account where account = %s limit 1),'NULL')",user_account[i][1]) #判断帐号是否存在
  isNull = cursor.fetchall()[0][0]
  if isNull!='NULL':
   cursor.execute("SELECT silver_coin FROM account WHERE account = %s" ,user_account[i][1]) #获取当前银元宝
   before_coin = cursor.fetchall()[0][0]
   after_coin=CHARGE_NUM+before_coin #计算增加后的银元宝数量
   if after_coin<2000000000: #判断是否超过20e
    cursor.execute("UPDATE account SET silver_coin = %s, CHECKSUM = upper(CAST(md5(concat(CAST(account AS char CHARACTER SET utf8),CAST(PASSWORD AS char CHARACTER SET utf8),CAST(LPAD(CONV(privilege, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(blocked_time AS char CHARACTER SET utf8),CAST(LPAD(CONV(gold_coin, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(LPAD(CONV(silver_coin, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(coin_password AS char CHARACTER SET utf8),CAST(unlock_coin_password_time AS char CHARACTER SET utf8),CAST(trade_lock_time AS char CHARACTER SET utf8),CAST(permit_ip AS char CHARACTER SET utf8),'ABCDEF')) AS CHAR))WHERE account = %s ;" ,(after_coin,user_account[i][1]))
    if isFullGold==1: #判断是否将金元宝修改为20E
     cursor.execute("UPDATE account SET gold_coin = 2000000000, CHECKSUM = upper(CAST(md5(concat(CAST(account AS char CHARACTER SET utf8),CAST(PASSWORD AS char CHARACTER SET utf8),CAST(LPAD(CONV(privilege, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(blocked_time AS char CHARACTER SET utf8),CAST(LPAD(CONV(gold_coin, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(LPAD(CONV(silver_coin, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(coin_password AS char CHARACTER SET utf8),CAST(unlock_coin_password_time AS char CHARACTER SET utf8),CAST(trade_lock_time AS char CHARACTER SET utf8),CAST(permit_ip AS char CHARACTER SET utf8),'ABCDEF')) AS CHAR))WHERE account = %s ;" ,(user_account[i][1]))
    db.commit()
    str1=" 帐号 %-10s 成功充值%s银元宝，当前银元宝为 %s\n"%(user_account[i][1],CHARGE_NUM,after_coin) #记录充值成功日志
    f.write(str1) 
   else:
    str2=" 帐号 %-10s 充值失败，当前银元宝为 %s\n"%(user_account[i][1],before_coin) #记录因限额20E无法充值
    f.write(str2)
  else:
   str3=" 帐号 %-10s 不存在，请检查配置文件\n"%(user_account[i][1]) #记录帐号不存在日志
   f.write(str3)
   continue
 db.close()
 f.close() 
 time.sleep(60)

def main(H,M):
    #H表示设定的小时，M为设定的分钟
    while True:
        # 判断是否达到设定时间
        while True:
            now = datetime.datetime.now()
            # 到达设定时间，结束内循环，去执行充值
            if now.hour==H and now.minute==M:
              break
            # 不到时间就等45秒之后再次检测
            time.sleep(45)
        # 执行充值
        charge()
cf=configparser.ConfigParser()
cf.read("./config.ini") #配置文件充值时间
secs = cf.sections()
H=cf.getint("charge_time", "H")
M=cf.getint("charge_time", "M")
welstr="欢迎使用自动定时充值系统，有使用问题请联系QQ:1102041547\n您当前设置的充值时间为每天的%d点%d分\n"%(H,M)
f= open("chargelog.txt","w")
f.write(welstr)
f.close()
main(H,M)
charge()

