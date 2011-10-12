from .grammar import grammar
from .generators import generate_python, generate_java, generate_cpp
from .plugins import plugins
from .support import EventEngine

default_settings = {
    "output": "out",
    "mode": None,
    "define": "__DYNAMIC_TPL_HPP__",
    "header": "generated.hpp",
    "source": "generated.cpp"
};

modes = {
  "java": generate_java,
  "python": generate_python,
  "cpp": generate_cpp
}

def exit_usage():
  import sys

  print "Usage: codegen -M <mode> <messages>"
  print "Options:"
  print "  -d <output> : Directory to save generated output in."
  print "  -M <mode>   : Generate code for the specified <mode>."
  print "  -p <plugin> : Enable plugin named <plugin>."
  print "  Available modes:"
  for m in modes:
    print "    " + m

  sys.exit(1)

def readopts(args, event):
  import getopt
  S = dict(default_settings)

  opts,args = getopt.gnu_getopt(args, "d:M:p:h")

  for k,v in opts:
    if k == "-d":
      S["output"] = v
    elif k == "-p":
      if v not in plugins:
        raise ValueError, "Not a valid plugin '" + v + "'"
      plugins[v](event)
    elif k == "-M":
      if v not in modes:
        raise ValueError, "Not a valid mode '" + v + "'"
      S["mode"] = v
    elif k == "-h":
      exit_usage()

  return S,args

def entrymain(args):
  import sys

  event = EventEngine()

  S,args = readopts(args, event)

  event.trigger("notice", S)

  if len(args) != 1:
    exit_usage()

  if S["mode"] is None:
    print >>sys.stderr, "No mode specified"
    exit_usage()

  try:
    packages_list = grammar.parseFile(open(args[0]), parseAll=True)
  except:
    print >>sys.stderr, "Failed to parse file"
    raise

  packages = dict()

  for p in packages_list:
    if p.name in packages:
      print "Duplicate package '{0}'".format(p.name)
      return 1
    packages[p.name] = p

  return modes.get(S["mode"])(S, packages, event)

def entrypoint():
  import sys
  sys.exit(entrymain(sys.argv[1:]))

if __name__ == "__main__":
  entrypoint()
