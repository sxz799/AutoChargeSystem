# -*- coding:UTF-8 -*-
# @Time 2019年8月17日19:03:27
# @Author sxz799
import pymysql
import configparser
import time
import datetime
import importlib,sys 
importlib.reload(sys)

def write_log(str,mode): # 写记录日志函数，mode作为操作模式传入
 try:
  f= open("chargelog.txt",mode)
  f.write(str)
 except IOError:
  print ("Error: 没有找到文件或读取文件失败")
 else:
  f.close()
  
def charge_A():  # A级会员充值函数
 localtime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
 cf = configparser.ConfigParser()
 cf.read("./config.ini") # 在配置文件获得数据库信息和账号信息
 secs = cf.sections()
 HOST = cf.get("mysql-datebase", "HOST")
 USER = cf.get("mysql-datebase", "USER")
 PASSWD = cf.get("mysql-datebase", "PASSWD")
 DB = cf.get("mysql-datebase", "DB")
 CHARGE_NUM_A = cf.getint("settings", "CHARGE_NUM_A")
 isFullGold_A = cf.getint("settings", "isFullGold_A")
 user_account_A = cf.items("USER_ACCOUNT_A")
 str="\n%s 当前会员A配置的充值金额为%d,充值详情：\n"%(localtime,CHARGE_NUM_A)
 write_log(str,"a")
 temp=len(user_account_A)
 db = pymysql.connect(HOST,USER,PASSWD,DB) # 连接数据库
 cursor = db.cursor()
 for i in range(0,temp):
  cursor.execute("SELECT IFNULL((SELECT '1' from dl_adb_all.account where account = %s limit 1),'NULL')",user_account_A[i][1]) # 判断帐号是否存在
  isNull = cursor.fetchall()[0][0]
  if isNull!='NULL':
   cursor.execute("SELECT silver_coin FROM account WHERE account = %s" ,user_account_A[i][1]) #获取当前银元宝
   before_coin = cursor.fetchall()[0][0]
   after_coin=CHARGE_NUM_A+before_coin # 计算增加后的银元宝数量
   if after_coin<2000000000: # 判断是否超过20e
    cursor.execute("UPDATE account SET silver_coin = %s, CHECKSUM = upper(CAST(md5(concat(CAST(account AS char CHARACTER SET utf8),CAST(PASSWORD AS char CHARACTER SET utf8),CAST(LPAD(CONV(privilege, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(blocked_time AS char CHARACTER SET utf8),CAST(LPAD(CONV(gold_coin, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(LPAD(CONV(silver_coin, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(coin_password AS char CHARACTER SET utf8),CAST(unlock_coin_password_time AS char CHARACTER SET utf8),CAST(trade_lock_time AS char CHARACTER SET utf8),CAST(permit_ip AS char CHARACTER SET utf8),'ABCDEF')) AS CHAR))WHERE account = %s ;" ,(after_coin,user_account_A[i][1]))
    if isFullGold_A==1: # 判断是否将金元宝修改为20E
     cursor.execute("UPDATE account SET gold_coin = 2000000000, CHECKSUM = upper(CAST(md5(concat(CAST(account AS char CHARACTER SET utf8),CAST(PASSWORD AS char CHARACTER SET utf8),CAST(LPAD(CONV(privilege, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(blocked_time AS char CHARACTER SET utf8),CAST(LPAD(CONV(gold_coin, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(LPAD(CONV(silver_coin, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(coin_password AS char CHARACTER SET utf8),CAST(unlock_coin_password_time AS char CHARACTER SET utf8),CAST(trade_lock_time AS char CHARACTER SET utf8),CAST(permit_ip AS char CHARACTER SET utf8),'ABCDEF')) AS CHAR))WHERE account = %s ;" ,(user_account_A[i][1]))
    db.commit()
    str=" 帐号 %-10s 成功充值%s银元宝，当前银元宝为 %s\n"%(user_account_A[i][1],CHARGE_NUM_A,after_coin) # 写记录充值成功日志
    write_log(str,"a") 
   else:
    str=" 帐号 %-10s 充值失败，当前银元宝为 %s\n"%(user_account_A[i][1],before_coin) # 写记录因限额20E无法充值
    write_log(str,"a")
  else:
   str=" 帐号 %-10s 不存在，请检查配置文件\n"%(user_account_A[i][1]) # 写记录帐号不存在日志
   write_log(str,"a")
   continue
 cursor.close()
 db.close()

