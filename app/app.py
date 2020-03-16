# 使用render_template这个函数渲染模板
from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")
def index():
    # from threading import Thread
    # import sys
    # sys.path.append('app\\garminexport')
    # from garminbackup import sync
    # from threading import Thread

    # 建立线程进行Garmin数据同步
    #Thread(sync())
    # 把模板文件的位置传递给render_template这个函数
    # 这是一个以templates文件夹开始的相对路径
    return render_template("garmin_sync.html")

# @app.route('/deal_rb/<key>,<val>', methods=['POST', 'GET'])
# def choose(key,val):
#     return "hello"

if __name__ == "__main__":
    app.run()