#!/bin/bash
DBNAME="dl_adb_all"
USERNAME="root"
PASSWORD="BHD2WjrBnT8sKAKj"
COIN_NUM="100"
user_account=("test0816" "1008611" "1105389211qq")  
length=`expr ${#user_account[@]} - 1`
for i in $(seq 0 $length)
do
BEFORE_COIN=`mysql  -u${USERNAME} -p${PASSWORD} --skip-column-names -e "use ${DBNAME} ;
SELECT silver_coin FROM account WHERE account = '${user_account[i]}';"`
AFTER_COIN=`expr $BEFORE_COIN + $COIN_NUM`
if [ $AFTER_COIN -ge 0 ] && [ $AFTER_COIN -le 2000000000 ] 
then mysql -u${USERNAME} -p${PASSWORD} -e "use ${DBNAME};
UPDATE account SET silver_coin = silver_coin + $COIN_NUM, CHECKSUM = upper(CAST(md5(concat(CAST(account AS char CHARACTER SET utf8),CAST(PASSWORD AS char CHARACTER SET utf8),CAST(LPAD(CONV(privilege, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(blocked_time AS char CHARACTER SET utf8),CAST(LPAD(CONV(gold_coin, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(LPAD(CONV(silver_coin, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(coin_password AS char CHARACTER SET utf8),CAST(unlock_coin_password_time AS char CHARACTER SET utf8),CAST(trade_lock_time AS char CHARACTER SET utf8),CAST(permit_ip AS char CHARACTER SET utf8),'ABCDEF')) AS CHAR))WHERE account = '${user_account[i]}';
UPDATE account SET gold_coin = 2000000000, CHECKSUM = upper(CAST(md5(concat(CAST(account AS char CHARACTER SET utf8),CAST(PASSWORD AS char CHARACTER SET utf8),CAST(LPAD(CONV(privilege, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(blocked_time AS char CHARACTER SET utf8),CAST(LPAD(CONV(gold_coin, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(LPAD(CONV(silver_coin, 10, 16), 8, 0) AS char CHARACTER SET utf8),CAST(coin_password AS char CHARACTER SET utf8),CAST(unlock_coin_password_time AS char CHARACTER SET utf8),CAST(trade_lock_time AS char CHARACTER SET utf8),CAST(permit_ip AS char CHARACTER SET utf8),'ABCDEF')) AS CHAR))WHERE account = '${user_account[i]}';"
sleep 1
echo "$(date +"%Y-%m-%d %H:%M:%S") 成功为帐号 ${user_account[i]} 充值$COIN_NUM银元宝,您现在银元宝数量为$AFTER_COIN" >> /root/charge_accs.log
else echo "$(date +"%Y-%m-%d %H:%M:%S") 帐号 ${user_account[i]} 充值失败, 你现在已拥有$BEFORE_COIN银元宝" >> /root/charge_accs.log
fi
done
