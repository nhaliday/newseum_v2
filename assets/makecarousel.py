#!/usr/bin/env python3


import sys
import json
import os


def main():
  f = sys.argv[1]

  base, ext = os.path.splitext(f)

  with open(f) as fin:
    l = json.load(fin)
  
  with open(base + '.html', 'w') as fout:
    fout.write("""<div id="myCarousel" class="carousel slide">
            <div class="carousel-inner">\n""")

    for i, d in enumerate(l):
      if i == 0:
        fout.write("""<div class="item active">\n""")
      else:
        fout.write("""<div class="item">\n""")

      fout.write("""<img src="{loc}" alt="{title}" />\n""".format(**d))
      fout.write("""<div class="carousel-caption">\n""")

      fout.write("""<h3>{title}</h3>\n""".format(**d))
      if base != 'photographs':
        fout.write("""<p>{caption}</p>\n""".format(**d))
      fout.write("""<p>{citation}</p>\n""".format(**d))


      fout.write("</div>\n")

      fout.write("</div>\n")

    fout.write("""</div>
          <a class="left carousel-control" href="#myCarousel" data-slide="prev">&lsaquo;</a>
          <a class="right carousel-control" href="#myCarousel" data-slide="next">&rsaquo;</a>
          </div>\n""")


if __name__ == "__main__":
  main()
