#!/usr/bin/python
#coding=utf8

import MySQLdb
from flask import Flask, request, Response,jsonify
from werkzeug.datastructures import Headers
app = Flask(__name__)

#@app.route('/')
#def hello_world():
#    return 'Hello, World!\n'
@app.route('/', methods=['POST'])
def eden2meta():
        dalgroup     = "'" +  request.form.get('dalgroup') + "'"
        dalgrouptype = request.form.get('dalgrouptype')
        ip           = "'" +  request.form.get('ip') + "'"
        db           = "'" +  request.form.get('db') + "'"
        port         = request.form.get('port')
        pjowner      = "'" +  request.form.get('pjowner') + "'"
        email        = "'" +  request.form.get('email') + "'"
        slack        = "'" +  request.form.get('slack') + "'"
        sms          = "'" +  request.form.get('sms') + "'"
        ping         = "'" +  request.form.get('ping') + "'"
        try:
                conn= MySQLdb.connect(
                        host='192.168.67.36',
                        port = 3307,
                        user='da_user',
                        passwd='root@123',
                        db ='autoreview',
                        )
                cur = conn.cursor()
                sqli="select count(*) from autoreview_alert_info where dalgroup = %s"
                cur.execute(sqli, (dalgroup))
                results=cur.fetchall()
                for row in results:
                    count = row[0]
                if count == 0:
                    sqli="insert into autoreview_alert_info(dalgroup,dalgrouptype, ip, db, port, project_owner, email, slack, sms, ping) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cur.execute(sqli, (dalgroup, dalgrouptype,ip, db, port,  pjowner, email, slack, sms, ping))
                else:
                   sqli="update autoreview_alert_info set dalgrouptype = %s, ip = %s, db = %s, port = %s, project_owner = %s, email= %s, slack = %s, sms = %s, ping =%s , update_at = CURRENT_TIMESTAMP where dalgroup = %s"
                   cur.execute(sqli, (dalgrouptype,ip, db, port,  pjowner, email, slack, sms, ping, dalgroup))
                cur.close()
                conn.commit()
                conn.close()
        except MySQLdb.Error,e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return responseto(data='true')       

def responseto(message=None, error=None, data=None, **kwargs):
    """ 封装 json 响应
    """
    # 如果提供了 data，那么不理任何其他参数，直接响应 data
    if not data:
        data = kwargs
        data['error'] = error
        if message:
            # 除非显示提供 error 的值，否则默认为 True
            # 意思是提供了 message 就代表有 error
            data['message'] = message
            if error is None:
                data['error'] = True
        else:
            # 除非显示提供 error 的值，否则默认为 False
            # 意思是没有提供 message 就代表没有 error
            if error is None:
                data['error'] = False
    # if not isinstance(data, dict):
    #     data = {'error':True, 'message':'data 必须是一个 dict！'}
    resp = jsonify(data)
    # 跨域设置
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9999)
