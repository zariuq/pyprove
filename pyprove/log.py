from datetime import datetime
from sys import argv, exc_info
import sys
import atexit
import traceback
import sys, os, io
import ctypes

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

libc = ctypes.CDLL(None)
c_stdout = ctypes.c_void_p.in_dll(libc, 'stdout')
c_stderr = ctypes.c_void_p.in_dll(libc, 'stderr')

def redirect(std, fd):
   libc.fflush(c_stdout)
   libc.fflush(c_stderr)
   std_fd = std.fileno()
   std.close()
   os.dup2(fd, std_fd)
   return io.TextIOWrapper(os.fdopen(std_fd,"wb"))

def redirect_start(f_log, bar=None):
   s_log = open(f_log, mode="wb")
   dup_out = os.dup(sys.stdout.fileno())
   dup_err = os.dup(sys.stderr.fileno())
   sys.stdout = redirect(sys.stdout, s_log.fileno())
   sys.stderr = redirect(sys.stderr, s_log.fileno())
   if bar:
      bar.file = io.TextIOWrapper(os.fdopen(dup_err,"wb"))
   return (s_log, dup_out, dup_err)

def redirect_finish(s_log, dup_out, dup_err):
   sys.stdout = redirect(sys.stdout, dup_out)
   sys.stderr = redirect(sys.stderr, dup_err)
   os.close(dup_out)
   os.close(dup_err)
   s_log.close()

