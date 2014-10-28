import sys

if (len(sys.argv) != 3):
  print "Run with 'python whatfetcher.py USERNAME PASSWORD'"
  sys.exit()

import mechanize
import os

br = mechanize.Browser()

# Spoof Headers
br.addheaders = [('User-agent', 'Firefox')]
br.set_handle_robots(False)

# Login
br.open('https://what.cd/login.php')
br.select_form("login")
control = br.form.find_control("username")
control.value = sys.argv[1]
control = br.form.find_control("password")
control.value = sys.argv[2]
br.submit()

# Download New Torrents
br.open('https://what.cd/torrents.php')
for link in br.links():
  if (link.text == 'DL'):
    filename = "torrents/" + os.path.basename(link.url.rsplit('=')[2].rstrip('&authkey') + ".torrent")
    if os.path.exists(filename):
      print "Skipping ", filename
      continue
    print "Downloading ", filename
    response = br.open_novisit(link.url)
    open(filename, 'w').write(response.read())
