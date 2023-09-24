from __future__ import unicode_literals

import json

from flask import redirect
from flask import render_template, url_for, session, jsonify
from flask import request

from app import app, model
from app.util.page import getPage
from app.model import User, Postinfo
from app.service.resiger import addUser
from app.service.login import userLogin
from app.service.imageCode import getImgCode
from app.service.getPredictResult import getPredictResult


@app.before_first_request
def before_test():
    session['request_path'] = '/index'


# 拦截器入口
@app.before_request
def before_login():
    if request.path == url_for('login'):
        return None
    if request.path == url_for('resiger'):
        return None
    if request.path == '/logout':
        return None
    if request.path.startswith("/static"):
        return None
    if request.path.startswith("/imgCode"):
        return None
    if request.path.startswith("/index"):
        return None
    if request.path == '/':
        return None
    if request.path == '/index':
        session['request_path'] = request.path
    if request.path == '/heartPredict':
        session['request_path'] = request.path
    if request.path == '/record':
        session['request_path'] = request.path
    if not session.get("username"):
        session['message'] = ''
        session.pop('message')
        return redirect("/login")


# 默认主页
@app.route('/None')
@app.route("/")
def root():
    return redirect(url_for('index'))


@app.route("/index")
def index():
    user = session.get('username')
    return render_template("index.html", title='模板页', username=user)


# 登出
@app.route('/logout')
def logout():
    if not session.get('username'):
        return redirect(url_for('login'))
    session.pop('username')

    return redirect(url_for('index'))


# 获取历史查询数据，get方法，参数limit为分页大小，page为页数
@app.route('/getHistoryData', methods=['GET'])
def getHistoryData():
    page = request.args.get('page')
    limit = request.args.get('limit')
    userid = User.query.filter_by(username=session.get('username')).first().id
    data = Postinfo.query.filter_by(userid=userid).all()
    res_data = []
    for i in data:
        res_data.append(i.data_serialize())

    usr = {'code': '0', 'msg': '请求成功', 'count': len(data), 'data': getPage(res_data, page, limit)}
    return jsonify(usr)


# 预测页，get方法 无参数
@app.route("/heartPredict", methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        result = session.get('result', None)
    user = session.get('username')
    return render_template("heartPredict.html", username=user)


# 注册接口，get返货注册页，post提交注册
@app.route("/resiger", methods=['GET', 'POST'])
def resiger():
    # 注册接口
    if request.method == 'POST':
        data = json.loads(request.get_data())
        return addUser(data=data)

    message = ''
    if request.args.get('code') == '100':
        message = '用户已存在，请尝试登录'
    elif request.args.get('code') == '101':
        message = '注册失败，请重新尝试'
    elif request.args.get('code') == '102':
        message = '密码输入不一致'
    user = session.get('username')
    return render_template("reg.html", username=user, message=message)


# 历史纪录页，get方法
@app.route("/record")
def record():
    user = session.get('username')
    return render_template("record.html", username=user)


# 登陆接口
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        return userLogin(data)
    else:
        message = ''
        if request.args.get('failure') == 'true':
            message = '用户名或者密码错误，请重新输入'
        elif request.args.get('failure') == '200':
            message = '恭喜您！注册成功，请登录'
        elif request.args.get('failure') == '201':
            message = '验证码错误'
        if session.get('username'):
            if session.get('request_path') is None:
                session['request_path'] = '/index'
            return redirect(session.get('request_path'))
        return render_template("/login.html", message=message, request_path=session.get('request_path'))


@app.route('/submitPredict', methods=['GET', 'POST'])
def submitPredict():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        getPredictResult(data)
        return ''


@app.route('/preResult', methods=['GET', 'POST'])
def preresult():
    result_s = session.get('result_s', None)
    result_m = session.get('result_m', None)
    age = session.get('age')
    sex = session.get('sex')
    preid = session.get('preid')
    user = session.get('username')
    return render_template('preResult.html', result_s=result_s,
                           result_m=result_m, age=age, sex=sex,
                           preid=preid, username=user)


@app.route('/imgCode')
def imgCode():
    return getImgCode()


@app.route('/getalldata')
def getalldata():
    data = Postinfo.query.all()
    res_data = []
    for i in data:
        res_data.append(i.data_serialize())
    usr = {'code': '0', 'msg': '请求成功', 'count': len(data), 'data': res_data}
    return jsonify(usr)
