from multiprocessing import Pool, Manager

TIMEOUT = 7*24*60*60

def apply(fun, args, cores=4, callback=None, bar=None, barmsg=None):
   pool = Pool(cores)
   m = Manager()
   queue = m.Queue()
   todo = len(args)
   if barmsg and not bar:
      from .bar import ProgressBar
      bar = ProgressBar(barmsg, max=todo)
   if bar: bar.start()

   args = [(fun,job,queue) for job in args]
   runner = pool.starmap_async(run, args, chunksize=1)
   while todo:
      (arg,res) = queue.get(TIMEOUT)
      if callback:
         callback(arg, res, bar)
      todo -= 1
      if bar: bar.next()
   if bar: bar.finish()
   pool.close()
   pool.join()
   ret = runner.get(TIMEOUT)
   return ret if not callback else None

def run(fun, job, queue):
   try:
      res = fun(*job)
   except Exception as e:
      print(e)
      import traceback
      print("Error: "+traceback.format_exc())
      res = None
   queue.put((job, res))
   return res

