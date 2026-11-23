"""Original menu artwork and sound. Python + Pillow + NumPy. No downloaded assets."""
from pathlib import Path
import math, random, wave
from PIL import Image,ImageDraw
import numpy as np
base=Path(__file__).resolve().parents[1]
out=base/'assets';out.mkdir(exist_ok=True)
rng=random.Random(338)
im=Image.new('RGB',(640,360),'#adb09a');d=ImageDraw.Draw(im)
def poly(pts,c): d.polygon(pts,fill=c)
def line(pts,c,w=1): d.line(pts,fill=c,width=w)
def rect(coords,c):d.rectangle(coords,fill=c)
for y,c in [(0,'#455652'),(15,'#596962'),(39,'#718278'),(70,'#8c9782'),(98,'#a4a78c'),(118,'#c0b494'),(143,'#cdbb92')]:rect((0,y,639,359),c)
d.ellipse((257,48,290,81),fill='#e1c891')
for j in range(95):
 x,y=rng.randrange(640),rng.randrange(23,136);width=rng.randrange(9,85)
 line([(x,y),(x+width,y)],rng.choice(['#9b9d86','#a7aa8e','#7b8b80']))
def ridge(h,amp,col,sp):
 pts=[(x,int(h+amp*math.sin(x/sp)+amp*.48*math.cos(x/(sp*.37))+rng.randint(-3,3))) for x in range(-5,650,6)]
 poly(pts+[(650,360),(-5,360)],col);return pts
ridge(150,23,'#738075',69);ridge(166,18,'#586f65',41);ridge(190,16,'#415c51',57)
def fir(x,y,h,c,light):
 line([(x,y-h),(x,y)],c)
 for k in range(2,7):
  top=y-h+int((k-2)*h*.105);bottom=y-h+int(k*h*.15);wide=max(2,int(h*k*.040))
  poly([(x,top),(x-wide,bottom),(x-1,bottom-1),(x+wide,bottom+1)],c)
  line([(x-1,top+3),(x-wide,bottom)],light)
for j in range(350):
 x=rng.randrange(640);y=187+int(12*math.sin(x/53))+rng.randrange(19);fir(x,y,rng.randint(5,14),'#3d594a','#5c7160')
# Steep basalt outcrop, with rock planes, scree and narrow courses of masonry.
cliff=[(71,225),(88,215),(102,211),(126,206),(167,210),(189,203),(216,210),(245,213),(263,224),(243,242),(233,257),(184,271),(132,277),(88,258)]
poly(cliff,'#3c4439')
for j in range(175):
 x=rng.randrange(91,241);y=rng.randrange(216,259);h=rng.randrange(2,10)
 if im.getpixel((x,y)) in [(60,68,57),(70,77,63)]:line([(x,y),(x-3,y+h)],rng.choice(['#5a604b','#2c3e35','#74755a']))
