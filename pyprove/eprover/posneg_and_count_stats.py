import os
import re
from os import path, listdir
from .. import par
from _ast import Try
from random import shuffle
from functools import reduce

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
   pos = list(filter(ispos, lines))
   neg = list(filter(isneg, lines))
   other = list(filter(isother, lines))
   return (pos, neg, other)

def save(lines, f_out, ratio=1):
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
   #(pos, neg, other) = (list(pos), list(neg), list(other))

   pos_set = set()
   neg_set = set()
   posneg = set()
   clauses = {}
   parents = {}
   ppos = []
   pneg = []
   responsible_parents = set()
   stats= dict()
   for line in pos: # + neg:
       clause_name = PATS["NAME"].search(line)
       if clause_name:
           pos_set.add(clause_name.group(1))
   for line in neg:
       clause_name = PATS["NAME"].search(line)
       if clause_name:
           neg_set.add(clause_name.group(1))
   posneg = pos_set | neg_set
   if posneg: #pos_set and neg_set:
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
                   label = clause_name in posneg or is_empty_clause # Formerly posneg
                   parent_key = (parent1, parent2) #if parent1 < parent2 else (parent2, parent1)
                   parent_key2 = (parent2, parent1)
                  
                   stat_key = parent_key if parent1 < parent2 else parent_key2
                   tmp = stats.get(stat_key, (0,0))
                   if label:
                       stats[stat_key] = (tmp[0]+1, tmp[1])
                   else:
                       stats[stat_key] = (tmp[0], tmp[1]+1)

                   if parent_key in parents:
                       label = label or parents[parent_key] # Currently precedence is given to positive data, unweighted
                   #if not label and  parent_key2 in parents:
                   #    label = label or parents[parent_key2]
                   # The idea is to only accept negative examples if a parent is a responsible parent of a good clause
                   # Moreover, the ratio is calculated to roughly balance pos and neg examples
                   #if label or random() < ratio:
                   #    responsible_parents.add(parent1)
                   #    responsible_parents.add(parent2)
                   
                   parents[parent_key] = label
                   #parents[parent_key2] = label
                  
       #i = 0
       for (parent1, parent2), label in parents.items():
           #i = i + 1
           #print("{}> {} {}   (# {})".format("+1" if label else "-0", parent1, parent2, i))
           try:
               parent1_clause = clauses[parent1]
               parent2_clause = clauses[parent2]
           except:
               continue # If the clauses aren't of the prescribed form, i.e., definition introductions rather than inferences, skip it!
           if label:
               ppos.append("%s\n%s;" % (parent1_clause, parent2_clause))
           else: #parent1 in responsible_parents or parent2 in responsible_parents:
               pneg.append("%s\n%s;" % (parent1_clause, parent2_clause))
               
       if ratio > 0:
           shuffle(pneg) 
           cut_off = int(ratio * len(ppos))
           pneg = pneg[:cut_off]
           
            
   slen = len(stats)
   if slen > 0:
       allpos = list(filter(lambda x: x[1] == 0, stats.values()))
       allneg = list(filter(lambda x: x[0] == 0, stats.values()))
       mixed = list(filter(lambda x: x[0] > 0 and x[1] > 0, stats.values()))
       mlen = len(mixed)
       mixed_sums = reduce(lambda x,y: (x[0] + y[0], x[1] + y[1]), mixed) if mlen > 0 else (0,0)
       #averages = (mixed_sums[0] / mlen, mixed_sums[1] / mlen)
       problem_name = f_out.split("/")[-1]
       #print("\n%s" % f_out)
       #print("{1}/{0} parents are all-pos\n{2}/{0} parents are all-neg\n{3}/{0} parents are mixed".format(slen, len(allpos), len(allneg), slen - len(allpos) - len(allneg)))
       #print("\n{3}/{0} parents are mixed -- {1}/{0} parents are all-pos -- {2}/{0} parents are all-neg -- {4}".format(slen, len(allpos), len(allneg), slen - len(allpos) - len(allneg), problem_name))
       print("\n{3}/{0} parents are mixed -- {1}/{0} parents are all-pos -- {2}/{0} parents are all-neg -- mixed (pos,neg): {5} -- {4}".format(slen, len(allpos), len(allneg), mlen, problem_name, mixed_sums))
   #print("given clauses: %s" % len(posneg))
   #print("generated clauses: %s" % len(clauses))
   #print("clauses with two parents: %s" % len(parents))
   #print("responsible parents: %s" % len(responsible_parents))
   #print("positive clauses: %s" % len(ppos))
   #print("negative clauses: %s" % len(pneg))
 
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

