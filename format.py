#!/usr/bin/python
import sys, argparse

'''
Format Apache Access log into HTML.

Provide the tag you want to look for.

To generate a 404 message on appache, just call a page that does not exist and pass it a tag and your parameters like so:

http://your.ho.st/dir_that_does_not_exist/TAG?firstarg=KEY&secondarg=VALUE

'''

def main(args):
  tag = args.tag
  log = args.log

  for line in open(log):
    if "/" + tag + "?" in line:
      print line

parser = argparse.ArgumentParser(description='Search for a tag in the logfile and format it to HTML.')

parser.add_argument('tag',
                    metavar = 'TAG',
                    help = 'The tag to look for in the log')

parser.add_argument('log',
                    metavar = 'LOGFILE',
                    help = 'Path to logfile')

args = parser.parse_args()
main(args)