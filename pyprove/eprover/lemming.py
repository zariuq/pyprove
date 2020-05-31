#!/usr/bin/env python3

import os, re

MIZAR = os.path.join(os.getenv("HOME","."), "atp/bin/mizar40.axiom.names")

def mizar():
   miz = open(MIZAR).read().strip().split("\n")
   miz = dict([x.split(" ") for x in miz if x])
   return miz

def make(f_out, axioms=None, d_lmgs=None):
   lems = {}
   elders = {}
   roles = {}
   for line in open(f_out):
      if not (line.startswith("fof(") or line.startswith("cnf(")):
         continue
      if "trainpos" in line or "trainneg" in line:
         continue

      if ", file(" in line:
         parts = line[4:].split(",")
         name = parts[0]
         role = parts[1].strip(" ")

         elders[name] = set([name])
      elif ", inference(" in line:
         name = line[4:].split(",")[0]
         role = line.split(", ")[1].strip(" ")
         inf = line[line.index(", inference("):]
         sources = re.findall(r"[a-zA-Z0-9_]+", inf)
         sources = [x for x in sources if x in elders]
         if not sources:
            continue
         elders[name] = set.union(*[elders[x] for x in sources])
      else:
         continue # well, there are some: "introduced(" or just a label in cnf's

      if not role in roles:
         roles[role] = set()
      roles[role].add(name)

      if role != "plain" or len(elders[name]) <= 1:
         continue

      if any([x not in roles["axiom"] for x in elders[name]]):
         continue
            
      clause = ", ".join(line.split(", ")[2:])
      clause = clause[:clause.index(", inference(")]

      if re.search(r"esk[0-9]+_[0-9]+", clause) or ("epred" in clause):
         continue

      lem = "-".join(sorted([axioms[x] for x in elders[name]]))

      if lem not in lems:
         lems[lem] = set()
      lems[lem].add(clause)

   if d_lmgs:
      append(lems, d_lmgs=d_lmgs)

   return lems if not d_lmgs else None

def join(*ls):
   lems = {}
   for l in ls:
      for x in l:
         if x not in lems:
            lems[x] = set()
         lems[x].update(l[x])
   return lems


def append(lems, d_lmgs="lemmings"):
   os.system("mkdir -p %s" % d_lmgs)
   for l in lems:
      with open(os.path.join(d_lmgs,l),"a") as f: f.write("\n".join(lems[l]))


def save(lems, prf="lmg_", d_lmgs="lemmings", counter=[0]):
   def fresh():
      counter[0] += 1
      return "%s%s" % (prf, counter[0])

   os.system("mkdir -p %s" % d_lmgs)
   for l in lems:
      ls = ["cnf(%s, axiom, %s)."%(fresh(),c) for c in lems[l]]
      with open(os.path.join(d_lmgs,l),"w") as f: f.write("\n".join(ls))


#miz = mizar()
#lems = join(*[
#   lemming("139.out", miz),
#   lemming("317.out", miz)
#])
#save(lems)

