from qqwry import QQwry
import pymysql

cz = QQwry()
cz.load_file('qqwry.dat', loadindex=True)


def getipaddress(useridn, ip, table, conn):
    cur = conn.cursor(pymysql.cursors.SSDictCursor)
    cur.execute(f'select count(*) as iscreate from information_schema.columns where table_name = \'{table}\' and column_name = \'{ip}_address\'')
    iscreate = cur.fetchall()
    print(iscreate[0])
    if iscreate[0]['iscreate'] == 0:
        cur.execute(f'alter table {table} add {ip}_address varchar(50) null after {ip};')
        conn.commit()
    cur.execute(f'select {useridn},{ip} from {table}')
    data = cur.fetchall()
    for i in data:
        address = "".join(cz.lookup(i[f'{ip}']))
        userid = i[f'{useridn}']
        cur.execute(f'update {table} set {ip}_address = \'{address}\' where {useridn} = {userid}')
    conn.commit()
    cur.close()
    conn.close()
    print('finsh!')
