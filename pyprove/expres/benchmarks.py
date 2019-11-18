import os

from .. import eprover, log, bar
from . import protos, results
from . import solved as solvedb

BENCHMARKS_DIR = os.getenv("ATPY_BENCHMARKS", ".")
TIMEOUT = 7*24*60*60

def path(bid, problem=""):
   ret = os.path.join(BENCHMARKS_DIR, bid, problem)
   return ret

def problems(bid):
   probs = os.listdir(path(bid))
   probs = [x for x in probs if os.path.isfile(path(bid, x)) and not x.endswith(".cnf")]
   return probs

def compute(bid, pid, problem, limit, force=False, ebinary=None, eargs=None):
   f_problem = path(bid, problem)
   f_out = results.path(bid, pid, problem, limit)
   if force or not os.path.isfile(f_out):
      os.system("mkdir -p %s" % os.path.dirname(f_out))
      proto = protos.load(pid)
      out = eprover.runner.run(f_problem, proto, limit, f_out, ebinary, eargs)
   return results.load(bid, pid, problem, limit)

def run_compute(job):
   return bar.run(compute, job)

def eval(bid, pids, limit, cores=4, force=False, ebinary=None, eargs=None, **others):
   def callback(arg, res, bar):
      if eprover.result.solved(res):
         bar.inc_solved()

   probs = problems(bid)
   log.msg("+ evaluating %s strategies @ %s (%d problems) @ limit %s @ %s cores" % (len(pids), bid, len(probs), limit, cores))
   
   allres = {}
   fmt = "%%%ds" % max(map(len,pids))
   for (n,pid) in enumerate(pids,start=1):
      if "completed" in others and pid in others["completed"]:
          continue
      args = [(bid,pid,problem,limit,force,ebinary,eargs) for problem in probs]
      name = pid if len(pid)<30 else "%s..%s"%(pid[:12],pid[-16:])
      name = "(%d/%d) %30s" % (n,len(pids),name)
      outs = bar.applies(name, run_compute, args, 
               cores=cores, bar=bar.SolvedBar, callback=callback)
      res = {x[0:4]:y for (x,y) in zip(args,outs)}
      solvedb.update(res)
      allres.update(res)
      if "completed" in others:
          others["completed"][pid] = True
   return allres

def cnf(bid, problem, force):
   f_cnf = path(os.path.join(bid, "cnf"), problem)
   if force or not os.path.isfile(f_cnf):
      f_problem = path(bid, problem)
      open(f_cnf,"wb").write(eprover.runner.cnf(f_problem))

def run_cnf(job):
   return bar.run(cnf, job)

def cnfize(bid, cores=4, force=False, **others):
   os.system("mkdir -p %s" % path(bid, "cnf"))
   args = [(bid,p,force) for p in problems(bid)]
   bar.applies("Computing CNFs", run_cnf, args, cores=cores)

def solved(bid, pids, limit, cores=4, force=False):
   res = eval(bid, pids, limit, cores=cores, force=force)
   res = {x:res[x] for x in res if eprover.result.solved(res[x])}
   return res

def get(bid, pids, limit):
   probs = problems(bid)
   rkeys = [(bid,pid,problem,limit) for pid in pids for problem in probs]
   print("Loading %d results ..." % len(rkeys))
   ret = {rkey:results.load(*rkey) for rkey in rkeys if results.exists(*rkey)}
   print("done.")
   return ret

