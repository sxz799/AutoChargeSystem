# AutoChargeSystem
 author：sxz799
## 使用说明
1.打开config.ini根据提示进行配置,建议使用notepad++
2.将本目录上传到服务器任意目录下
3.赋予777权限
    1.使用命令 chmod 777 -R AutoCharge
    2.使用winscp选中目录右键点击属性 将0755改为0777 勾选下方循环设定组权限
4.切换到AutoCharge目录 
启动  sh start.sh
停止  sh end.sh


## v1.2
添加20E元宝限额判断

##  v1.3
添加金元宝20E选项

##  v1.4
优化配置文件
添加定时执行功能
基本完成最初设计

##  v1.5
优化IO操作
添加异常处理

## v1.6
优化时间延迟

## v1.7
添加帐号分类功能
可为不同类别帐号充值不同数量元宝

## v1.8
修复游标关闭
更新Python3.7支持
