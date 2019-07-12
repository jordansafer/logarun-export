
from logarun_export import export_date_range
import PySimpleGUI as SG
from datetime import datetime
from uploader import uploadActivities


# Request dates, logarun login
form = SG.FlexForm('Logarun to Strava transfer info', auto_size_text=True, default_element_size=(40, 1))
layout = [
        [SG.Text('logarun username'), SG.InputText(key='uname')],
        [SG.Text('logarun password'), SG.InputText(key='pass')],
        [SG.Text('strava client id'), SG.InputText(key='id')],
        [SG.Text('strava client secret'), SG.InputText(key='secret')],
        [SG.In(0, size=(10,1), key='sdate')], 
        [SG.CalendarButton('Start Date', target=(4,0))],
        [SG.In(0, size=(20,1), key='edate')],
        [SG.CalendarButton('End Date', target=(6,0))],
        [SG.Ok(key='1')]]

b,v = form.Layout(layout).Read()

## get dates
start = datetime.strptime(v['sdate'][0:10], "%Y-%m-%d")
end = datetime.strptime(v['edate'][0:10], "%Y-%m-%d")

## get logarun logs
data = export_date_range(v['uname'],
                         v['pass'],
                         start,
                         end,
                         0.1) 
#print(data)


## upload to strava
uploadActivities(data, v['id'], v['secret'])




