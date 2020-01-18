from datetime import datetime
from sys import argv, exc_info
import sys
import atexit
import traceback

PREFIX = "~~~pyprove~log~~~"

def terminating(cache):
   msg("Terminating.")
   if "last_traceback" in dir(sys):
      traceback.print_last(file=open(cache[1],"a"))

def trace():
   text(traceback.format_exc())

def start(intro, config=None, script=""):
   config = "\n   ".join(["%12s = %s"%(x,config[x]) for x in sorted(config)]) if config else ""
   intro = "%s\n\n   %s\n" % (intro, config)
   msg(intro, script=script, reset=True)

def msg(msg, cache=[], script="", timestamp=True, reset=False):
   now = datetime.now()
   if not cache:
      script = argv[0] if argv and not script else script
      cache.append(now)
      cache.append(("%s%s~~~%s" % (PREFIX, script.lstrip("./").replace("/","+"), now)).replace(" ","~"))
      atexit.register(terminating, cache)
   elif reset:
      cache[0] = now
   
   msg = ("[%s] %s" % (now-cache[0], msg)) if timestamp else msg
   print(msg)
   if PREFIX:
      f = open(cache[1],"a")
      f.write(msg+"\n")
      f.flush()
      f.close()

def text(msg0=""):
   msg(msg0, timestamp=False)

def humanbytes(b):
   units = {0 : 'Bytes', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB', 5: 'PB'}
   power = 1024
   n = 0
   while b > power:
      b /= power
      n += 1
   return "%.2f %s" % (b, units[n])

def humanint(n):
   s = str(int(abs(n)))
   r = s[-3:]
   s = s[:-3]
   while s:
      r = s[-3:] + "," + r
      s = s[:-3]
   return r if n >= 0 else "-%s" % r

def humantime(s):
   h = s // 3600
   s -= 3600*h
   m = s // 60
   s -= 60*m
   return "%02d:%02d:%04.1f" % (h,m,s)


