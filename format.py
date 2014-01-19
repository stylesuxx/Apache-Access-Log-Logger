#!/usr/bin/python
import sys, argparse, re
from datetime import datetime

def main(args):
  tag = args.tag
  logPath = args.log
  outPath = args.out
  counter = 0;
  output = ''

  try:
    for line in open(logPath):
      if tag in line:
        counter += 1
        ip = line.split()[1]
        
        # Apache should log with this timestamp [18/Jan/2014:22:55:43 +0100]
        dateString = re.findall('\[([a-zA-Z0-9\:\/]*).*\]', line)[0]
        date = datetime.strptime(dateString, '%d/%b/%Y:%H:%M:%S')

        agent = re.findall('"-" "(.*)"$', line)[0]

        # "GET /test?first=foo&second=bar HTTP/1.1"
        url = re.findall('\"(GET|POST) (.*) HTTP\/[0-9\.]*\"', line)[0][1]

        # /test?first=foo&second=bar
        keyValue = re.findall('\?([a-zA-Z0-9]*\=.*) HTTP\/', line)[0]
        keyValue = keyValue.split('&')

        for pair in keyValue:
          key = re.findall('([a-zA-Z0-9]*)\=', pair)[0]
          value = re.findall('[a-zA-Z0-9]*\=(.*)', pair)[0]

          output += '''
                    <tr>
                      <td>%s</td>
                      <td>%s</td>
                      <td><a href="#" class="agent" title="%s">%s</a></td>
                      <td>%s</td>
                      <td>%s</td>
                    </tr>
                    ''' %(date.strftime('%d-%m-%Y'), date.strftime('%H:%M:%S'), agent, ip, key, value)

    # Replace the placeholders in the template and write output
    html = open('template.html').read()
    html = html.replace('%%ROWS%%', output)
    html = html.replace('%%PATH%%', logPath)

    outPath = outPath if outPath else 'out-%s.html' %(tag)
    out = open(outPath, 'w+')
    out.write(html)
    out.close

    print 'Found %i matches for "%s". Open "%s" in your browser.' %(counter, tag, outPath)

  except IOError:
    print 'Log file does not exist or you are not allowed to read it.'

parser = argparse.ArgumentParser(description='Search for a tag in the apache access log files and format it to sort and filterable HTML table.')
parser.add_argument('tag', metavar = 'TAG', help = 'The tag to look for in the log')
parser.add_argument('log', metavar = 'LOGFILE', help = 'Path to logfile')
parser.add_argument('-o',
                    '--out',
                    dest = 'out',
                    metavar = 'OUTPUT',
                    default = False,
                    help = 'Path of the output file')

args = parser.parse_args()
main(args)