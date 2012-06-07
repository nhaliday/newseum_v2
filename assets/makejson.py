#!/usr/bin/env python3


import re
import json
import codecs
from urllib.parse import urlparse
import os

from pprint import pprint


DB = "FINALTEXTDOCUMENTWITHACTUALLYEVERYTHING.txt"
CAMELCASE = re.compile(r"""
    (?<=[A-Z])(?=[A-Z][a-z])
  | (?<=[^A-Z ])(?=[A-Z])
  | (?<=[A-Za-z])(?=[^A-Za-z ])
""", re.VERBOSE)

def better(s):
  s = re.sub('\u2019', '\'', s)
  # s = re.sub('\u201c', '&ldquo', s)
  # s = re.sub('\u201d', '&rdquo', s)
  s = re.sub('\u201c', '<q>', s)
  s = re.sub('\u201d', '</q>', s)
  s = s.encode('ascii', 'xmlcharrefreplace').decode('utf-8')
  return s


def parse(filename):
  '''Get rid of underscores and camel case to make a title.'''

  title = filename
  title = re.sub(r'_+', ' ', title)
  title = CAMELCASE.sub(' ', title)
  return title.strip()


def main():
  s = ""
  with open(DB) as fin:
    s = fin.read()
  l = re.split(r'\n\n\n', s)

  paintings = []
  photos = []
  newspapers = []

  addto = None
  for entry in l:
    if "*paintings" in entry:
      addto = paintings
    elif "*newspapers" in entry:
      addto = newspapers
    elif "*photographs" in entry:
      addto = photos
    else:
      addto.append([s.strip() for s in entry.split('\n')])

  for lst in (paintings, newspapers, photos):
    for i, entry in enumerate(lst):
      url = entry[0]

      o = urlparse(url)
      filename = os.path.basename(o.path)
  
      title = None

      citation = entry[1]

      if lst is not newspapers:
        m = re.search(r'\. [\w\s,\']+\.', citation)
        s, e = m.start(), m.end()
        title = better(citation[s + 1:e - 1].strip())
        citation = citation[:s + 2] + '<cite>' + citation[s + 2:e - 1] + '</cite>' + citation[e - 1:]
      else:
        base, _ = os.path.splitext(filename)
        title = parse(base[4:])

      citation = better(citation)

      caption = entry[2]
      caption = better(caption)

      directory = ""
      if lst is paintings:
        directory = "paintings"
      elif lst is newspapers:
        directory = "newspapers"
      elif lst is photos:
        directory = "photographs"

      lst[i] = {'url': url, 'filename': filename, 'citation': citation,
          'caption': caption, 'loc': os.path.join('assets/img/' + directory, filename)}
      if title:
        lst[i]['title'] = title

    f = ""
    if lst is paintings:
      f = "paintings"
    elif lst is newspapers:
      f = "newspapers"
    elif lst is photos:
      f = "photographs"

    with open(f + ".json", 'w') as fout:
      json.dump(lst, fout, indent=2)
      fout.write('\n')




if __name__ == "__main__":
  main()
