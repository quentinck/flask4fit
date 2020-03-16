from ultis_fit_time import dt_to_secs,secs_to_dt
#Ep90. 用89分钟减去10分钟
# 计算心率变异性
def file_hrv_fit(fitfile):
    records_list = list(fitfile.get_messages('record'))

    index = 0
    start_index = 0
    start_time = 0
    hrv1_index = 0
    hrv1_time = 0
    hrv2_index = 0
    hrv2_time = 0
    for record_msg in records_list:
        for field_data in record_msg:
            if 'timestamp' in field_data.name:
                check_time = dt_to_secs(str(field_data.value))
                if start_index == 0 and check_time is not None:
                    start_index = index
                    start_time = check_time
                if hrv1_index == 0 and (check_time-start_time) > 10*60:
                    hrv1_index = index
                    hrv1_time = check_time
                if hrv2_index == 0 and (check_time - start_time) > 89 * 60:
                    hrv2_index = index
                    hrv2time = check_time
        index += 1
    hrv_1 = 0
    hrv_2 = 0
    for field_data in records_list[hrv1_index]:
        if 'heart_rate' in field_data.name:
            hrv_1 = str(field_data.value)
    for field_data in records_list[hrv2_index]:
        if 'heart_rate' in field_data.name:
            hrv_2 = str(field_data.value)
    # hrv_2 = 105
    # hrv_1 = 100
    if hrv_2<hrv_1:
        return 0
    else:
        hrv = abs(int(hrv_2)-int(hrv_1)) / int(hrv_1)
        return str('percent: {:.2%}'.format(hrv))