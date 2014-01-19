#!/usr/bin/python
import sys, argparse, re
from datetime import datetime

def main(args):
  tag = args.tag
  log = args.log
  output = ''

  for line in open(log):
    if tag in line:
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
                    <td>''' + date.strftime('%Y-%d-%m') + '''</td>
                    <td>''' + date.strftime('%H:%M:%S') + '''</td>
                    <td><a href="#" class="agent" title="''' + agent + '''">''' + ip + '''</a></td>
                    <td>''' + key + '''</td>
                    <td>''' + value + '''</td>
                  </tr>
                  '''

  # Replace the placeholders in the template and write output
  html = open('template.html').read()
  html = html.replace('%%ROWS%%', output)
  html = html.replace('%%PATH%%', log)

  out = open('out-' + tag + '.html', 'w+')
  out.write(html)
  out.close

parser = argparse.ArgumentParser(description='Search for a tag in the apache access log files and format it to sort and filterable HTML table.')
parser.add_argument('tag', metavar = 'TAG', help = 'The tag to look for in the log')
parser.add_argument('log', metavar = 'LOGFILE', help = 'Path to logfile')

args = parser.parse_args()
main(args)