def masonry(x,y,w,h):
 rect((x,y,x+w,y+h),'#343d34');rect((x+1,y+1,x+w-1,y+h-1),'#8e896b')
 for yy in range(y+2,y+h-1,4):
  line([(x+1,yy),(x+w-1,yy)],'#686c54')
  for xx in range(x+2+(yy//4%2)*4,x+w-2,8):
   line([(xx,yy),(xx,yy+2)],'#656950')
   if rng.random()<.4: line([(xx+1,yy+1),(min(x+w-1,xx+4),yy+1)],'#aca17b')
 rect((x+w-max(2,w//4),y+1,x+w-1,y+h-1),'#515b47')
def tower(x,y,w,h,roof=True):
 masonry(x,y,w,h)
 if roof:
  peak=(x+w//2,y-w)
  poly([(x-3,y+1),peak,(x+w+3,y+1)],'#273d38')
  poly([(x-2,y),peak,(x+w//2-1,y)],'#4a6558')
  line([(x-2,y),(x+w//2,y-w)],'#b6a880')
 else:
  for k in range(x,x+w,5):rect((k,y-3,k+2,y),'#aa9975')
 for yy in range(y+7,y+h-3,12):
  for xx in range(x+4,x+w-3,7):
   rect((xx,yy,xx+1,yy+3),'#29382f')
   if rng.random()<.42:rect((xx,yy+1,xx,yy+2),'#e0b55d')
def flag(x,y):
 line([(x,y-12),(x,y+1)],'#56432d')
 poly([(x+1,y-12),(x+13,y-11),(x+8,y-8),(x+1,y-8)],'#983e2c');line([(x+1,y-12),(x+9,y-11)],'#d7a157')
masonry(111,177,110,38)
tower(118,159,14,53);tower(183,145,17,66)
tower(146,145,26,64);tower(156,127,13,42)
tower(190,144,11,40);tower(101,180,13,39,False);tower(217,176,13,43,False)
flag(162,115);flag(125,147);flag(224,176)
masonry(110,198,108,19)
for k in range(109,218,7):rect((k,194,k+3,200),'#998e69')
tower(152,191,12,30,False);tower(174,190,12,31,False)
d.pieslice((163,202,176,220),180,360,fill='#25362e');rect((163,211,175,221),'#25362e')
for x,y in [(123,180),(193,163),(155,151),(178,202)]:
 poly([(x,y),(x+4,y),(x+4,y+9),(x+2,y+12),(x,y+10)],'#a14933')
line([(167,222),(163,228),(183,235),(182,238),(145,245),(133,250),(142,254)],'#af9f73',2)
for j in range(72):
 x=rng.randrange(640);y=267+rng.randrange(20);fir(x,y,rng.randrange(13,36),'#304c40','#4a6550')
ridge(290,12,'#253e34',49)
for j in range(95):
 x=rng.randrange(640);y=306+rng.randrange(33);fir(x,y,rng.randrange(21,49),'#21372e','#3a5140')
ridge(338,7,'#1c3028',38)
for x in [5,25,350,381,414,602,625]:
 fir(x,338+rng.randrange(13),rng.randrange(63,106),'#1b2e26','#344a38')
im.save(out/'keep_at_dusk.png')
# Plucked modal theme, made specifically for this game; seamless wrap-around decay.
sr=22050;beat=.48;length=int(sr*beat*48);music=np.zeros(length)
def pluck(start,note,amp,decay,span):
 t=np.arange(int(span*sr))/sr;f=440*2**((note-69)/12)
 a=np.minimum(1,t/.012)*np.exp(-t/decay)
 tone=np.sin(2*np.pi*f*t)+.38*np.sin(2*np.pi*2*f*t+.1)*np.exp(-2*t)+.17*np.sin(2*np.pi*3*f*t)*np.exp(-3*t)
 np.add.at(music,(int(start*sr)+np.arange(len(t)))%length,amp*a*tone)
for bar,notes in enumerate([(50,57,62,65),(46,53,58,62),(48,55,60,64),(45,52,57,60),(50,57,62,65),(48,55,60,67),(43,50,55,62),(45,52,57,64)]):
 for j,k in enumerate([0,1,2,3,2,1]):pluck((bar*6+j)*beat,notes[k],.085 if j else .12,.72,2.9)
 for j,k in [(0,3),(3,2)]:pluck((bar*6+j)*beat,notes[k]+12,.064,1.15,3.5)
music+=.16*np.roll(music,int(.19*sr))+.08*np.roll(music,int(.35*sr))
def wav(path,data):
 with wave.open(str(path),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((np.clip(data,-1,1)*32767).astype('<i2').tobytes())
wav(out/'menu_lute.wav',music)
t=np.arange(int(sr*.15))/sr;wav(out/'ui_select.wav',.18*np.sin(2*np.pi*(610*t+140*t*t))*np.exp(-35*t)*np.minimum(1,t/.006))

