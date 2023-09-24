from flask import session

from app.util import heartpre
from app import app
from exts import db
from app.model import User, Postinfo,Result


def getPredictResult(data):
    age = data['age']
    sex = data['sex']
    cp = data['cp']
    trestbps = data['trestbps']
    chol = data['chol']
    fbs = data['fbs']
    restect = data['restecg']
    thalach = data['thalach']
    exang = data['exang']
    oldpeak = data['oldpeak']
    slop = data['slop']
    ca = data['ca']
    thal = data['thal']

    result_m = heartpre.heartPre(
        [float(age), float(sex), float(cp), float(trestbps), float(chol), float(fbs), float(restect),
         float(thalach), float(exang), float(oldpeak), float(slop), float(ca), float(thal)])

    result_s = heartpre.heartPre_single(
        [float(age), float(sex), float(cp), float(trestbps), float(chol), float(fbs), float(restect),
         float(thalach), float(exang), float(oldpeak), float(slop), float(ca), float(thal)])

    age = int(age)

    username = session.get('username')
    user = User.query.filter_by(username=username).first()
    postinfo = Postinfo(userid=user.id, age=age, sex=sex, cp=cp, trestbps=trestbps, chol=chol, fbs=fbs,
                              restecg=restect, thalach=thalach, exang=exang
                              , oldpeak=oldpeak, slop=slop, ca=ca, num=thal)
    db.session.add(postinfo)
    db.session.commit()
    postid = postinfo.id

    res = Result(postid=postid, result_m=result_m[0], result_s=result_s[0])
    db.session.add(res)
    db.session.commit()

    res_return = [{
        "preId": postid
        , "age": age
        , "sex": sex
        , "num1": result_m
        , "num2": result_s
    }]

    if age == 0:
        sex = '男'
    else:
        sex = '女'

    session['result_s'] = result_s[0]
    session['result_m'] = result_m[0]
    session['sex'] = sex
    session['age'] = age
    session['preid'] = postid
    return postid
