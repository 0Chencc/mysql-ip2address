from qqwry import QQwry
import pymysql

cz = QQwry()
cz.load_file('qqwry.dat', loadindex=True)


def getipaddress(useridn, ip, table, conn,mode,db):
    cur = conn.cursor(pymysql.cursors.SSDictCursor)

    print(f'select count(*) as iscreate from information_schema.columns where table_name = \'{table}\' and column_name = \'{ip}_address\' and TABLE_SCHEMA={db}')
    cur.execute(
        f'select count(*) as iscreate from information_schema.columns where table_name = \'{table}\' and column_name = \'{ip}_address\' and TABLE_SCHEMA={db}')
    iscreate = cur.fetchall()
    print(iscreate[0])
    if iscreate[0]['iscreate'] == 0:
        cur.execute(f'alter table {table} add {ip}_address varchar(50) default \'\' null after {ip};')
        conn.commit()
    if mode == '1':
        cur.execute(f'select {useridn},{ip} from {table}')
    elif mode =='2':
        cur.execute(f'select {useridn},inet_ntoa({ip}) as {ip} from {table}')
    data = cur.fetchall()
    for i in data:
        if i[f'{ip}'] != '':
            address = ''
            try:
                address = "".join(cz.lookup(i[f'{ip}']))
            except:
                print(i[f'{ip}'])
                pass
            userid = i[f'{useridn}']
            cur.execute(f'update {table} set {ip}_address = \'{address}\' where {useridn} = {userid}')
    conn.commit()
    cur.close()
    conn.close()
    print('finsh!')
