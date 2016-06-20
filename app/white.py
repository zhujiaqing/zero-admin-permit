#!/usr/bin/env python
# -*- coding:utf8 -*-

"""
author: jesse
description: 用于管理入口机器的白名单IP限制

run host
wan ip: 122.144.167.76 / 122.144.167.81
lan ip: 10.10.10.109   / 10.10.10.106
port: 10030

/usr/bin/htpasswd
/usr/local/nginx/sbin/nginx

"""

import web
import json
import time
import os
import sys
import redis
import urllib

reload(sys)
sys.setdefaultencoding('UTF-8')  # @UndefinedVariable

urls = (
    '/white/agency?', 'agency',
    '/white/view?', 'view',
    '/white/home?', 'home',
    '/.*', 'home',
    )
app = web.application(urls, locals())

class White:
    '''
    Redis key 说明
    HSET H:phonenumber phonenumber username，预申请通过的手机号码和用户名白名单
    HSET S:ip:%s phonenumber username，申请有效IP映射手机号码和用户名，有效时间 3*24*60*60
    H:admin:%s author,backend,memo 后台信息存储
    '''
    
    _HOST = '122.144.167.76'
    _ADMIN_DENY_FILE = '/usr/local/nginx/conf/admin/deny/dynamic.white.list'
    _TIMEDELTA = 3 * 24 * 60 * 60
    
    _KEY_HSET_PHONENUMBER = 'H:phonenumber'
    _KEY_SET_IP = 'S:ip:%s'
    _KEY_HSET_ADMIN = 'H:admin:%s'
    
    def __init__(self):
        self.r = redis.Redis(host='ops.redis.youja.cn', port=6610, db=15)
    
    def get_base_html(self, body):
        web.header('Content-Type', 'text/html; charset=utf-8', unique=True) 
        web.header('Cache-Control', 'no-Cache') 
        return '<HTML><HEAD><TITLE>友加后台访问权限自助申请</TITLE>' \
        '<link rel="stylesheet" href="//cdn.bootcss.com/bootstrap/3.3.5/css/bootstrap.min.css">' \
        '<link rel="stylesheet" href="//cdn.bootcss.com/bootstrap/3.3.5/css/bootstrap-theme.min.css">' \
        '<script src="//cdn.bootcss.com/jquery/1.11.3/jquery.min.js"></script>' \
        '<script src="//cdn.bootcss.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>' \
        '</HEAD><BODY>%s</BODY></HTML>' % body
    
    def get_remote_ip(self):
        ctxInfo = web.ctx
        ctxEnv = ctxInfo.get('env')
        ip = ctxEnv.get('HTTP_X_REAL_IP', ctxEnv.get('HTTP_X_FORWARDED_FOR', ctxEnv.get('REMOTE_ADDR', ctxInfo['ip'])))
        return ip
    
    def check_exists(self, ip):
        return self.r.exists(self._KEY_SET_IP % ip)
    
    def check_validate(self, data):
        username = self.r.hget(self._KEY_HSET_PHONENUMBER, data.get('phonenumber'))
        return True if username == data.get('username') else False
    
    def refresh(self):  # 加载生效
        with open(self._ADMIN_DENY_FILE, 'w') as f:
            for key in self.r.keys('S:ip:*'):
                f.write('allow %s;\n' % key.split(':')[-1])
            f.close()
        os.system('/usr/local/nginx/sbin/nginx -s reload')
    
    def reload_nginx(self, thread_name, delay):
        while True:
            self.refresh()
            time.sleep(delay)
    
    def send_sms(self, phone, content):
        try:
            params = {'phone':phone, 'content':content}
            data = urllib.urlencode(params)
            smsUrl = 'http://yw.admin.youja.cn/sms'
            urllib.urlopen(smsUrl, data=data)
        except:pass
    
    def add(self, data):
        self.r.setex(self._KEY_SET_IP % data.get('ip'), data.get('phonenumber'), self._TIMEDELTA)
        self.refresh()
        self.send_sms(data.get('phonenumber'), '你正在登录后台确认是否是本人，若不是本人请及时联系管理员。')

    def get_admin_list(self):
        admin_list = []
        for key in self.r.keys('H:admin:*'):
            admin = self.r.hgetall(key)
            admin['domain'] = key.split(':')[-1]
            admin_list.append(admin)
        return admin_list

    def get_permit_list(self):
        permit_list = []
        for key in self.r.keys('S:ip:*'):
            permit = {}
            permit['phonenumber'] = self.r.get(key)
            permit['ip'] = key.split(':')[-1]
            permit['ttl'] = self.r.ttl(key)
            permit['username'] = self.r.hget(self._KEY_HSET_PHONENUMBER, permit['phonenumber'])
            permit_list.append(permit)
        return permit_list

