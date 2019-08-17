# -*- coding:UTF-8 -*-
# Time 2019年8月17日19:03:27
# Author sxz799
import pymysql
import configparser
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')
cf = configparser.ConfigParser()
cf.read("./config.ini")
secs = cf.sections()
HOST = cf.get("mysql-datebase", "HOST")
USER = cf.get("mysql-datebase", "USER")
PASSWD = cf.get("mysql-datebase", "PASSWD")
DB = cf.get("mysql-datebase", "DB")
CHARGE_NUM = cf.getint("mysql-datebase", "CHARGE_NUM")
user_account = cf.items("USER_ACCOUNT")
temp=len(user_account)
for i in range(0,temp):
 db = pymysql.connect(HOST,USER,PASSWD,DB)
 cursor = db.cursor()
 cursor.execute("SELECT silver_coin FROM account WHERE account = %s" ,user_account[i][1])
 before_coin = cursor.fetchall()[0][0]
 after_coin=CHARGE_NUM+before_coin
 localtime=time.asctime( time.localtime(time.time()) )
 if after_coin<2000000000:
  cursor.execute("UPDATE account SET silver_coin = %s, CHECKSUM = upper(CAST(md5(concat(CAST(account AS char CHARACTER SET utf8),CAST(PASSWORD AS char CHARACTER SET utf8),CAST(LPAD(CONV(privilege, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(blocked_time AS char CHARACTER SET utf8),CAST(LPAD(CONV(gold_coin, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(LPAD(CONV(silver_coin, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(coin_password AS char CHARACTER SET utf8),CAST(unlock_coin_password_time AS char CHARACTER SET utf8),CAST(trade_lock_time AS char CHARACTER SET utf8),CAST(permit_ip AS char CHARACTER SET utf8),'ABCDEF')) AS CHAR))WHERE account = %s ;" ,(after_coin,user_account[i][1]))
  db.commit()
  db.close()
  str="%s帐号%s成功充值%s银元宝，当前银元宝为%s\n"%(localtime,user_account[i][1],CHARGE_NUM,after_coin)
  f= open("chargelog.txt","a")
  f.write(str)
  f.close()
 else:
  db.close()
  str="%s帐号%s成功失败，当前银元宝为%s\n"%(localtime,user_account[i][1],before_coin)
  f= open("chargelog.txt","a")
  f.write(str)
  f.close()
  
