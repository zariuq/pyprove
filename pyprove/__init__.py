
__all__ = ["eprover", "expres", "log"]

import progress
from progress.bar import FillingCirclesBar as Bar
from math import ceil

class SolvedBar(Bar):
   
   def __init__(self, message, max):
      Bar.__init__(self, message, max=max)
      self._solved = 0
      self.suffix = "%(percent)5.1f%% | +%(solved)4s @ %(elapsed_td)s | ETA +%(eta_solved)4s @ %(eta_td)s"

   def inc_solved(self):
      self._solved += 1

   @property
   def eta(self):
      return int(ceil((self.elapsed/self.progress)-self.elapsed)) if self.progress else 0

   @property
   def solved(self):
      return self._solved

   @property
   def eta_solved(self):
      return int(ceil((self._solved / self.progress))) if self.progress else 0

