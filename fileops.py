import os

from subprocess import call

def parent_dir(x):
  d,_ = os.path.split(os.path.abspath(x.rstrip('/')))
  return d

def with_cwd(d, t):
    old = os.getcwd()
    os.chdir(d)
    res = t()
    os.chdir(old)
    return res

def callerror(args):
  res = call(args)
  if res != 0:
    raise ValueError("call returned non zero exit code")

def gitmv(old, new):
  d = parent_dir(old)
  with_cwd(d, lambda: callerror(["git", "mv", old, new]))

def ingit(path):
  d = parent_dir(path)
  res = with_cwd(d, lambda:
    call(["git", "ls-files", "--error-unmatch", path]))
  return res == 0

# API
def grename(old, new):
  print "grename %s %s" % (old,new)
  if ingit(old):
    gitmv(old, new)
  else:
    os.rename(old, new)
  print "end of grename"
