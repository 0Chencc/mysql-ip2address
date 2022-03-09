from qqwry import QQwry
from qqwry import updateQQwry
import pymysql
q = QQwry()
ret = updateQQwry('qqwry.dat')
q.load_file('qqwry.dat', loadindex=True)


def ip2address(useridn, ip, table, conn, mode, db):
    cur = conn.cursor(pymysql.cursors.SSDictCursor)
    print(f'select count(*) as iscreate from information_schema.columns where table_name = \'{table}\' and column_name = \'{ip}_address\' and TABLE_SCHEMA=\'{db}\'')
    cur.execute(
        f'select count(*) as iscreate from information_schema.columns where table_name = \'{table}\' and column_name = \'{ip}_address\' and TABLE_SCHEMA=\'{db}\'')
    create = cur.fetchall()
    print(create[0])
    if create[0]['iscreate'] == 0:
        cur.execute(f'alter table {table} add {ip}_address varchar(50) default \'\' null after {ip};')
        conn.commit()
    if mode == '1':
        cur.execute(f'select {useridn},{ip} from {table}')
    elif mode == '2':
        cur.execute(f'select {useridn},inet_ntoa({ip}) as {ip} from {table}')
    data = cur.fetchall()
    for i in data:
        if i[f'{ip}'] != '':
            try:
                address = "".join(q.lookup(i[f'{ip}']))
                userid = i[f'{useridn}']
                cur.execute(f'update {table} set {ip}_address = \'{address}\' where {useridn} = {userid}')
            except:
                pass
    conn.commit()
    cur.close()
    conn.close()
    print('finsh!')
