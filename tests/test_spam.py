import sys,os,json
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','scripts'));import crossroads as c
os.environ['CROSSROADS_CONTACTS']=os.path.join(os.path.dirname(os.path.abspath(__file__)),'contacts_test.json')
os.environ['AGENTMAIL_API_KEY']='dummy';calls=[]
body=open(os.path.join(os.path.dirname(__file__),'req_ok.txt')).read()
def fake(method,path,data=None):
    calls.append(path)
    if '?labels=unread' in path: return {"messages":[{"message_id":"spam1","labels":["spam"]},{"message_id":"ok1","labels":["unread"]}]}
    mid=path.rsplit('/',1)[1]
    return {"labels":["spam"] if mid=="spam1" else ["unread"],"from":"x <crossroads-trey-demo@agentmail.to>","text":body}
c.api=fake;sys.argv=['x','poll','--inbox','nefarioustrey@agentmail.to']
import io,contextlib;o=io.StringIO()
with contextlib.redirect_stdout(o): c.main()
cards=o.getvalue().count('CROSSROADS  -')
print("cards shown:",cards,"calls:",calls); assert cards==1 and not any("spam1" in x for x in calls); print("PASS spam skipped")
