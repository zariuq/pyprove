from os import path, listdir
from .. import par

def ispos(line):
   return line.startswith("cnf(") and \
         ("#trainpos" in line) and \
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
   (pos, neg, other) = split(lines)
   (pos, neg) = (list(pos), list(neg))
   open(f_out,"w").write("\n".join(other))
   if pos:
      open(filename("pos"),"w").write("\n".join(pos))
   if neg:
      open(filename("neg"),"w").write("\n".join(neg))

def makeone(f_out):
   lines = open(f_out).read().strip().split("\n")
   save(lines, f_out)

def make(d_outs, cores=4, msg="[POS/NEG]"):
   files = [path.join(d_out,f) for d_out in d_outs for f in listdir(d_out)]
   files = [(f,) for f in files if isout(f)]
   par.apply(makeone, files, cores=cores, barmsg=msg)

