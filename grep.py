#!/usr/bin/env python3

import re
import os
import sys

usage = """
grep - search pattern in files or standard input

USAGE:
  grep [OPTIONS] PATTERN [FILE...]
  
OPTIONS:
  -h   print this information
  -v   reverse search
  
"""

class Program:
 
  class Error(Exception):
    pass
  
  def __init__(self):
    self.pattern = None
    self.opts = {
      'v': False,
      'h': False,
    }
    self.paths = []
    self.lines_printed = 0
  
  def parse_args(self, argv):
    for arg in argv:
      if arg.startswith('-'):
        # short option
        for c in arg[1:]:
          if c in self.opts.keys():
            self.opts[c] = True
          else:
            raise Error("unknwon option '%s'" % c)
      elif self.pattern is None:
        # reg exp pattern
        try:
          self.pattern = re.compile(arg)
        except re.error:
          raise Error("invalid pattern specified")
      else:
        # file name
        if os.path.isfile(arg):
          self.paths.append(arg)
        else:
          raise Error("'%s' is not valid file name" % arg)
  
  def iter_stdin(self):
    yield sys.stdin.readline()
    
  def iter_paths(self):
    for path in self.paths:
      with open(path) as file:
        yield file.readline()
        
  def search_lines(self, input):
    for line in input:
      match = self.pattern.match(line)
      if ((match and not self.opts['v'])
        or (not match and self.opts['v'])):
          print(line)
          self.lines_printed += 1
        
  def exec_command_line(self, argv):
    self.parse_args(argv)
    if self.opts['h']:
      print(usage)
      sys.exit(0)
    if self.paths:  # look up path
      self.search_lines(self.iter_paths())
    else:  # read from stdin
      self.search_lines(self.iter_stdin())
    sys.exit(0 if self.lines_printed > 0 else 1)
  
  
if __name__ == '__main__':
  try:
    if len(sys.argv) < 2:
      sys.stdout.write(usage)
      sys.exit(2)
    else:
      Program().exec_command_line(sys.argv[1:])
      
  except Program.Error as ex:
    sys.stderr.write("error: %s" % str(ex))
    sys.exit(2)
    
  except Exception as ex:
    sys.stderr.write("unexpected error: %s" % str(ex))
    sys.exit(2)