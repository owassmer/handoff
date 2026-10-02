import sys,re
sys.path.insert(0,'register/work')
from q5_lib import SEC,text
for sid in sys.argv[1:]:
    t=text(sid)
    t=t.split('\n',3)[3] if t.startswith('SOURCE') else t
    t=re.sub(r'\nSOURCE CREDIT:.*','',t,flags=re.S)
    t=re.sub(r'\n(\([0-9A-Za-z]+\))\n',r'\n\1 ',t)
    print('#####',sid,'jev',SEC[sid].get('jev_p_decides')); print(t.strip())
