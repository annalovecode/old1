from exts import db


# 用户表
class User(db.Model):
    # 定义表名
    __tablename__ = 'user'

    # 定义列对象
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    emailAddress = db.Column(db.String(255), unique=True)
    age = db.Column(db.Integer)
    sex = db.Column(db.Integer)
    password = db.Column(db.String(255))


# 提交信息表
class Postinfo(db.Model):
    __tablename__ = 'postinfo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, db.ForeignKey(User.id))
    age = db.Column(db.String(255))
    sex = db.Column(db.String(255))
    cp = db.Column(db.String(255))
    trestbps = db.Column(db.String(255))
    chol = db.Column(db.String(255))
    fbs = db.Column(db.String(255))
    restecg = db.Column(db.String(255))
    thalach = db.Column(db.String(255))
    exang = db.Column(db.String(255))
    oldpeak = db.Column(db.String(255))
    slop = db.Column(db.String(255))
    ca = db.Column(db.String(255))
    num = db.Column(db.String(255))

    def data_serialize(self):
        result = Result.query.filter_by(postid=self.id).first()
        return {
            'preId': self.id,
            'age': self.age,
            'sex': self.sex,
            'cp': self.cp,
            'trestbps': self.trestbps,
            'chol': self.chol,
            'fbs': self.fbs,
            'restecg': self.restecg,
            'thalach': self.thalach,
            'exang': self.exang,
            'oldpeak': self.oldpeak,
            'slop': self.slop,
            'ca': self.ca,
            'thal': self.num,
            'num1': result.result_s,
            'num2': result.result_m,
        }


# 结果表
class Result(db.Model):
    # 定义表名
    __tablename__ = 'result'
    postid = db.Column(db.Integer, db.ForeignKey(Postinfo.id), primary_key=True)
    result_m = db.Column(db.String(255))
    result_s = db.Column(db.String(255))
