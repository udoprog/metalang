from pyparsing import *
from .grammartypes import *

ParserElement.setDefaultWhitespaceChars(" \t")

eos = OneOrMore(Literal("\n")).suppress()

def get_debugdata(loc,s):
  line = lineno(loc,s)
  text = s.split("\n")[line-1]
  return line,text

def newFieldDecl(s,loc,toks):
  t,n = toks[0]
  line, text = get_debugdata(loc,s)
  return FieldDecl.get(t).__call__(t,n, line=line, text=text)

def newMessageDecl(s,loc,toks):
  t = toks[0]
  name = t[0]
  fields = t[1:]
  line, text = get_debugdata(loc,s)
  return MessageDecl(name, fields, line=line, text=text)

def newPackageDecl(s,loc,toks):
  t = toks[0]
  name = t[0]
  messages = t[1:]
  line, text = get_debugdata(loc,s)
  return PackageDecl(name, messages, line=line, text=text)

name_decl   = Combine(Word(alphas) + ZeroOrMore(Word(alphanums)))
field_type  = reduce(lambda a,b: a | b, map(lambda typename: Literal(typename), FieldDecl.types.keys()))
field_decl  = Group(field_type + name_decl).setParseAction(newFieldDecl)

message_body = OneOrMore(field_decl + eos)

END = "end"
end = Literal(END).suppress() + eos
MESSAGE = "message"
message = Literal(MESSAGE).suppress()

message_decl = Group(
    message + name_decl + eos + 
    message_body +
    end).setParseAction(newMessageDecl)

PACKAGE = "package"
package_decl = Literal(PACKAGE).suppress() + name_decl + eos
package = Group(package_decl + OneOrMore(message_decl) + end).setParseAction(newPackageDecl)
# root
grammar = OneOrMore(package)

__all__ = ["grammar"]
