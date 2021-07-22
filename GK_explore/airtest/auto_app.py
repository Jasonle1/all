# -*- encoding=utf8 -*-
__author__ = "admin"
# auto_setup(__file__)
from airtest.core.api import *
from airtest.core.android.android import Android
from poco.drivers.android.uiautomation import AndroidUiautomationPoco


# with open('play_tel.csv',mode='r') as tel:
#     print(tel.readlines()[:10])
# start_time = dt.datetime.now()
poco = AndroidUiautomationPoco(force_restart=False)
connect_device('Android:///')
# 点击
touch(Template(r"tpl1619334146303.png", record_pos=(0.118, -0.56), resolution=(1080, 2340)))
touch(Template(r"tpl1619334639319.png", record_pos=(0.428, -0.949), resolution=(1080, 2340)))

touch(Template(r"tpl1619334205849.png", record_pos=(0.269, -0.658), resolution=(1080, 2340)))
touch(Template(r"tpl1619334217279.png", record_pos=(-0.056, -0.829), resolution=(1080, 2340)))
# 输入手机号
# data = pd.read_csv('play_tel.csv')
# test = data[:50]
test = ['18332159776', '13570364927', '19126382311', '13828410541', '13828410541']

def caozuo(tel):
    text(tel)
    touch(Template(r"tpl1619514492371.png", record_pos=(-0.397, -0.813), resolution=(1080, 2340)))
    if exists(Template(r"tpl1619518204902.png", threshold=0.93, record_pos=(-0.048, -0.816), resolution=(1080, 2340))):

        touch(Template(r"tpl1619514526576.png", record_pos=(-0.447, -0.953), resolution=(1080, 2340)))
        touch(Template(r"tpl1619334570545.png", record_pos=(0.318, -0.951), resolution=(1080, 2340)))
        res = '男'


    elif exists(Template(r"tpl1619692343322.png", threshold=0.93, record_pos=(0.005, -0.812), resolution=(1080, 2340))):
        touch(Template(r"tpl1619514526576.png", record_pos=(-0.447, -0.953), resolution=(1080, 2340)))
        touch(Template(r"tpl1619334570545.png", record_pos=(0.318, -0.951), resolution=(1080, 2340)))
        res = '女'

    else:
        touch(Template(r"tpl1619513630179.png", record_pos=(0.314, -0.944), resolution=(1080, 2340)))
        res = ''

    return res


# test['sex'] = test.tel.astype('str').apply(caozuo)
# test.to_csv('test.csv')
print([caozuo(t) for t in test])
# print(man,girl)
# print(caozuo('13570364927'))

# end_time = dt.datetime.now()
# print('训练所需时间:{}'.format(end_time-start_time))
# data['sex'] = data.tel.astype('str').apply(caozuo)











