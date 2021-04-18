import socket
from uncleengineer import thaistock

my_ip = "192.168.0.170"
port = 5000

while True:
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((my_ip, port))
    server.listen(1)

    print("waiting for client...")

    client, addr = server.accept()
    print("Connect from:", client)

    data = client.recv(1024).decode("utf-8")
    print("Message from client:", data)

    try:
        my_stock = thaistock(data)
        resp = "Stock: {} Price: {}".format(my_stock[0], my_stock[1])
    except:
        resp = "No stock DATA"

    client.send(resp.encode("utf-8"))
    client.close()