def charge_B():  # B级会员充值函数
 localtime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
 cf = configparser.ConfigParser()
 cf.read("./config.ini") # 在配置文件获得数据库信息和账号信息
 secs = cf.sections()
 HOST = cf.get("mysql-datebase", "HOST")
 USER = cf.get("mysql-datebase", "USER")
 PASSWD = cf.get("mysql-datebase", "PASSWD")
 DB = cf.get("mysql-datebase", "DB")
 CHARGE_NUM_B = cf.getint("settings", "CHARGE_NUM_B")
 isFullGold_B = cf.getint("settings", "isFullGold_B")
 user_account_B = cf.items("USER_ACCOUNT_B")
 str="\n%s 当前会员B配置的充值金额为%d,充值详情：\n"%(localtime,CHARGE_NUM_B)
 write_log(str,"a")
 temp=len(user_account_B)
 db = pymysql.connect(HOST,USER,PASSWD,DB) # 连接数据库
 cursor = db.cursor()
 for i in range(0,temp):
  cursor.execute("SELECT IFNULL((SELECT '1' from dl_adb_all.account where account = %s limit 1),'NULL')",user_account_B[i][1]) # 判断帐号是否存在
  isNull = cursor.fetchall()[0][0]
  if isNull!='NULL':
   cursor.execute("SELECT silver_coin FROM account WHERE account = %s" ,user_account_B[i][1]) #获取当前银元宝
   before_coin = cursor.fetchall()[0][0]
   after_coin=CHARGE_NUM_B+before_coin # 计算增加后的银元宝数量
   if after_coin<2000000000: # 判断是否超过20e
    cursor.execute("UPDATE account SET silver_coin = %s, CHECKSUM = upper(CAST(md5(concat(CAST(account AS char CHARACTER SET utf8),CAST(PASSWORD AS char CHARACTER SET utf8),CAST(LPAD(CONV(privilege, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(blocked_time AS char CHARACTER SET utf8),CAST(LPAD(CONV(gold_coin, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(LPAD(CONV(silver_coin, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(coin_password AS char CHARACTER SET utf8),CAST(unlock_coin_password_time AS char CHARACTER SET utf8),CAST(trade_lock_time AS char CHARACTER SET utf8),CAST(permit_ip AS char CHARACTER SET utf8),'ABCDEF')) AS CHAR))WHERE account = %s ;" ,(after_coin,user_account_B[i][1]))
    if isFullGold_B==1: # 判断是否将金元宝修改为20E
     cursor.execute("UPDATE account SET gold_coin = 2000000000, CHECKSUM = upper(CAST(md5(concat(CAST(account AS char CHARACTER SET utf8),CAST(PASSWORD AS char CHARACTER SET utf8),CAST(LPAD(CONV(privilege, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(blocked_time AS char CHARACTER SET utf8),CAST(LPAD(CONV(gold_coin, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(LPAD(CONV(silver_coin, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(coin_password AS char CHARACTER SET utf8),CAST(unlock_coin_password_time AS char CHARACTER SET utf8),CAST(trade_lock_time AS char CHARACTER SET utf8),CAST(permit_ip AS char CHARACTER SET utf8),'ABCDEF')) AS CHAR))WHERE account = %s ;" ,(user_account_B[i][1]))
    db.commit()
    str=" 帐号 %-10s 成功充值%s银元宝，当前银元宝为 %s\n"%(user_account_B[i][1],CHARGE_NUM_B,after_coin) # 写记录充值成功日志
    write_log(str,"a") 
   else:
    str=" 帐号 %-10s 充值失败，当前银元宝为 %s\n"%(user_account_B[i][1],before_coin) # 写记录因限额20E无法充值
    write_log(str,"a")
  else:
   str=" 帐号 %-10s 不存在，请检查配置文件\n"%(user_account_B[i][1]) # 写记录帐号不存在日志
   write_log(str,"a")
   continue
 cursor.close()
 db.close()

