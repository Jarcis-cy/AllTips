# coding:utf-8
'''
@File   :   tips.py
@Time   :   2021/12/26
@Author :   Jarcis-cy
@Link   :   https://github.com/Jarcis-cy/AllTips
'''
import sqlite3
import base64
import argparse
import time

def banner():
    print(r'''
 _______  _        _    __________________ _______  _______ 
(  ___  )( \      ( \   \__   __/\__   __/(  ____ )(  ____ \
| (   ) || (      | (      ) (      ) (   | (    )|| (    \/
| (___) || |      | |      | |      | |   | (____)|| (_____ 
|  ___  || |      | |      | |      | |   |  _____)(_____  )
| (   ) || |      | |      | |      | |   | (            ) |
| )   ( || (____/\| (____/\| |   ___) (___| )      /\____) |
|/     \|(_______/(_______/)_(   \_______/|/       \_______)  version:0.1
        ''')

parser = argparse.ArgumentParser(usage='python tips.py --add --mark "jarcis" -i "https://github.com/Jarcis-cy"')
create_group = parser.add_argument_group(title='Create Options')
create_group.add_argument('--create', action="store_true", help='Input the parameters into creating mode')

add_group = parser.add_argument_group(title='Add Options')
create_group.add_argument('--add', action="store_true", help='Input the parameters into the add mode')
add_group.add_argument('-i', type=str, help='Please input you want to insert data')
add_group.add_argument('-f', type=str, help='Please input you want to insert the data files')

delete_group = parser.add_argument_group(title='Delete Options')
delete_group.add_argument('--delete', action="store_true", help='Input the parameters into the deleted model, add - id can delete the corresponding data')

show_group = parser.add_argument_group(title='Show Options')
show_group.add_argument('--show', action="store_true", help='Input the parameters into the view mode')
show_group.add_argument('-t', type=str, help='Input to the content of the query')
show_group.add_argument('-l', action="store_true", help='View all marks')

change_group = parser.add_argument_group(title='Change Options')
change_group.add_argument('--change', action="store_true", help='Input the parameters into the modified model')

share_group = parser.add_argument_group(title='Share Options')
share_group.add_argument('--mark', type=str, help='Data retrieval')
share_group.add_argument('-c', type=str, default='tips.db', help='Please enter a name for you to open the database, the default for the tips.db')
share_group.add_argument('--id', type=int, help='The id of the tips')
share_group.add_argument('-T', type=str, default='ALLTIPS', help='Please input the name of the table, the default alltips')

args = parser.parse_args()

def create_table(cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS {} 
    (   id INTEGER PRIMARY KEY AUTOINCREMENT,
        mark               TEXT  NOT NULL,
        content            TEXT  NOT NULL,
        create_data        TEXT  NOT NULL,
        update_data        TEXT  NOT NULL)'''.format(args.T))
    print("Initialization data table")

def main():
    banner()
    conn = sqlite3.connect(args.c)
    print("\nOpen the database successfully\n\n")
    c = conn.cursor()
    if args.create and args.delete and args.show and args.change and args.add:
        print("Please select a pattern")

    elif args.create and not (args.delete or args.show or args.change or args.add):
        create_table(c)

    elif args.delete and not (args.create or args.show or args.change or args.add):
        if args.id:
            c.execute("DELETE FROM {} WHERE id={}".format(args.T,args.id))
            print("Delete success!")
        else:
            print("Please enter the ID to delete")

    elif args.show and not (args.delete or args.create or args.change or args.add):
        if args.mark:
            data = c.execute("SELECT * FROM {} WHERE mark=={}".format(args.T,args.mark))
            if len(data.fetchall()) == 0:
                print("Not query to the data")
            else:
                for i in data:
                    content = base64.decodebytes(bytes(i[2],encoding="utf-8")).decode()
                    print("-"*50)
                    print("ID:",i[0])
                    print("Mark:",i[1])
                    print("Content:")
                    print("*"*35)
                    print(content)
                    print("*"*35)
                    print("Update_time:",i[3])
                    print("Create_time:",i[4])
        elif args.l:
            data = c.execute("SELECT distinct mark FROM {}".format(args.T))
            print("Marks:")
            for i in data:
                print(i[0])
        else:
            print("Please input to query mark")

    elif args.change and not (args.delete or args.show or args.create or args.add):
        if args.id and args.i:
            data = args.i
            en_data = data.encode()
            base64_data = str(base64.b64encode(en_data),encoding="utf-8")
            stime = time.asctime()
            c.execute("UPDATE {} SET content='{}',update_data='{}' WHERE id=={}".format(args.T,base64_data,stime,args.id))
            conn.commit()
            conn.close()
            print("Update success!")
        elif args.id and args.f:
            with open(args.f,"rb") as f:
                data = f.read()
                base64_data = str(base64.b64encode(data),encoding="utf-8")
                stime = time.asctime()
                c.execute("UPDATE {} SET content='{}',update_data='{}' WHERE id=={}".format(args.T,base64_data,stime,args.id))
                conn.commit()
                conn.close()
                print("Update success！")
        else:
            print("Please enter the need to modify the id and content")

    elif args.add and not (args.delete or args.show or args.create or args.change):
        if args.mark and args.i:
            data = args.i
            mark = args.mark
            en_data = data.encode()
            base64_data = str(base64.b64encode(en_data),encoding="utf-8")
            stime = time.asctime()
            c.execute("INSERT INTO {} (mark,content,create_data,update_data) VALUES ('{}','{}','{}','{}')".format(args.T,mark,base64_data,stime,stime))
            conn.commit()
            conn.close()
            print("Data into success！")
        elif args.mark and args.f:
            mark = args.mark
            with open(args.f,"rb") as f:
                data = f.read()
                base64_data = str(base64.b64encode(data),encoding="utf-8")
                stime = time.asctime()
                c.execute("INSERT INTO {} (mark,content,create_data,update_data) VALUES ('{}','{}','{}','{}')".format(args.T,mark,base64_data,stime,stime))
                conn.commit()
                conn.close()
                print("Data into success！")
        else:
            print("Lack the necessary parameters")

    else:
        print("Please select a pattern")

main()

