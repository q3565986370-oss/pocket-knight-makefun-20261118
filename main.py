import os,json,urllib.request as U
V=[0,100,320,335,500,900,20000]
D={2:(31,33,14,18,-31,-33,-14,-18),3:(15,17,-15,-17),4:(1,16,-1,-16),5:(1,16,-1,-16,15,17,-15,-17),6:(1,16,-1,-16,15,17,-15,-17)}
def fen(f):
 r,t,c,e,h,*_=f.split();b=[0]*128
 for y,row in enumerate(r.split('/')[::-1]):
  x=0
  for v in row:
   if v.isdigit():x+=int(v)
   else:b[y*16+x]=(' pnbrqk'.index(v.lower()))*(1 if v.isupper() else -1);x+=1
 return b,1 if t=='w' else -1,c, sq(e) if e!='-' else -1,int(h)
def sq(t):return ord(t[0])-97+16*(int(t[1])-1)
def attacked(b,k,s):
 for d in (15,17):
  j=k-s*d
  if not j&136 and b[j]==s:return True
 for p in (2,3,4,6):
  for d in D[p]:
   j=k+d
   while not j&136:
    v=b[j]
    if v:
     if v*s>0 and (abs(v)==p or p in (3,4) and abs(v)==5):return True
     break
    if p in (2,6):break
    j+=d
 return False
def step(t,m):
 b,s,c,e,h=t;a,z,p=m;b=b[:];v=b[a];cap=b[z];b[a]=0;b[z]=p*s if p else v
 if abs(v)==1 and z==e:b[z-16*s]=0
 if abs(v)==6:
  c=c.replace('K' if s==1 else 'k','').replace('Q' if s==1 else 'q','')
  if abs(z-a)==2:r=a+3 if z>a else a-4;b[(a+z)//2]=b[r];b[r]=0
 for j,ch in ((0,'Q'),(7,'K'),(112,'q'),(119,'k')):
  if a==j or z==j:c=c.replace(ch,'')
 return b,-s,c,(a+z)//2 if abs(v)==1 and abs(z-a)==32 else -1,0 if abs(v)==1 or cap else h+1
def moves(t):
 b,s,c,e,h=t
 for a in range(128):
  if a&136 or b[a]*s<=0:continue
  v=abs(b[a]);ds=(16*s,15*s,17*s) if v==1 else D[v]
  for d in ds:
   z=a+d
   while not z&136:
    w=b[z]
    if w*s>0:break
    if v==1:
     if d==16*s:
      if w:break
     elif not w and z!=e:break
    for p in ((5,4,3,2) if v==1 and z//16 in (0,7) else (0,)):
     m=(a,z,p);q=step(t,m)
     if not attacked(q[0],q[0].index(6*s),-s):yield m
    if v==1 and d==16*s and a//16==(1 if s==1 else 6):
     zz=z+d
     if not b[zz]:
      m=(a,zz,0);q=step(t,m)
      if not attacked(q[0],q[0].index(6*s),-s):yield m
    if w or v in (1,2,6):break
    z+=d
  if v==6 and a==(4 if s==1 else 116) and not attacked(b,a,-s):
   for dr,ch in ((1,'K' if s==1 else 'k'),(-1,'Q' if s==1 else 'q')):
    r=a+(3 if dr==1 else -4)
    if ch in c and b[r]==4*s and all(not b[a+dr*j] for j in range(1,3 if dr==1 else 4)) and not attacked(b,a+dr,-s) and not attacked(b,a+2*dr,-s):yield a,a+2*dr,0
def val(t):
 b,s,c,e,h=t;v=0
 for a,p in enumerate(b):
  if p:
   k=abs(p);x=a%16;y=a//16;center=7-abs(2*x-7)-abs(2*y-7)
   v+=(1 if p>0 else -1)*(V[k]+center*(4 if k==2 else 2 if k in (1,3) else 0)+(y if p>0 else 7-y)*(7 if k==1 else 2 if k==4 else 0))
 return v*s
def uci(m):
 a,z,p=m
 return ''.join(chr(97+j%16)+str(j//16+1) for j in (a,z))+(' pnbrqk'[p] if p else '')
def search(t,d,a,z,ply=0):
 global N
 N+=1
 if N>12000:raise OverflowError
 b,s,c,e,h=t;check=attacked(b,b.index(6*s),-s);ms=list(moves(t))
 if not ms:return -30000+ply if check else 0
 if t[4]>=100:return 0
 if d<=0 and not check:
  v=val(t)
  if v>=z:return v
  a=max(a,v)
  if d<=-4:return a
  ms=[m for m in ms if b[m[1]] or m[2] or abs(b[m[0]])==1 and m[1]==e]
 if d<=-6:return val(t)
 ms.sort(key=lambda m:V[abs(b[m[1]])]*10-V[abs(b[m[0]])]+m[2]*100,reverse=True)
 for m in ms:
  v=-search(step(t,m),d-1,-z,-a,ply+1)
  if v>=z:return v
  a=max(a,v)
 return a
def choose(t,legal=None):
 global N
 ms=list(moves(t));ms=[m for m in ms if legal is None or uci(m) in legal]
 if not ms:return sorted(legal)[0] if legal else None
 ms.sort(key=lambda m:V[abs(t[0][m[1]])]*10-V[abs(t[0][m[0]])],reverse=True);N=0;best=ms[0]
 for d in range(1,6):
  a=-40000;win=best
  try:
   for m in ms:
    v=-search(step(t,m),d-1,-40000,-a)
    if v>a:a=v;win=m
  except OverflowError:break
  best=win;ms.remove(best);ms.insert(0,best)
  if a>29000:break
 return uci(best)
def run():
 def post(path,data):return json.load(U.urlopen(U.Request(os.environ['MAKEFUN_ENV_URL'].rstrip('/')+path,json.dumps(data).encode(),{'Content-Type':'application/json'})))
 r=post('/game',{})
 while r['status']!='done':
  r=post('/move',{'game':r['game'],'move':choose(fen(r['fen']),r['legal_moves'])}) if r['status']=='your_move' else post('/game',{})
if __name__=='__main__':run()
