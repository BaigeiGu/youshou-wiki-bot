from string import Template

import Config
from mwclient import Site


def login(host=Config.HOST, 
          path=Config.WIKIPATH, 
          isHTTP=Config.HTTP, 
          ua=Config.BOTUA,
          username=Config.USERNAME,
          password=Config.PASSWORD) -> Site:
    if isHTTP == True:
        site = Site(host, path, clients_useragent=ua,
                    scheme='http')
    else:
        site = Site(host, path, clients_useragent=ua)
    site.login(username, password)

    return site

def generate_wikitext(template_path, data) -> str:
    with open(template_path, encoding='UTF-8') as f:
        template = Template(f.read())
    t = template.safe_substitute(data)
    return t