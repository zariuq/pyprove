from . import details, summary
from .. import log

def processed(bid, pids, results, dkey=None, **others):
   data = details.processed(bid, pids, results, none=-1)

   log.text("Legend:")
   out = "      %25s    " % "problem:"
   for (i,pid) in enumerate(pids):
      out += "%10s" % ("%02d:" % i)
      log.text("%02d: %s" % (i,pid))
   log.text()
   
   log.text("Processed:")
   log.text(out)
   log.text("X = [")
   for d in sorted(data, key=dkey):
      out = "   /* %25s */ " % d[0]
      for pid in pids:
         out += "%10s" % data[d][pid]
      log.text(out)
   log.text("]")
   log.text()

def runtime(bid, pids, results, dkey=None, **others):
   data = details.runtime(bid, pids, results, none=-1)
   
   out = "      %25s    " % "problem:"
   for (i,pid) in enumerate(pids):
      out += "%10s" % ("%02d:" % i)
      log.text("%02d: %s" % (i,pid))
   log.text()

   log.text("Runtime:")
   log.text(out)
   log.text("X = [")
   for d in sorted(data, key=dkey):
      out = "   /* %25s */ " % d[0]
      for pid in pids:
         out += "%10s" % data[d][pid]
      log.text(out)
   log.text("]")
   log.text()

def generated(bid, pids, results, dkey=None, **others):
   data = details.generated(bid, pids, results, none=-1)
   
   out = "      %25s    " % "problem:"
   for (i,pid) in enumerate(pids):
      out += "%10s" % ("%02d:" % i)
      log.text("%02d: %s" % (i,pid))
   log.text()

   log.text("Generated:")
   log.text(out)
   log.text("X = [")
   for d in sorted(data, key=dkey):
      out = "   /* %25s */ " % d[0]
      for pid in pids:
         out += "%10s" % data[d][pid]
      log.text(out)
   log.text("]")
   log.text()

def solved(bid, pids, results, ref=None, **others):
   log.text("Summary @ %s:" % bid)
   if not ref:
      ref = pids[0]
   data = summary.make(bid, pids, results, ref=ref) 
   for pid in sorted(data, key=lambda p: data[p][2], reverse=True):
      s = data[pid]
      if ref:
         log.text("%s %4s/%4s   +%2s/-%2s: %s" % ("!" if s[1] else "",s[2],s[0],s[3],s[4],pid))
      else:
         log.text("%s %4s/%4s: %s" % ("!" if s[1] else "",s[2],s[0],pid))
   log.text()

def grid(xs, ys, key):
   log.text("X = [ %s ]" % " ".join(map(str,xs)))
   log.text("Y = [ %s ]" % " ".join(map(str,ys)))
   log.text("Z = [")
   for y in ys:
      log.text("    %s" % " ".join([str(key(x,y)) for x in xs]))
   log.text("]")

