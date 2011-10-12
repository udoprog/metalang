from out.slask import test3
from out import base
import json
import sys

if __name__ == "__main__":
  dct = json.loads(sys.stdin.read())
  print base.from_dict(dct).to_dict()
