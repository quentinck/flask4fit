# 使用render_template这个函数渲染模板
from flask import Flask,render_template,request
import sys
from fitparse import FitFile, FitParseError
from ultis_fit_show import all_fit_show,fit_info_dict,fit_show_dict,\
    fit_activity_dict,fit_session_dict,\
    fit_multi_record_list,fit_position_list
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import json

app = Flask(__name__)
GoogleMaps(app)

def fit_decode(file2parse):
    try:
        fitfile = FitFile(file2parse)
        fitfile.parse()
        all_fit_show(fitfile)
    except FitParseError as e:
        print("Error while parsing .FIT file: %s % e")
        sys.exit(1)

# file2parse = 'D:\\MyGarminData\\2019-03-18T04_18_16+00_00_64189059.fit'
# fit_decode(file2parse)

@app.route("/")
@app.route("/fit_parse",methods=['POST','GET'])
def fit_parse():
    file2parse = request.files.get("fit_name")
    #默认进行一个文件的解码,这里主要是为了规避默认的错误
    if file2parse is None:
        # file2parse = 'D:\\MyGarminData\\2019-12-30T23_38_55+00_00_82012108.fit'
        file2parse = 'D:\\MyGarminData\\2019-05-19T23_43_18+00_00_64189156.fit'
    fit_decode(file2parse)
    # 把模板文件的位置传递给render_template这个函数
    # return render_template("fit_parse.html", msg=file2parse.filename+"解析完成")
    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=30.508111133339,
        lng=114.333645243484,
        markers=[(30.508111133339, 114.333645243484)]
    )
    sndmap = Map(
        identifier="sndmap",
        lat=30.508111133339,
        lng=114.333645243484,
        markers=[
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                'lat': 30.508111133339,
                'lng': 114.333645243484,
                'infobox': "<b>Hello World</b>"
            },
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                'lat': 37.4300,
                'lng': -122.1400,
                'infobox': "<b>Hello World from other place</b>"
            }
        ]
    )

    return render_template("fit_parse.html",
                           # fileinfo=fit_info_dict,
                           fileinfo=fit_show_dict,
                           # activity=fit_activity_dict,
                           # session=fit_session_dict,
                           postions=json.dumps(fit_position_list),
                           record=fit_multi_record_list[0],
                           mymap=mymap, sndmap=sndmap)

# fit_parse()

if __name__ == "__main__":
    app.run()