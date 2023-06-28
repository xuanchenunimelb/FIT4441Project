from client import Client


if __name__ == '__main__':
    client  = Client()
    root = client.update("1","cat","111")
    root = client.update("1","cat","222")
    root = client.update("1","cat","333")
    root = client.update("1","cat","444")
    root = client.update("0","cat","111")
