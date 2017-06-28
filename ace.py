#!/usr/bin/env python3

#imports
import sys, argparse, subprocess, socket, re
try:
    import dryscrape
except:
    print("Can't import dryscrape, please install it if you wan't run an arenavision channel")

# parse arguments
argparser = argparse.ArgumentParser(
    description="""Launch a acestream url with vlc from command line
    using a custom acestream proxy""",
    usage="$ ace (url | id | arenavision channel) [-s | --server proxyserver] ")

argparser.add_argument("url",
                        help='''valid acestream id or url acestream, for example:
                        "ace acestream://r1oIk6lGyqEvE3BhJavj2goZTwDZUm9X7SMoAeL2" or
                        "ace r1oIk6lGyqEvE3BhJavj2goZTwDZUm9X7SMoAeL2"
                        You can put an id channel from Arenavision web (dryscrape library required), for example:
                        "ace 14"''',
                        type=str, nargs=1)
argparser.add_argument("-s","--server",
                        help='''aceproxy server with format: "server:port", for example:
                        "--server myaceproxyserver:8080" or "-s 192.168.1.25:8000"
                        by default is "127.0.0.1:8080"''',
                        type=str, required=False, default="127.0.0.1:8080")


# variables
player="vlc"
url=argparser.parse_args().url[0]
server=argparser.parse_args().server.split(":")
server[1]=int(server[1])
urlpattern=re.compile('^([0-9]|[a-z]){40}$', re.IGNORECASE)
idpattern=re.compile('^([0-9]){1,2}$', re.IGNORECASE)
linkpattern=re.compile('acestream://([0-9]|[a-z]){40,}', re.IGNORECASE)
av_baseurl="https://arenavision.in/av"

#begin program

# test if aceproxy server is reacheable
conntest = socket.socket()
try:
	conntest.connect(tuple(server))
except socket.error as e:
    print("Connection to aceproxy: %s failed: %s" % (str(server), e))
    print("Is aceproxy running and reacheable?")
    sys.exit(1)
conntest.close()

# check if arg is a id channel, in this case, scrap arenavision web and get url stream
if re.match(idpattern, url):
    av_url=av_baseurl + url
    try:
        session = dryscrape.Session()
        session.visit(av_url)
        response = session.body()
        match=re.search(linkpattern, response)
        url=match.group(0)
    except Exception as e:
        print(e)
        print('''Can't get the url form Arenavision Web,
        maybe the id channel is wrong?
        is dryscrape library installed?
        Remember: without dryscraper, channel id mode isn't available.
        Try to run this program
        with acestream id or acestream url''')
        sys.exit(1)

# check if arg is an complete url or acestream id, make the final url and launch vlc
if url.startswith("acestream://"):
    url=url.split("//")
    streamid=url[1]
    url="http:// " + server[0] + ":" + str(server[1]) + "/" + streamid + "/stream.mp4"
    subprocess.Popen(['setsid', player, url], stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
elif re.match(urlpattern, url):
        url="http:// " + server[0] + ":" + str(server[1]) + "/" + url + "/stream.mp4"
        subprocess.Popen(['setsid', player, url], stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
else:
    print('''ERROR, the url must be a valid acestream link, example: "ace acestream://r1oIk6lGyqEvE3BhJavj2goZTwDZUm9X7SMoAeL2"
    or a valid acestream id, for example: "ace r1oIk6lGyqEvE3BhJavj2goZTwDZUm9X7SMoAeL2"
    or a valid id channel of the Arenavision web (dryscrape library required), for example: "ace 14"''')
    sys.exit(1)

sys.exit(0)
