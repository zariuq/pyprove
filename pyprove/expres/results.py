import os
from .. import eprover

DEFAULT_NAME = "00RESULTS"
DEFAULT_DIR = os.getenv("PYPROVE_RESULTS", DEFAULT_NAME)
RAMDISK_DIR = None

def dir(bid, pid, limit, **others):
   d_out = bid.replace("/","-") + "-" + limit
   return os.path.join(DEFAULT_DIR, d_out, pid)  

def path(bid, pid, problem, limit, ext="out"):
   global DEFAULT_DIR, RAMDISK_DIR
   tid = bid.replace("/","-")
   tid += "-%s%s" % ("T" if isinstance(limit,int) else "", limit)
   f_out = "%s.%s" % (problem, ext)
   f = os.path.join(DEFAULT_DIR, tid, pid, f_out)
   if RAMDISK_DIR and not os.path.isfile(f):
      f = os.path.join(RAMDISK_DIR, tid, pid, f_out)
   return f

def output(bid, pid, problem, limit):
   return open(path(bid, pid, problem, limit)).read()

def exists(bid, pid, problem, limit, ext="out"):
   return os.path.isfile(path(bid, pid, problem, limit, ext=ext))

def save(bid, pid, problem, limit, out):
   f_out = path(bid, pid, problem, limit)
   os.system("mkdir -p %s" % os.path.dirname(f_out))
   open(f_out,"w").write(out)

def load(bid, pid, problem, limit, trains=False, proof=False):
   f_out = path(bid, pid, problem, limit)
   return eprover.result.parse(f_out, trains=trains, proof=proof)

