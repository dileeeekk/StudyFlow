from qa import *
wifi=run('shell','settings','get','global','wifi_on').strip()
mobile=run('shell','settings','get','global','mobile_data').strip()
try:
 run('shell','svc','wifi','disable');run('shell','svc','data','disable');time.sleep(2)
 tap('button1');time.sleep(3)
 t=ui()
 error=find(t,'planner_form_error')
 assert error is not None and error.get('text'), 'No network error shown'
 assert any(n.get('text')=='Problem set 04' for n in t.iter('node')), 'Draft lost'
 shot('06-network-error')
 print('Offline save displays an error and preserves the form.')
finally:
 if wifi==b'1':run('shell','svc','wifi','enable')
 if mobile==b'1':run('shell','svc','data','enable')
