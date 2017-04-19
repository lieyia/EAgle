#!/usr/bin/env python
# -*- coding: utf-8 -*-
# auth :eleme

import MySQLdb
import pika
import json

# ########################## consume ##########################
credentials = pika.PlainCredentials('dal_rmq', 'rXiUJTEE')
#connect to rabbit server
connection = pika.BlockingConnection(pika.ConnectionParameters('10.103.107.62',5672,'dal_rmq_vh',credentials))
channel = connection.channel()
channel.queue_declare(queue='wzg')
i = 0

#define  parse body function
def parseSend(body):
    s = json.loads(body)
    print s
   # print s.keys()
   # print s["originSql"]
   # s["dbName"]
   # print s["ip"]
   # print s["port"]
    port=s["port"]
   # originSql=s["originSql"]
   # print s["dalGroup"]
    sql = '/*--user=root;--password=root123;--host='+s["ip"]+';'+'--port='+str(port)+';'+'--dalgroup='+s["dalGroup"]+';'+'--db='+s["dbName"]+'*/'\
          'inception_magic_start;'\
          'use ' + s["dbName"] + ';' \
           + s["originSql"] +';' \
          'inception_magic_commit;'
    sql = sql.encode('utf-8').decode('latin-1')
    print sql
    try:
        conn=MySQLdb.connect(host='192.168.114.50',user='root',passwd='root',db='wwn',port=6669)
        cur=conn.cursor()
        ret=cur.execute(sql)
        #result=cur.fetchall()
        #num_fields = len(cur.description)
        #field_names = [i[0] for i in cur.description]
        #print field_names
        #for row in result:
        #        print row[0], "¦",row[1],"¦",row[2],"¦",row[3],"¦",row[4],"¦",
        #        row[5],"¦",row[6],"¦",row[7],"¦",row[8],"¦",row[9],"¦",row[10]
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

# define callback function
def callback(ch, method, properties, body):
    global i
    i = i + 1
    print ("count is %d "%(i))
    parseSend(body)


# callback to receive msg

channel.basic_consume(callback,
                      queue='dal_rmq_q1',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()
connection.close()
