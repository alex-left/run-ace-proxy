# run-ace-proxy
parse acestreams urls to use local aceproxy with vlc

this is for run easily acestreams with VLC player aganist proxy acestream. This docker image works fine:
https://github.com/sergelevin/docker-acestream-debproxy

Also can scrap the arenavision web, extract de acestream link and open it. 

``` ace [number of AV channel] ``` 

# requirements
- python 3
- dryscrape library
``` pip3 install dryscrape```
# how use

```

usage: $ ace (url | id | arenavision channel) [-s | --server proxyserver] 

Launch a acestream url with vlc from command line using a custom acestream
proxy

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
```
