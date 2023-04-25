import json

from flask import Flask, request, jsonify, session, url_for
from flask import render_template

from pymysql import *
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app,resource={r"/*":{"origins":"*"}})
# bootstrap = Bootstrap(app)
app.config["SECRET_KEY"] = 'TPmi4aLWRbyVq8zu9v82dWYW1'



@app.route('/select',methods=["GET"])
def select():
    # with open(request.get_data().decode('utf-8'), 'r') as j:
    #     get_data = json.loads(j.read())

    get_data = json.loads(request.get_data().decode('utf-8'))
    username = get_data.get('username')
    conn = connect(host='42.192.168.242', user='root', password='123456',
                   database='mytest', charset='utf8')
    cur = conn.cursor()
    cur.execute('select * from userinfo where username = %s',username)
    u=cur.fetchall()

    if u.__len__()!=0:
        print(u)
        return jsonify(code = 200, msg=u)
    else :
        return jsonify(code = 501, msg="无数据")



@app.route('/selectAll',methods=["POST"])
def selectAll():
    # get_data = json.loads( request.get_data().decode( 'utf-8' ) )
    # print(get_data)
    print(request.json)
    return request.json
    # conn = connect(host='42.192.168.242', user='root', password='123456',
    #                database='mytest', charset='utf8')
    # cur = conn.cursor()
    # cur.execute('select * from userinfo')
    # u=cur.fetchall()
    #
    # if u.__len__()!=0:
    #     print(u)
    #     return jsonify(code = 200, msg=u)
    # else :
    #     return jsonify(code = 501, msg="无数据")



@app.route('/index',methods=["GET"])
# 在首页查询数据
def index():
    # 创建数据库的连接
    conn = connect(host='42.192.168.242', user='root', password='123456',
                   database='mytest', charset='utf8')
    cur = conn.cursor()
    sql = "SELECT * FROM info"
    cur.execute(sql)
    u = cur.fetchall()
    # for item in u:
    #     print('姓名:{0} 地址：{1}'.format(item[1], item[4]))
    # print(u)
    conn.close()

    return render_template('index.html',u=u)

# 登录界面
@app.route("/try/login",methods=["GET"])
def loginPage():
    return render_template('login.html')


# 登录Post
@app.route("/try/login",methods=["POST"])
def login():
    """
    账号 username asd123
    密码 password asdasd
    :return:
    """
    # 从html页面上取到相关数据，方便取到在数据库中查询
    # get_data=request.get_json()
    # username= get_data.get("username")
    # print('json'+username)
    # password= get_data.get("password")
    # print('json'+password)
    if request.method=="POST":
        username=request.form['name']
        password=request.form['password']

    print(username)
    if not all([username,password]):
        return jsonify(msg="参数不完整")
    conn = connect(host='42.192.168.242', user='root', password='123456',
                   database='mytest', charset='utf8')
    cur = conn.cursor()
    cur.execute('select * from user where UserName =%s and Password= %s',[username,password])
    u = cur.fetchall()
    print(u)
    if u.__len__()!=0:
        # 如果验证通过 保存登录状态在session中
        print("查到了，确实有")
        session["username"]=username
        # return redirect(url_for('index'))
        # response = redirect("http://10.89.27.249:5000/index",code=302)
        # 这里是不是还需要一个转发或者重定向页面到index
        # print(url_for('index'))
        return '1132131'
    else:
        print('err')
        return jsonify(msg="账号或者密码错误")




@app.route("/upload",methods=["POST"])
def upload():
    get_data=json.loads(request.get_data().decode('utf-8'))
    username=get_data.get('username')
    FEV1 = get_data.get('FEV1')
    FVC = get_data.get('FVC')
    FEV1_FVE = get_data.get('FEV1_FVE')
    PEF = get_data.get('PEF')
    RR = get_data.get('RR')
    print(FEV1, FVC, FEV1_FVE, PEF, RR)
    print("这里到数据")
    try:
        # 创建数据库的连接
        conn = connect(host='42.192.168.242', user='root', password='123456',
                       database='mytest', charset='utf8')
        cur=conn.cursor()
        sql = "insert into UserInfo(username,FEV1,FVC,FEV1_FVE,PEF,RR) values (%s,%s,%s,%s,%s,%s)"
        cur.execute(sql,(username,FEV1,FVC,FEV1_FVE,PEF,RR))
        conn.commit()
        print(FEV1,FVC,FEV1_FVE,PEF,RR)
    except Exception as ex:
        print(ex)
        pass
    finally:
        cur.close()
        conn.close()

    return '0'


if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug = True,port = 5000)