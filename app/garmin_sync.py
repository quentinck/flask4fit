# 使用render_template这个函数渲染模板
from flask import Flask,render_template,request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("garmin_sync.html", msg="未同步")

@app.route("/garmin_sync",methods=['POST'])
def garmin_sync():
    from threading import Thread
    import sys
    sys.path.append('app\\garminexport')
    from garminbackup import sync
    from threading import Thread

    # 建立线程进行Garmin数据同步
    Thread(sync())
    # 把模板文件的位置传递给render_template这个函数
    return render_template("garmin_sync.html", msg="数据解析完成")

if __name__ == "__main__":
    app.run()