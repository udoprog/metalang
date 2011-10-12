from .support import read_template
from .grammartypes import *

def generate_python(S, packages, event):
  import os

  output_dir = S["output"]

  if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

  def generate_baseclass(out):
    print >>out, read_template("messagebase.tpl.py")

  def generate_package(out, p):
    print >>out, "from . import base as message_base"
    print >>out, ""
    for k,m in p.messages.items():
      print >>out, "class {0}(message_base):".format(m.name)
      print >>out, "  __classname__ = \"{0}.{1}\";".format(p.name, m.name)
      print >>out, "  __keys__ = ["
      for f in m.fields:
        print >>out, "    \"{0}\",".format(f.name)
      print >>out, "  ]"
      print >>out, ""

  init_path = os.path.join(output_dir, "__init__.py")
  print "Writing " + init_path

  init = open(init_path, "w")
  try:
    generate_baseclass(init)
  finally:
    init.close()

  for pn,p in packages.items():
    package_path = os.path.join(output_dir, "{0}.py".format(p.name))
    print "Writing " + package_path
    package = open(package_path, "w")
    try:
      generate_package(package, p)
    finally:
      package.close()

def generate_java(S, packages, event):
  pass

def generate_cpp(S, packages, event):
  import os

  output_dir = S["output"]

  if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

  header_path_tmp = os.path.join(output_dir, S["header"] + ".tmp")
  header_path     = os.path.join(output_dir, S["header"])
  source_path_tmp = os.path.join(output_dir, S["source"] + ".tmp")
  source_path     = os.path.join(output_dir, S["source"])

  def convert_type(f):
    if isinstance(f, BoolDecl):
      return "bool"
    if isinstance(f, IntDecl):
      return "int"
    if isinstance(f, StringDecl):
      return "std::string"
    if isinstance(f, ListDecl):
      return "dynamic_list"
    if isinstance(f, ObjectDecl):
      return "object*"
    return "__badtype__"

  def generate_accessor(f):
    if isinstance(f, BoolDecl):
      return "as_boolean()"
    if isinstance(f, IntDecl):
      return "as_integer()"
    if isinstance(f, StringDecl):
      return "as_string()"
    if isinstance(f, ListDecl):
      return "as_list()"
    if isinstance(f, ObjectDecl):
      return "as_object()"
    return "__badtype__()"

  def generate_header(S, event, hdr, packages):
    print >>hdr, "#ifndef {0}".format(S["define"])
    print >>hdr, "#define {0}".format(S["define"])
    print >>hdr, ""
    print >>hdr, "namespace metalang {"
    print >>hdr, "  typedef enum {"
    for pn,p in packages.items():
      for mn,m in p.messages.items():
        print >>hdr, "    /* line #{0}: {1} */".format(m.line, m.text)
        print >>hdr, "    {0}_{1},".format(p.name, m.name)
    print >>hdr, "  } message_type;"
    print >>hdr, "}"
    print >>hdr, ""
    print >>hdr, read_template("dynamic.tpl.hpp")
    print >>hdr, ""

    for pn,p in packages.items():
      print >>hdr, ""
      print >>hdr, "/* line #{0}: {1} */".format(p.line, p.text)
      print >>hdr, "namespace {0}".format(pn)
      print >>hdr, "{"
      print >>hdr, "  using metalang::message_type;"
      print >>hdr, "  using metalang::object;"
      print >>hdr, "  using metalang::dynamic_map;"
      print >>hdr, "  using metalang::dynamic_pair;"
      print >>hdr, "  using metalang::dynamic_list;"
      print >>hdr, ""
      for mn,m in p.messages.items():
        print >>hdr, "  /* line #{0}: {1} */".format(m.line, m.text)
        print >>hdr, "  class {0} : public object".format(mn)
        print >>hdr, "  {"
        print >>hdr, "  public:"
        print >>hdr, "    static const message_type object_type = metalang::{0}_{1};".format(pn,mn)
        print >>hdr, ""
        print >>hdr, "    {0}();".format(mn)
        print >>hdr, "    virtual message_type type() const;"
        print >>hdr, "    virtual const char* name() const;"
        print >>hdr, "    static std::string static_name();"
        print >>hdr, "    static object* new_instance();"
        print >>hdr, ""
        for f in m.fields:
          print >>hdr, "    /* line #{0}: {1} */".format(f.line, f.text)
          print >>hdr, "    {0} get_{1}();".format(convert_type(f), f.name)
          print >>hdr, "    void set_{1}({0} {1});".format(convert_type(f), f.name)
          print >>hdr, "    bool has_{0}();".format(f.name)
          print >>hdr, ""
        print >>hdr, "  private:"
        print >>hdr, "    static const char* _name;"
        #for f in m.fields:
        #  print >>hdr, "    {0} {1};".format(convert_type(f), f.name)
        print >>hdr, "  };"
        print >>hdr, ""
      print >>hdr, "}"

    event.trigger("cpp-header", S, hdr, packages)

    print >>hdr, "#endif /* {0} */".format(S["define"])


  def generate_getter(S, out, f, m):
    print >>out, "  {0} {2}::get_{1}()".format(convert_type(f), f.name, m.name)
    print >>out, "  {"
    print >>out, "    dynamic d = get(\"{0}\");".format(f.name)
    print >>out, "    if (d.empty()) {"
    # maybe throw an exception instead?
    print >>out, "      throw metalang::missing_field(\"{0}\");".format(f.name)
    print >>out, "    }"
    print >>out, "    return d.{0};".format(generate_accessor(f))
    print >>out, "  }"

  def generate_setter(S, out, f, m):
    print >>out, "  void {2}::set_{1}({0} {1})".format(convert_type(f), f.name, m.name)
    print >>out, "  {"
    print >>out, "    set(\"{0}\", {0});".format(f.name)
    print >>out, "  }"

  def generate_has(S, out, f, m):
    print >>out, "  bool {1}::has_{0}()".format(f.name, m.name)
    print >>out, "  {"
    print >>out, "    return has(\"{0}\");".format(f.name)
    print >>out, "  }"

  def generate_source(S, event, out, packages):
    print >>out, "#include \"{0}\"".format(S["header"])
    print >>out, ""
    print >>out, read_template("dynamic.tpl.cpp")
    print >>out, ""

    print >>out, "namespace metalang"
    print >>out, "{"
    print >>out, "  generator_map __create_generators()"
    print >>out, "  {"
    print >>out, "    generator_map m;"
    for pn,p in packages.items():
      for mn,m in p.messages.items():
        print >>out, "    m.insert(generator_pair({0}::{1}::static_name(), {0}::{1}::new_instance));".format(pn, mn)
    print >>out, "    return m;"
    print >>out, "  }"
    print >>out, ""
    print >>out, "  generator_map __generators = __create_generators();"
    print >>out, ""
    print >>out, "  object* new_instance(std::string name)"
    print >>out, "  {"
    print >>out, "    return __generators[name]();"
    print >>out, "  }"
    print >>out, "}"

    for pn,p in packages.items():
      print >>out, "namespace {0}".format(pn)
      print >>out, "{"
      print >>out, "  using metalang::dynamic;"
      for mn,m in p.messages.items():
        print >>out, "  const char* {1}::_name = \"{0}.{1}\";".format(p.name, m.name)
        print >>out, "  {0}::{0}()".format(mn)
        print >>out, "  {"
        print >>out, "    set(\"__class__\", std::string(name()));"
        print >>out, "  }"
        print >>out, "  const char* {0}::name() const".format(mn)
        print >>out, "  {"
        print >>out, "    return _name;"
        print >>out, "  }"
        print >>out, "  message_type {0}::type() const".format(mn)
        print >>out, "  {"
        print >>out, "    return metalang::{0}_{1};".format(pn,mn)
        print >>out, "  }"
        print >>out, "  object* {0}::new_instance()".format(mn)
        print >>out, "  {"
        print >>out, "    return new {0};".format(mn)
        print >>out, "  }"
        print >>out, "  std::string {0}::static_name()".format(mn)
        print >>out, "  {"
        print >>out, "    return \"{0}.{1}\";".format(pn, mn)
        print >>out, "  }"

        for f in m.fields:
          generate_getter(S, out, f, m)
          generate_setter(S, out, f, m)
          generate_has(S, out, f, m)
      print >>out, "}"
      print >>out, ""

      # build type specializations of dynamic constructors
      for pn,p in packages.items():
        print >>out, "/* type specializations */"
        print >>out, "namespace metalang"
        print >>out, "{"
        for mn,m in p.messages.items():
          print >>out, "  template<> dynamic::dynamic<{0}::{1}>(const {0}::{1}& object)".format(pn,mn)
          print >>out, "  {"
          print >>out, "    _pointer_value.reset(new {0}::{1}(object));".format(pn,mn)
          print >>out, "    _type = Object;"
          print >>out, "  }"
        print >>out, "}"

    event.trigger("cpp-source", S, out, packages)

  hdr = open(header_path_tmp, "w")

  print "Writing " + header_path_tmp
  try:
    generate_header(S, event, hdr, packages)
  finally:
    hdr.close()

  out = open(source_path_tmp, "w")

  print "Writing " + source_path_tmp
  try:
    generate_source(S, event, out, packages)
  finally:
    out.close()

  print "Moving {0} -> {1}".format(header_path_tmp, header_path)
  os.rename(header_path_tmp, header_path)
  print "Moving {0} -> {1}".format(source_path_tmp, source_path)
  os.rename(source_path_tmp, source_path)

__all__ = ["generate_python", "generate_java", "generate_cpp"]
