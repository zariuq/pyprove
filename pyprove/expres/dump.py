from . import details, summary
from .. import log

def processed(bid, pids, results, dkey=None, **others):
   data = details.processed(bid, pids, results, none=-1)
   msg = ""
   def text(m=""):
      nonlocal msg
      msg += m + "\n"

   text("Legend:")
   out = "      %25s    " % "problem:"
   for (i,pid) in enumerate(pids):
      out += "%10s" % ("%02d:" % i)
      text("%02d: %s" % (i,pid))
   
   text("Processed:")
   text(out)
   text("P = [")
   for d in sorted(data, key=dkey):
      out = "   /* %25s */ " % d[0]
      for pid in pids:
         out += "%10s" % data[d][pid]
      text(out)
   text("]")

   return msg.strip("\n")

def runtime(bid, pids, results, dkey=None, **others):
   data = details.runtime(bid, pids, results, none=-1)
   msg = ""
   def text(m=""):
      nonlocal msg
      msg += m + "\n"
   
   out = "      %25s    " % "problem:"
   for (i,pid) in enumerate(pids):
      out += "%10s" % ("%02d:" % i)
      text("%02d: %s" % (i,pid))

   text("Runtime:")
   text(out)
   text("T = [")
   for d in sorted(data, key=dkey):
      out = "   /* %25s */ " % d[0]
      for pid in pids:
         out += "%10s" % data[d][pid]
      text(out)
   text("]")

   return msg.strip("\n")

def generated(bid, pids, results, dkey=None, **others):
   data = details.generated(bid, pids, results, none=-1)
   msg = ""
   def text(m=""):
      nonlocal msg
      msg += m + "\n"
   
   out = "      %25s    " % "problem:"
   for (i,pid) in enumerate(pids):
      out += "%10s" % ("%02d:" % i)
      text("%02d: %s" % (i,pid))

   text("Generated:")
   text(out)
   text("G = [")
   for d in sorted(data, key=dkey):
      out = "   /* %25s */ " % d[0]
      for pid in pids:
         out += "%10s" % data[d][pid]
      text(out)
   text("]")

   return msg.strip("\n")

def solved(bid, pids, results, ref=None, **others):
   msg = ""
   def text(m=""):
      nonlocal msg
      msg += m + "\n"
   text("Summary @ %s:" % bid)
   if not ref:
      ref = pids[0]
   data = summary.make(bid, pids, results, ref=ref) 
   for pid in sorted(data, key=lambda p: data[p][2], reverse=True):
      s = data[pid]
      if ref and len(s) >=5:
         text("%s %4s/%4s   +%2s/-%2s: %s" % ("!" if s[1] else "",s[2],s[0],s[3],s[4],pid))
      else:
         text("%s %4s/%4s: %s" % ("!" if s[1] else "",s[2],s[0],pid))

   return msg.strip("\n")

def grid(xs, ys, key):
   msg = ""
   def text(m=""):
      nonlocal msg
      msg += m + "\n"
   text("X = [ %s ]" % " ".join(map(str,xs)))
   text("Y = [ %s ]" % " ".join(map(str,ys)))
   text("Z = [")
   for y in ys:
      text("    %s" % " ".join([str(key(x,y)) for x in xs]))
   text("]")
   return msg.strip("\n")

