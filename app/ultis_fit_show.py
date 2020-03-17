# from fitparse import FitFile
# 用于打印profile中的所有字段,使用不同的profile配置会有不同的结果,这里打印结果仅依赖于profile.py文件
from fitparse.profile import MESSAGE_TYPES
# from fitparse.utils import scrub_method_name
from translate import file_info_translate,activity_translate,session_translate

# 定义全局的字典
fit_show_dict = dict()
fit_info_dict = dict()
fit_activity_dict = dict()
fit_session_dict = dict()
fit_lap_list = []
fit_multi_record_list = [{'record':'information'}]
fit_position_list = []
# 提取用于显示的数据部分
fit_show_dict = dict()
fit_msg_type_list = []#fit文件解码后所包含的类型

def fit_profile_show():
    unit_values = []
    unit_dict = dict()
    for message_type in MESSAGE_TYPES.values():
        for field in message_type.fields.values():
            unit_values.append(field.units)
            unit_dict[str(field.name)] = field.units
            if field.components:
                for component in field.components:
                    unit_values.append(component.units)
                    unit_dict[component.name] = component.units
            if field.subfields:
                for subfield in field.subfields:
                    unit_values.append(subfield.units)
                    unit_dict[subfield.name] = subfield.units
                    if subfield.components:
                        for component in subfield.components:
                            unit_values.append(component.units)
                            unit_dict[component.name] = component.units

    # unit_values = filter(None, unit_values)
    # for unit_value in sorted(set(unit_values)):
    #     print(format(unit_value))

    # unit_dict = unit_dict.pop(filter(None, unit_dict.values()))
    print(unit_dict)

# 打印当前fit文件中所有的字段,用于测试该fit文件内包含的字段类型
def fit_message_all_show(fitfile=None):
    if fitfile is None:
        fit_profile_show()
        return

    unit_dict = dict()
    for message_type in MESSAGE_TYPES.values():
        msg_dict = dict()
        msg_dict = list(fitfile.get_messages(name=message_type.name))
        if len(msg_dict) > 0:
            unit_dict[message_type.name] = msg_dict.copy()
            fit_msg_type_list.append(message_type.name)

    # for x in unit_dict:
    #     print(x, len(unit_dict[x]), '\n')
    #     print(unit_dict[x])

def file_info_fit_show(fitfile):
    # fit_show_dict['profile_version']=fitfile.profile_version
    # fit_show_dict['protocol_version']=fitfile.protocol_version
    types = ['device_info', 'device_settings',
             'file_creator', 'file_id', 'sport',
             'activity', 'session']
    # type = []
    # types = fit_msg_type_list.copy()#这里显示fit文件中所有包含的字段,sub_type有可能相互重叠
    # types.remove('record')
    # types.remove('event')
    # types.remove('lap')
    # types.remove('session')
    # types.remove('activity')
    fit_show_en_dict = dict()#英文字典
    for message_type in types:
        for fit_message in fitfile.get_messages(message_type):
            for field_data in fit_message:
                if 'unknown' not in field_data.name:
                    # field_name = file_info_translate(field_data.name)
                    # field_name = field_data.name;#不翻译,就不进行过滤
                    #通过翻译器进行数据显示的过滤
                    # if field_name not in field_data.name:
                    fit_show_en_dict[field_data.name] = str(field_data.value)
                    # if field_data.units is not None:
                    #     fit_show_en_dict[field_data.name] += field_data.units

    # 过滤和修正部分数据
    from ultis_fit_time import utc_dt_to_dt
    keyword = 'timestamp'
    #有可能fit中不包含时区信息
    if 'time_offset' not in fit_show_en_dict.keys():
        fit_show_en_dict['time_offset'] = 0;#默认为UTC时间
    if keyword in fit_show_en_dict.keys():
        fit_show_en_dict[keyword] = utc_dt_to_dt(fit_show_en_dict[keyword]
                                    , fit_show_en_dict['time_offset'])
    keyword = 'time_created'
    if keyword in fit_show_en_dict.keys():
        fit_show_en_dict[keyword] = utc_dt_to_dt(fit_show_en_dict[keyword]
                                    , fit_show_en_dict['time_offset'])

    # # 添加activity和session信息
    secs = float(fit_show_en_dict['total_timer_time'])
    m, s = divmod(int(secs), 60)
    h, m = divmod(m, 60)
    fit_show_en_dict['total_timer_time'] = str(h)+':'+str(m)+':'+str(s)

    dist = float(fit_show_en_dict['total_distance'])
    fit_show_en_dict['total_distance'] = str(dist/1000) + ' km'

    # fit_show_dict = fit_show_en_dict.copy()#显示所有
    # 翻译并只显示翻译指定数据
    for field_name in fit_show_en_dict.keys():
        tr_name = file_info_translate(field_name)
        if tr_name not in field_name:#无法翻译,非指定显示内容
            fit_show_dict[tr_name] = fit_show_en_dict[field_name]

    # print(fit_show_dict)

