import getopt
import sys
import pymysql
from ip import getipaddress
host = 'localhost'
port = 3306
username = 'root'
password = '12345678'
def usage():
    print(
        '-h --help help\n' \
        '-d --database chose database选择库\n' \
        '-a --area chose you want select area要查询的地区\n' \
        '-t --table chose table表名\n' \
        '-i --ipfiled the filed in selected database ip在该表中的字段名\n' \
        '-u --userid the useridfiled in selected database 用户id在该表中的字段名\n' \
        '-m --mode 1.normal 2.ntoa The inet_ntoa function converts an (Ipv4) Internet network address into an ASCII string in Internet standard dotted-decimal format.\n'
        '人话：模式1 正常的ipv4地址查归属地，模式2 将ip戳（就是那一串数字）转化为常规的ip地址'
        )
def connectDB():
    conn = pymysql.connect(host=host,port=port,user=username,password=password)
    return conn

if __name__ == '__main__':
    conn = connectDB()
    db =''
    table = ''
    ip = ''
    useridn = ''
    mode = 0 #0.select sql 1.getipaddress
    try:
        opts,args = getopt.getopt(sys.argv[1:],
                                  '-h-d:-a:-t:-i:-u:-m:',
                                  ['help','database=','area=','table=','ipfiled=','userid=','mode='])
    except getopt.GetoptError as err:
        usage()
        sys.exit()
    for opt,value in opts:
        if opt in ('-h','--help'):
            usage()
            sys.exit()
        elif opt in ('-d','--database'):
            db = value
            conn.select_db(db)
        elif opt in ('-a','--area'):
            area = value
            print(value)
        elif opt in ('-m','--mode'):
            mode=value
        elif opt in ('-t','--table'):
            table = value
        elif opt in ('-u','--userid'):
            useridn = value
        elif opt in ('-i','--ip'):
            ip = value
    # 
    # if mode == '1':
    #     print(f'db is {db},table is {table},mode is {mode},useridn is {useridn},ip is {ip}')
    getipaddress(useridn=useridn,ip=ip,table=table,conn=conn,mode=mode)
