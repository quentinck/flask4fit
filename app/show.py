from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    s = "python测试"
    fun = {"数据同步", "单模块测试"}
    return render_template('show.html', descr=s, func=fun)

if __name__ == "__main__":
    app.run(Debug=True)