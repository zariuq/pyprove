import os
import re
from os import path, listdir
from .. import par
from _ast import Try

PATS = {
   "NAME":      re.compile(r"^cnf\((\w+),"),                        # Retrieves clause name
   "TRAIN":     re.compile(r"(^cnf\((\w+),.*?\)\.)"),               # Retrieves clause name and whole formula.
   "DERIV":     re.compile(r"(^cnf\((\w+),.*?), inference.*?\)\."), # Retrieves clause name and formula, dropping the inference derivation
   "PARENTS":   re.compile(r"\[(\w+), (\w+)\]"),                    # Retrieves primary parents from an inference() stack, eg: [c_0_35, c_0_36]
   "FALSE":     re.compile(r"\$false")                              # Checks for the empty clause
}

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
   dirname, f_name = os.path.split(os.path.splitext(f_out)[0])
   dirname = os.path.join(dirname, "parents")
   def filename_parents(ext):
      return os.path.join(dirname, "%s.%s" % (f_name, ext))
   if not path.isfile(f_out):
      # d_dst mode: enforce *.out extension
      f_out = filename("out")
   os.system('mkdir -p "%s"' % dirname) # I don't see a more efficient way to do this at the moment
   (pos, neg, other) = split(lines)
   (pos, neg, other) = (list(pos), list(neg), list(other))
   given_clauses = {}
   posneg = set()
   clauses = {}
   parents = {}
   for line in pos + neg:
       clause_name = PATS["NAME"].search(line)
       if clause_name:
           posneg.add(clause_name.group(1))
   for line in other:
       clause = PATS["DERIV"].search(line)
       if clause:
           clause_formula = "{}).".format(clause.group(1))
           clause_name = clause.group(2)
           clauses[clause_name] = clause_formula
           
           clause_parents = PATS["PARENTS"].search(line)
           if clause_parents:
               parent1 = clause_parents.group(1)
               parent2 = clause_parents.group(2)
               is_empty_clause = True if PATS["FALSE"].search(clause_formula) else False
               label = clause_name in posneg or is_empty_clause
               parent_key = (parent1, parent2) if parent1 < parent2 else (parent2, parent1)
               if parent_key in parents:
                   label = label or parents[parent_key] # Currently precedence is given to positive data, unweighted
               parents[parent_key] = label
   print("\n%s" % f_out)
   print("given clauses: %s" % len(posneg))
   print("generated clauses: %s" % len(clauses))
   print("clauses with two parents: %s" % len(parents))
   ppos = []
   pneg = []
   for (parent1, parent2), label in parents.items():
       #print("{}> {} {}".format("+1" if label else "-0", parent1, parent2))
       parent1_clause = clauses[parent1]
       parent2_clause = clauses[parent2]
       if label:
           ppos.append(parent1_clause)
           ppos.append(parent2_clause + ";")
       else:
           pneg.append(parent1_clause)
           pneg.append(parent2_clause + ";")
              
   open(f_out,"w").write("\n".join(other)+"\n")
   if pos:
      open(filename("pos"),"w").write("\n".join(pos)+"\n")
   if neg:
      open(filename("neg"),"w").write("\n".join(neg)+"\n")
   if ppos:
      open(filename_parents("pos"),"w").write("\n".join(ppos)+"\n")
   if pneg:
      open(filename_parents("neg"),"w").write("\n".join(pneg)+"\n")

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

