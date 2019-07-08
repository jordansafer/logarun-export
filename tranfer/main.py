
from logarun_export import export_date_range

import PySimpleGUI as SG


form = SG.FlexForm('Logarun to Strava transfer info', auto_size_text=True, default_element_size=(40, 1))
layout = [
        [SG.Text('logarun username'), SG.InputText(key='uname')],
        [SG.Text('logarun password'), SG.InputText(key='pass')],
        [SG.In(0, size=(10,1), key='sdate')], 
        [SG.CalendarButton('Start Date', target=(2,0))],
        [SG.In(0, size=(20,1), key='edate')],
        [SG.CalendarButton('End Date', target=(4,0))],
        [SG.Ok(key='1')]]

b,v = form.Layout(layout).Read()
print(v)
print(v['sdate'][0:9])
print(v['uname'])
x = 1/0
## get dates



## get username, password
username = 'fileyfood500'
password = 'mlpnko'

## strava login


## get logarun logs
data = export_date_range(username,
                        password,
                        args.start,
                        args.end)



## upload to strava
