import os
from .. import eprover

RESULTS_DIR = os.getenv("EXPRES_RESULTS", "./00RESULTS")
RAMDISK_DIR = None

def path(bid, pid, problem, limit, ext="out"):
   d_pid = "%s%s/%s" % (limit, "s" if isinstance(limit,int) else "", pid)
   f_out = "%s.%s" % (problem, ext)
   f = os.path.join(RESULTS_DIR, bid, d_pid, f_out)
   if RAMDISK_DIR and not os.path.isfile(f):
      f = os.path.join(RAMDISK_DIR, bid, d_pid, f_out)
   return f

def output(bid, pid, problem, limit):
   return file(path(bid, pid, problem, limit)).read()

def exists(bid, pid, problem, limit, ext="out"):
   return os.path.isfile(path(bid, pid, problem, limit, ext=ext))

def save(bid, pid, problem, limit, out):
   f_out = path(bid, pid, problem, limit)
   os.system("mkdir -p %s" % os.path.dirname(f_out))
   file(f_out,"w").write(out)

def load(bid, pid, problem, limit, trains=False, proof=False):
   f_out = path(bid, pid, problem, limit)
   return eprover.result.parse(f_out, trains=trains, proof=proof)

