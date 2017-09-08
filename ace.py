#!/usr/bin/env python3

#imports
import sys, argparse, subprocess, socket, re, os, configparser
try:
    import dryscrape
except:
    print("Can't import dryscrape, please install it if you wan't run an arenavision channel directly")



# parse arguments
argparser = argparse.ArgumentParser(
    description="""Launch a acestream url with vlc from command line
    using a custom acestream proxy or generate a playable strm file""")

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
                        type=str, required=False)

argparser.add_argument("-f","--file",
                        help='''generate a playable strm file (useful for kodi)
                        for example: "ace 13 -f /home/ubuntu/media/mystream.strm''',
                        type=str, required=False)

# variables
av_baseurl = "http://arenavision.in/"
server = "127.0.0.1:8000"
player = "vlc"
config_file = "/etc/ace/default.cfg"
url = argparser.parse_args().url[0]
urlpattern = re.compile('^([0-9]|[a-z]){40}$', re.IGNORECASE)
idpattern = re.compile('^([0-9]){1,2}$', re.IGNORECASE)
linkpattern = re.compile('acestream://([0-9]|[a-z]){40,}', re.IGNORECASE)

#begin program
def filemode(url):
    if argparser.parse_args().file:
        filepath = argparser.parse_args().file
        if os.path.isfile(filepath):
            try:
                if not filepath.endswith(".strm"):
                    filepath = filepath + ".strm"
                with open(filepath, 'w') as f:
                    f.write(url)
                sys.exit(0)
            except Exception as e:
                print(e)
                print('''generation of strm file was failed''')
                sys.exit(1)
    else:
        pass

def process_config():
    try:
        global server
        global av_baseurl
        global player
        config = configparser.ConfigParser()
        config.read(config_file)
        server = config['default']['server']
        av_baseurl = config['default']['av_baseurl']
        player = config['default']['player']
    except Exception as e:
        print(e)
        print("WARNING config file not found or corrupt")

    if argparser.parse_args().server:
        try:
            server = argparser.parse_args().server.split(":")
        except Exception as e:
            print(e)
            print('ERROR, server syntax worng. Must be of kind "address:port"')
            sys.exit(1)
    else:
        server = os.environ.get('ACEPROXY_SERVER', server).split(":")
    server[1] = int(server[1])


# test if aceproxy server is reacheable
process_config()
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
    if int(url):
        if int(url) > 0 and int(url) < 10:
            url = "0" + url
    av_url = av_baseurl + url
    try:
        session = dryscrape.Session()
        session.visit(av_url)
        response = session.body()
        match = re.search(linkpattern, response)
        url = match.group(0)
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
    url = url.split("//")
    streamid = url[1]
    url = "http://" + server[0] + ":" + str(server[1]) + "/pid/" + streamid + "/stream.mp4"
    filemode(url)
    subprocess.Popen(['setsid', player, url], stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
elif re.match(urlpattern, url):
        url = "http://" + server[0] + ":" + str(server[1]) + "/pid/" + url + "/stream.mp4"
        filemode(url)
        subprocess.Popen(['setsid', player, url], stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
else:
    print('''ERROR, the url must be a valid acestream link, example: "ace acestream://r1oIk6lGyqEvE3BhJavj2goZTwDZUm9X7SMoAeL2"
    or a valid acestream id, for example: "ace r1oIk6lGyqEvE3BhJavj2goZTwDZUm9X7SMoAeL2"
    or a valid id channel of the Arenavision web (dryscrape library required), for example: "ace 14"''')
    sys.exit(1)

sys.exit(0)
