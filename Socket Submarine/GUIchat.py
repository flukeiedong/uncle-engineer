from tkinter import *
from tkinter import ttk
import socket
import threading


all_message = []


def run_server():
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

        all_message.append(data)

        resp = "We Received"

        client.send(resp.encode("utf-8"))
        client.close()


def send_to_server():
    server_ip = "192.168.0.100"
    port = 7000

    data = v_message.get()

    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.connect((server_ip, port))

    server.send(data.encode("utf-8"))

    data_server = server.recv(1024).decode("utf-8")
    print("Data from server: ", data_server)

    all_message.append(data_server)

    try:
        textshow = ""
        if len(all_message) >= 5:
            for m in all_message[-5:]:
                textshow += m + "\n"
        else:
            for m in all_message:
                textshow += m

        v_result2.set(textshow)
    except:
        print("Something wrong!")

    server.close()


def send(event=None):
    text = v_message.get()
    v_result.set(text)
    task2 = threading.Thread(target=send_to_server)
    task2.start()


task1 = threading.Thread(target=run_server)
task1.start()

GUI = Tk()
GUI.geometry("1000x500")
GUI.title("Chat Submarine")


FONT = ("Angsana New", 18)

# Input
v_message = StringVar()
message = ttk.Entry(GUI, textvariable=v_message, font=FONT, width=70)
message.pack()

# Button
send_bt = ttk.Button(GUI, text="Send Message", command=send)
send_bt.pack()

# Label left
v_result = StringVar()
v_result.set("-----RESULT-----")
result = ttk.Label(GUI, textvariable=v_result, font=FONT, width=55)
result.pack()
result.place(x="250", y="200")

# Label right
v_result2 = StringVar()
v_result2.set("-----RESULT-----")
result2 = ttk.Label(GUI, textvariable=v_result2, font=FONT, width=55)
result2.pack()
result2.place(x="500", y="200")


GUI.bind("<Return>", send)

GUI.mainloop()

