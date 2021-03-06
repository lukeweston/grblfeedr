#!/usr/bin/env python
# This file is part of the PySide project.
#
# Copyright (C) 2009 Nokia Corporation and/or its subsidiary(-ies).
# Copyright (C) 2009 Riverbank Computing Limited.
# Copyright (C) 2009 Torsten Marek
#
# Contact: PySide team <contact@pyside.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 2 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA

import sys
import optparse
import logging

from PySide import QtCore
import pysideuic

Version = "Python User Interface Compiler"

def generateUi(uifname, pyfname, execute, indent):
    if pyfname == "-":
        pyfile = sys.stdout
    else:
        pyfile = file(pyfname, "w")

    pysideuic.compileUi(uifname, pyfile, execute, indent)
    return 0


optparser = optparse.OptionParser(usage="pyuic4 [options] <ui-file>",
                                  version=Version)
optparser.add_option("-o", "--output", dest="output",
                     default="-", metavar="FILE",
                     help="write generated code to FILE instead of stdout")
optparser.add_option("-x", "--execute", dest="execute",
                     action="store_true", default=False,
                     help="generate extra code to test and display the class")
optparser.add_option("-d", "--debug", dest="debug",
                     action="store_true", default=False,
                     help="show debug output")
optparser.add_option("-i", "--indent", dest="indent",
                     action="store", type="int", default=4, metavar="N",
                     help="set indent width to N spaces, tab if N is 0 (default: 4)")

options, args = optparser.parse_args(sys.argv)

if len(args) != 2:
    print "Error: one input ui-file must be specified"
    sys.exit(1)

if options.debug:
    # Setup logging.
    logger = logging.getLogger('pysideuic')
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(name)s: %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

error = 1
try:
    error = generateUi(args[1], options.output, options.execute,
            options.indent)
except IOError, e:
    sys.stderr.write("Error: %s: \"%s\"\n" % (e.strerror, e.filename))

except SyntaxError, e:
    sys.stderr.write("Error in input file: %s\n" % e)

except pysideuic.exceptions.NoSuchWidgetError, e:
    if e.args[0].startswith("Q3"):
        sys.stderr.write("Error: Q3Support widgets are not supported by PySide.\n")
    else:
        sys.stderr.write(str(e) + "\n")

except Exception, e:
    if logging.getLogger('pysideuic').level == logging.DEBUG:
        import traceback
        traceback.print_exception(*sys.exc_info())
    else:
        sys.stderr.write("An unexpected error occurred.")

sys.exit(error)
