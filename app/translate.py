import re
import six

class Xlator(dict):
    def _make_regex(self):
        return re.compile('|'.join(map(re.escape, six.iterkeys(self))))

    def __call__(self, match):
        return self[match.group(0)]

    def xlat(self, text):
        return self._make_regex().sub(self, text)

#fit文件解码后的对应翻译,具体包含哪些,参考fit_parse中的profile.py
#profile.py 0: MessageType  file_id部分
file_info_adict = {
    'manufacturer': '厂家',
    'garmin_product': '型号',
    'serial_number': '设备序列号',
    'software_version': '软件版本',
    'timestamp': '数据时间timetamp',
    'time_created': '起始时间',
    'sport': '运动类型',
    'sub_sport': '运动子类型',
    'resting_heart_rate': '静息心率',
    #activity
    'total_timer_time' :'总时间',
    #session
    'avg_cadence' :'平均踏频',
    'avg_heart_rate' :'平均心率',
    'avg_power':'平均功率',
    'avg_speed':'平均速度',
    'total_distance':'距离',
    'total_training_effect':'训练效果TE',
    'training_stress_score':'训练压力TSS'
}

session_adict = {
    'start_time':'开始时间',
    'start_position_lat':'起始坐标lat',
    'start_position_long':'long',
    'sport':'运动类型',
    'sub_sport':'子类型'
}

activity_adict = {
    'sport': '运动类型'
}

#FIELD_TYPES
field_types_adict = {
    'sport':'运动类型',
    'activity_subtype':'运动类型',
    'treadmill':'跑步:tredmill',
    'trail': '跑步: ',
    'track': '评审: ',
    'spin': '骑行: ',
    'indoor_cycling': '骑行: ',
    'road': '骑行: ',
    'mountain': '骑行: ',
    'downhill': '骑行: ',
    'recumbent': '骑行: ',
    'cyclocross': '骑行: ',
    'hand_cycling': '骑行: ',
    'track_cycling': '骑行: ',
    'indoor_rowing': 'Fitness Equipment',
    'elliptical': 'Fitness Equipment',
    'stair_climbing': 'Fitness Equipment',
    'lap_swimming': 'Swimming',
    'open_water': 'Swimming'
}

def file_info_translate(field_name):
    if field_name in file_info_adict.keys():
        return file_info_adict[field_name]
    else:
        return field_name

def session_translate(field_name):
    if field_name in session_adict.keys():
        return session_adict[field_name]
    else:
        return field_name

def activity_translate(field_name):
    if field_name in activity_adict.keys():
        return activity_adict[field_name]
    else:
        return field_name

#匹配部分单词的翻译
# text = 'Larry Wall is the creator of Perl'
# xlat = Xlator(activty_adict)
# print(xlat.xlat(text))