def activity_fit_show(fitfile):
    for fit_message in fitfile.get_messages('activity'):
        for field_data in fit_message:
            # Print the records name and value (and units if it has any)
            if field_data.value is not None:
                field_name = activity_translate(field_data.name)
                if isinstance(field_data.value, str):
                    fit_activity_dict[field_data.name] = field_data.value
                if field_data.value is not None:
                    fit_activity_dict[field_data.name] = str(field_data.value)
                if field_data.units is not None:
                    fit_activity_dict[field_data.name] += ' ' + field_data.units
    print(fit_activity_dict)

def session_fit_show(fitfile):
    for fit_message in fitfile.get_messages('session'):
        for field_data in fit_message:
            # Print the records name and value (and units if it has any)
            # if field_data.units:
            #     print(' * %s: %s %s' % (
            #        field_data.name, field_data.value, field_data.units,
            #     ))
            # else:
            #     print(' * %s: %s' % (field_data.name, field_data.value))

            if field_data.value is not None:
                field_name = session_translate(field_data.name)
                if isinstance(field_data.value, str):
                    fit_session_dict[field_data.name] = field_data.value
                if field_data.value is not None:
                    fit_session_dict[field_data.name] = str(field_data.value)
                if field_data.units is not None:
                    fit_session_dict[field_data.name] += ' ' + field_data.units
    print(fit_session_dict)

def record_fit_show(fitfile):
    for fit_message in fitfile.get_messages('record'):
        fit_record_dict = dict()
        position_dict = dict()
        for field_data in fit_message:
            if field_data.value is not None:
                # field_name = record_translate(field_data.name)
                if 'position_lat' in field_data.name:
                    field_data.value = float(field_data.value) * 0.83819 / 10000000
                    position_dict['lat'] = field_data.value
                if 'position_long' in field_data.name:
                    field_data.value = float(field_data.value) * 0.83819 / 10000000
                    position_dict['lng'] = field_data.value
                fit_record_dict[field_data.name] = str(field_data.value)
                if field_data.units is not None:
                    fit_record_dict[field_data.name] += ' ' + field_data.units
        fit_multi_record_list.append(fit_record_dict)
        if len(position_dict) > 0:
            fit_position_list.append(position_dict)

    # print(fit_multi_record_list)
    print(fit_position_list)

# 计算心率变异性
def file_hrv_fit_show(fitfile):
    from ultis_hrv import file_hrv_fit
    fit_show_dict['心率变异性'] = str(file_hrv_fit(fitfile))

def all_fit_show(fitfile):
    # print('activities num:', len(list(fitfile.get_messages(name='activity'))))
    # print('sessions num:', len(list(fitfile.get_messages(name='session'))))
    # print('laps num:', len(list(fitfile.get_messages(name='lap'))))
    # print('records num:', len(list(fitfile.get_messages(name='record'))))

    # 读取文件中所包含的字段并放入fit_msg_type_list
    # 该函数需要第一个调用
    fit_message_all_show(fitfile)
    activity_fit_show(fitfile)
    session_fit_show(fitfile)
    record_fit_show(fitfile)
    #该函数依赖activity,session解码,需要放在后面
    file_info_fit_show(fitfile)
    fit_message_need_show(fitfile)

    file_hrv_fit_show(fitfile)

#显示需要查看的字段内容,如果不包含该字段,则不会显示
def fit_message_need_show(fitfile):
    # fit_info_dict['运动类型'] = fit_show_dict['sport']
    # fit_info_dict['生产厂家'] = fit_show_dict['manufacturer']
    # fit_info_dict['产品型号'] = fit_show_dict['garmin_product']

    import copy
    fit_info_dict = copy.deepcopy(fit_show_dict)