white = White()

################################## Controller ##################################

class agency:
    def POST(self):
        data = web.input()
        if white.check_validate(data):
            white.add(data)
            web.seeother('/white/view?ip=%s' % data.get('ip'))
        else:
            web.seeother('/white/home?ret=1&info=no validate')

class view:
    def GET(self):
        if white.check_exists(ip=web.input().get('ip', None)):
            
            t_admin = '<tr><td>#Host</td><td>域名</td><td>#</td><td>后端</td><td>提供者</td><td>描述</td></tr>'
            for admin in white.get_admin_list():
                t_admin += '<tr><td>%s</td><td>%s</td><td>#</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
                                                                                     white._HOST,
                                                                                     admin.get('domain', ''),
                                                                                     admin.get('backend', ''),
                                                                                     admin.get('author', ''),
                                                                                     admin.get('memo', '')
                                                                                     )
            
            t_ip = '<tr><td>IP</td><td>还剩下有效时间/s</td><td>申请时间/YYYY-mm-dd HH:MM</td><td>手机号码</td><td>用户名</td></tr>'
            for permit in white.get_permit_list():
                t_ip += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
                                                                             permit.get('ip', ''),
                                                                             permit.get('ttl', ''),
                                                                             time.strftime("%Y-%m-%d %H:%M",
                                                                                time.localtime(
                                                                                     int(time.time() - (white._TIMEDELTA - permit.get('ttl', '')))
                                                                                )),
                                                                             permit.get('phonenumber', ''),
                                                                             permit.get('username', '')
                                                                             )
            
            t_tip = '<p>注意事项：</p><ul class="list-group">' \
                '<li class="list-group-item">Windows 系统更改hosts文件 C:\Windows\System32\drivers\etc\hosts</li>' \
                '<li class="list-group-item">Mac/Linux 系统更改hosts文件 /etc/hosts</li>' \
                '<li class="list-group-item">家庭IP非固定会经常变更</li>' \
                '<li class="list-group-item">每次IP申请有效期为3天</li>' \
                '</ul></div>' 
            
            body = '<div STYLE="padding: 20 100">' \
            '<div class="panel panel-default">' \
            '<div class="panel-heading"><h1>友加后台访问权限自助申请</h1></div>' \
            '<div class="panel-body">已经授权的IP列表</div>' \
            '<table class="table">%s</table>' \
            '<div class="panel-body">%s</div>' \
            '<div class="panel-body">后台列表 (若公网没有解析需要拷贝下面的内容粘贴至hosts文件)</div>' \
            '<table class="table">%s</table>' \
            '</div></div>' % (t_ip, str(t_tip), t_admin)
            
            return white.get_base_html(body)
        else:
            web.seeother('/white/home?ret=1&info=not exits')

class home:
    def GET(self):
        msg = ''
        data = web.input()
        ret = data.get('ret', None)
        info = data.get('info', '')
        if '0' == ret:
            msg = '<div class="alert alert-success" role="alert">%s</div>' % info
        elif '1' == ret:
            msg = '<div class="alert alert-danger" role="alert">%s</div>' % info
            
        body = '<DIV STYLE="TEXT-ALIGN: CENTER;padding: 20 100">%s' \
        '<DIV class="well well-sm">' \
        '<h1>友加后台访问权限自助申请</h1>' \
        '<FORM METHOD="POST" ACTION="/white/agency" class="form-inline">' \
        '<INPUT class="form-control" placeholder="你的家庭外网IP" type="text" value="%s" name="ip" required pattern="([0-9]{1,3}\.){3}[0-9]{1,3}">' \
        '<INPUT class="form-control" placeholder="你的预留手机号码" type="num" name="phonenumber" autofocus required pattern="1[0-9]{10}">' \
        '<INPUT class="form-control" placeholder="你的预留用户名" type="text" name="username" required>' \
        '<button type="submit" class="btn btn-default">申请</button>' \
        '</FORM></DIV></DIV>' % (msg, white.get_remote_ip())
        
        return white.get_base_html(body)

if __name__ == "__main__":
    import thread
    thread.start_new_thread(white.reload_nginx, ('Thread_reload_nginx', 1 * 24 * 60 * 60))

    app.run()

    print '\nCompleted\n'
    
    
