import os
from os import path, listdir
from .. import par

def ispos(line):
   return line.startswith("cnf(") and \
         ("#trainpos" in line or "# trainpos" in line) and \
         ("$false" not in line)

def isneg(line):
   return line.startswith("cnf(") and \
         ("#trainneg" in line) and \
         ("$false" not in line)

def isother(line):
   return (not ispos(line)) and (not isneg(line))

def isout(filename):
   return filename.endswith(".out") and path.isfile(filename)
   
def split(lines):
   pos = filter(ispos, lines)
   neg = filter(isneg, lines)
   other = filter(isother, lines)
   return (pos, neg, other)

def save(lines, f_out):
   def filename(ext):
      return "%s.%s" % (f_out[:-4] if f_out.endswith(".out") else f_out, ext)
   if not path.isfile(f_out):
      # d_dst mode: enforce *.out extension
      f_out = filename("out")
   (pos, neg, other) = split(lines)
   (pos, neg) = (list(pos), list(neg))
   open(f_out,"w").write("\n".join(other)+"\n")
   if pos:
      open(filename("pos"),"w").write("\n".join(pos)+"\n")
   if neg:
      open(filename("neg"),"w").write("\n".join(neg)+"\n")

def makeone(f_out, d_dst=None):
   lines = open(f_out).read().strip().split("\n")
   if d_dst:
      (pid, f) = f_out.split("/")[-2:]
      f_out = path.join(d_dst, pid, f).rstrip("/")
      os.system("mkdir -p %s" % path.dirname(f_out))
   save(lines, f_out)

def make(d_outs, cores=4, msg="[POS/NEG]", chunksize=100, d_dst=None):
   files = [path.join(d_out,f) for d_out in d_outs for f in listdir(d_out)]
   outs = [(f,d_dst) for f in files if isout(f)]
   if not outs:
      outs = [(f,d_dst) for f in files if path.isfile(f)]
   par.apply(makeone, outs, cores=cores, barmsg=msg, chunksize=chunksize)

