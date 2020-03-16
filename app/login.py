# 使用render_template这个函数渲染模板
from flask import Flask,render_template,request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login",methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("pwd")
    if username == "ajax" and password == "123":
        return "成功 "
    else:
        return render_template("login.html", msg="登陆失败")

if __name__ == "__main__":
    app.run()