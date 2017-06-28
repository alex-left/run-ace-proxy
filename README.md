# run-ace-proxy
Nasty script to parse acestreams urls and play it in VLC or kodi with a local aceproxy server.
tested in ubuntu and debian systems

# Description
This is for run easily acestreams with VLC player or kodi aganist local proxy acestream server. 
Supports acestream url or acestreams id. 
For acestream proxy server this docker image works fine:
https://github.com/sergelevin/docker-acestream-debproxy

Also can connect to arenavision web, and extract acestream link. 

``` ace [number of AV channel] ``` 

# requirements
- vlc
- python 3
- dryscrape library
``` pip3 install dryscrape```
- acestream proxy server reacheable

### warning:
probably you need more dependencies to install dryscrape (qt4, webkit, etc...)
more info:
http://dryscrape.readthedocs.io/en/latest/installation.html

# how use

```

usage: ace.py (url) [-h] [-s SERVER] [-f FILE] 

Launch a acestream url with vlc from command line using a custom acestream
proxy or generate a playable strm file

positional arguments:
  url                   valid acestream id or url acestream, for example: "ace
                        acestream://r1oIk6lGyqEvE3BhJavj2goZTwDZUm9X7SMoAeL2"
                        or "ace r1oIk6lGyqEvE3BhJavj2goZTwDZUm9X7SMoAeL2" You
                        can put an id channel from Arenavision web (dryscrape
                        library required), for example: "ace 14"

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        aceproxy server with format: "server:port", for
                        example: "--server myaceproxyserver:8080" or "-s
                        192.168.1.25:8000" by default is "127.0.0.1:8080"
  -f FILE, --file FILE  generate a playable strm file (useful for kodi) for
                        example: "ace 13 -f /home/ubuntu/media/mystream.strm

```
