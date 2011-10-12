from .support import read_template

plugins = dict()

def json_plugin(events):
  def notice(S):
    print """
Using the jsoncpp plugin.

Please download and install json-cpp from:
http://jsoncpp.sourceforge.net/
    """

  def add_to_cpp_header(S, hdr, packages):
    print >>hdr, read_template("plugin.json.tpl.hpp")

  def add_to_cpp_source(S, out, packages):
    print >>out, read_template("plugin.json.tpl.cpp")

  events.on("notice", notice)
  events.on("cpp-header", add_to_cpp_header)
  events.on("cpp-source", add_to_cpp_source)

plugins["jsoncpp"] = json_plugin

__all__ = ["plugins"]