def charge_C():  # C级会员充值函数
 localtime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
 cf = configparser.ConfigParser()
 cf.read("./config.ini") # 在配置文件获得数据库信息和账号信息
 secs = cf.sections()
 HOST = cf.get("mysql-datebase", "HOST")
 USER = cf.get("mysql-datebase", "USER")
 PASSWD = cf.get("mysql-datebase", "PASSWD")
 DB = cf.get("mysql-datebase", "DB")
 CHARGE_NUM_C = cf.getint("settings", "CHARGE_NUM_C")
 isFullGold_C = cf.getint("settings", "isFullGold_C")
 user_account_C = cf.items("USER_ACCOUNT_C")
 str="\n%s 当前会员C配置的充值金额为%d,充值详情：\n"%(localtime,CHARGE_NUM_C)
 write_log(str,"a")
 temp=len(user_account_C)
 db = pymysql.connect(HOST,USER,PASSWD,DB) # 连接数据库
 cursor = db.cursor()
 for i in range(0,temp):
  cursor.execute("SELECT IFNULL((SELECT '1' from dl_adb_all.account where account = %s limit 1),'NULL')",user_account_C[i][1]) # 判断帐号是否存在
  isNull = cursor.fetchall()[0][0]
  if isNull!='NULL':
   cursor.execute("SELECT silver_coin FROM account WHERE account = %s" ,user_account_C[i][1]) #获取当前银元宝
   before_coin = cursor.fetchall()[0][0]
   after_coin=CHARGE_NUM_C+before_coin # 计算增加后的银元宝数量
   if after_coin<2000000000: # 判断是否超过20e
    cursor.execute("UPDATE account SET silver_coin = %s, CHECKSUM = upper(CAST(md5(concat(CAST(account AS char CHARACTER SET utf8),CAST(PASSWORD AS char CHARACTER SET utf8),CAST(LPAD(CONV(privilege, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(blocked_time AS char CHARACTER SET utf8),CAST(LPAD(CONV(gold_coin, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(LPAD(CONV(silver_coin, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(coin_password AS char CHARACTER SET utf8),CAST(unlock_coin_password_time AS char CHARACTER SET utf8),CAST(trade_lock_time AS char CHARACTER SET utf8),CAST(permit_ip AS char CHARACTER SET utf8),'ABCDEF')) AS CHAR))WHERE account = %s ;" ,(after_coin,user_account_C[i][1]))
    if isFullGold_C==1: # 判断是否将金元宝修改为20E
     cursor.execute("UPDATE account SET gold_coin = 2000000000, CHECKSUM = upper(CAST(md5(concat(CAST(account AS char CHARACTER SET utf8),CAST(PASSWORD AS char CHARACTER SET utf8),CAST(LPAD(CONV(privilege, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(blocked_time AS char CHARACTER SET utf8),CAST(LPAD(CONV(gold_coin, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(LPAD(CONV(silver_coin, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(coin_password AS char CHARACTER SET utf8),CAST(unlock_coin_password_time AS char CHARACTER SET utf8),CAST(trade_lock_time AS char CHARACTER SET utf8),CAST(permit_ip AS char CHARACTER SET utf8),'ABCDEF')) AS CHAR))WHERE account = %s ;" ,(user_account_C[i][1]))
    db.commit()
    str=" 帐号 %-10s 成功充值%s银元宝，当前银元宝为 %s\n"%(user_account_C[i][1],CHARGE_NUM_C,after_coin) # 写记录充值成功日志
    write_log(str,"a") 
   else:
    str=" 帐号 %-10s 充值失败，当前银元宝为 %s\n"%(user_account_C[i][1],before_coin) # 写记录因限额20E无法充值
    write_log(str,"a")
  else:
   str=" 帐号 %-10s 不存在，请检查配置文件\n"%(user_account_C[i][1]) # 写记录帐号不存在日志
   write_log(str,"a")
   continue
 cursor.close()
 db.close()

def DoTime(H,M): #定时函数 H表示设定的小时，M为设定的分钟
    while True: 
        while True: # 判断是否达到设定时间
            now = datetime.datetime.now()      
            if now.hour==H and now.minute==M: # 到达设定时间，结束内循环，去执行充值
              break
            time.sleep(50) # 不到时间就等50秒之后再次检测
        charge_A()  # 执行充值函数
        charge_B()
        charge_C()
        time.sleep(60)
def start():
 cf=configparser.ConfigParser()
 cf.read("./config.ini") #配置文件充值时间
 secs = cf.sections()
 H=cf.getint("charge_time", "H")
 M=cf.getint("charge_time", "M")
 welstr="欢迎使用自动定时充值系统，当前程序版本：v1.8\n有使用问题请联系青丝QQ:1102041547\n青丝接1.60、1.63架设，登录器制作，etc修改定制\n当前配置的充值时间为每天%d点%d分\n程序启动后可随时修改除时间外的配置信息\n"%(H,M)
 write_log(welstr,"a")  #写记录日志
 DoTime(H,M)
 
start()