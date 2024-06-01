import opensearchpy
from opensearchpy import OpenSearch


def opensearch_connect(host,username,password,user):
    auth = (username,password)
    client = OpenSearch(hosts=host,http_auth=auth,use_ssl=True,verify_certs=True)
    return client.sec
if __name__=="__main__":
      username = "admin"
      password = "secret"
      host = "https://search-domain1-jra4uodezy2er3gfujfnt5csxi.us-east-1.es.amazonaws.com"
      user = "os-readonly"
      os=opensearch_connect(host,username,password,user)