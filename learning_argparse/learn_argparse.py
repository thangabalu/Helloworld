#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import sys
import argparse
import os


"""
Learning Argparse
"""

#TODO - Use this function to validate the input
def dir_arg(arg):
    if os.path.isdir(arg):
        return arg
    else:
        msg = '%s is not a directory' %arg
        raise argparse.ArgumentTypeError(msg)

def main():
    print 'this is main'

if __name__ == "__main__":
    #TODO- Add choice
    parser = argparse.ArgumentParser(description='Inspects and report on the Python test cases.',prog='testimony')
    #Positional arguments (mandatory arguments)
    parser.add_argument('square', type=int, help='square a number', nargs='+')
    #parser.add_argument('fyra', type=int, help='square a number', nargs='+')
    #parser.add_argument('trice', type=int, nargs='+', help='a list of paths to look for tests cases')
    
    #optional argument. Needs one value
    parser.add_argument('-r','--rank',help ='tell the rank')

    #optional argument. More than one value can be given.
    parser.add_argument('-f','--friends',type=str, help ='tell the rank', nargs='+')
    
    #optional argument with option, action = 'store_true' which stores the value, true or false. Store_true can be used only with optional arguments.
    #If this option is not given, value is false
    parser.add_argument(
        '-n', '--nocolor', action='store_true', help='Do not use color option')
        
    #optional argument with option, choices
    parser.add_argument('-c','--choi', type=int, choices=[1,2,3],help='optional argument with the option choices')

    args = parser.parse_args() 
    if args.square:
        print 'you entered the option square'
        print '%s'%(args.square)
    #if args.trice:
        #print 'you entered the option thrice'
        #print '%s'%(args.trice)
    if args.friends:
        print 'Friends - %s' %(args.friends)
    
    if args.choi:
        print 'your choice -%s' %(args.choi)
    
    if args.nocolor:
        print 'you picked no color -%s' %(args.nocolor)
        
    main()