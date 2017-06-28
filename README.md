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
- vlc (optional if you use it for kodi)
https://www.videolan.org/vlc/
- python 3
- dryscrape library (optional if you will use it only with url's)
``` pip3 install dryscrape```
- acestream proxy server reacheable (see docker image in description)

### warning:
probably you need more dependencies to install dryscrape (qt4, webkit, etc...)
more info:
http://dryscrape.readthedocs.io/en/latest/installation.html

# install
- clone project
``` git clone https://github.com/alex-left/run-ace-proxy ```
- copy the program to PATH for more convenience
``` cd run-ace-proxy && sudo cp ace.py /usr/bin/ace```
- install optional dependencies (see requirements)

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
# TO DO
- set the default local aceproxy server reading it from an config/enviroment file (for example: /etc/ace.conf) to avoid set it 
by parameter if you use a player in different machine than docker engine. 
- get urls from more providers ¿suggestions? I only know arenavision
- add more players? I only use VLC. 
- investigate a way to send the stream to kodi directly avoiding the strm file generation (maybe by kodi's api?)
- create an installer?
- organize, improve and Beautify the code. 
