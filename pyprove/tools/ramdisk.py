import os

MODULES = []

def connect(module, ramdisk, envar=None):
   assert not module.RAMDISK_DIR 
   module.RAMDISK_DIR = os.path.join(ramdisk, module.DEFAULT_NAME)
   if envar:
      os.environ[envar] = module.RAMDISK_DIR

def disconnect(module, envar=None):
   assert module.RAMDISK_DIR
   module.RAMDISK_DIR = None
   if envar:
      del os.environ[envar]

def open(module, ramdisk, envar=None, **others):
   if not ramdisk:
      return
   os.system("mkdir -p %s" % module.RAMDISK_DIR)
   connect(module, ramdisk, envar)

def close(module, envar=None, **others):
   if not module.RAMDISK_DIR:
      return
   print("+ Closing ramdisk for module: %s" % module.__name__)
   os.system("mkdir -p %s" % module.DEFAULT_DIR)
   os.system("cp -rf %s/* %s" % (module.RAMDISK_DIR, module.DEFAULT_DIR))
   os.system("rm -fr %s" % module.RAMDISK_DIR)
   disconnect(module, envar)

def register(module, ramdisk, envar=None, **others):
   global MODULES
   MODULES.append((module, ramdisk, envar))

def opens():
   global MODULES
   for (module, ramdisk, envar) in MODULES:
      open(module, ramdisk, envar)

def closes():
   global MODULES
   for (module, ramdisk, envar) in MODULES:
      close(module, envar)



