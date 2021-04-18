# NetworkGUI.py
from tkinter import *
from tkinter import ttk
##############################
import socket
import time
import threading
import csv
from tkinter import messagebox


def ReadIP():
    with open('networkip.csv', newline='') as f:
        fr = csv.reader(f)
        result = list(fr)
    return result[0]


###########SETTING PORT############
try:
    global my_ip
    global port
    global serverip
    global port_server

    ipdata = ReadIP()
    print(ipdata)
    my_ip = ipdata[0]
    port = int(ipdata[1])

    serverip = ipdata[2]
    port_server = int(ipdata[3])
except:
    print('No IP')


# my_ip = '192.168.0.100'
# port = 7000

# serverip = '192.168.0.130'
# port_server = 7000
###########END############
def Runserver():
    while True:
        try:
            server = socket.socket()
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((my_ip, port))
            server.listen(1)

            print('Waiting for client..')

            client, addr = server.accept()
            print('Connect from: ', str(addr))

            data = client.recv(1024).decode('utf-8')
            print('Message from Client: ', data)

            ######collect data#######
            global allmessage2
            allmessage2.append(data)

            old_msg2 = ''

            message2 = allmessage2.copy()

            message2.reverse()

            if len(message2) < 9:

                for msg in message2:
                    old_msg2 = old_msg2 + '\n' + msg
            else:

                for msg in message2[:9]:
                    old_msg2 = old_msg2 + '\n' + msg

            #############

            v_result2.set(old_msg2)

            reply_msg = 'Hello we recieved'

            client.send(reply_msg.encode('utf-8'))
            client.close()
        except:

            messagebox.showerror('Not Found IP',
                                 'Plaese Set Ip and Restart Program')
            break


def ThreadRunserver():
    task1 = threading.Thread(target=Runserver)
    task1.start()


##############################


def SendtoServer(data):
    try:
        server = socket.socket()
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.connect((serverip, port_server))

        server.send(data.encode('utf-8'))
        data_server = server.recv(1024).decode('utf-8')
        print('Data from server: ', data_server)
        server.close()
    except:
        messagebox.showerror('ERROR',
                             'Connection Loss, Please Check Your Internet')


def ThreadSendtoServer(data):
    task2 = threading.Thread(target=SendtoServer, args=(data,))
    task2.start()


##############################
global allmessage1
allmessage1 = []

global allmessage2
allmessage2 = []


def SendData(event=None):
    global allmessage1

    text = v_message.get()
    print(text)

    allmessage1.append(text)

    old_msg = ''

    message = allmessage1.copy()

    message.reverse()

    if len(message) < 9:

        for msg in message:
            old_msg = old_msg + '\n' + msg
    else:

        for msg in message[:9]:
            old_msg = old_msg + '\n' + msg

    v_result1.set(old_msg)
    ThreadSendtoServer(text)


GUI = Tk()
GUI.geometry('400x400')
GUI.title('Network Command System')
FONT = ('Angsana New', 15)


########## MENU ############

def Popup():
    def WriteIP(ip1, port1, ip2, port2):
        with open('networkip.csv', 'w', newline='') as f:
            fw = csv.writer(f)
            fw.writerow([ip1, port1, ip2, port2])
        print('Done')

    def SetIP():
        try:
            WriteIP(v_ip1.get(), v_port1.get(), v_ip2.get(), v_port2.get())
            global my_ip
            global port
            global serverip
            global port_server

            ipdata = ReadIP()
            print('Current Data: ', ipdata)
            my_ip = ipdata[0]
            port = int(ipdata[1])

            serverip = ipdata[2]
            port_server = int(ipdata[3])
        except:
            print('Error')

    GUI2 = Toplevel()
    GUI2.geometry('300x300')
    GUI2.title('IP Setting')

    v_ip1 = StringVar()
    v_ip2 = StringVar()
    v_port1 = StringVar()
    v_port2 = StringVar()

    try:
        ipdata = ReadIP()
        v_ip1.set(ipdata[0])
        v_port1.set(ipdata[1])
        v_ip2.set(ipdata[2])
        v_port2.set(ipdata[3])
    except:
        print('Not Found IP')

    LB1 = ttk.Label(GUI2, text='My IP (cmd: ipconfig)').pack()
    EP1 = ttk.Entry(GUI2, textvariable=v_ip1)
    EP1.pack(pady=5)

    LB2 = ttk.Label(GUI2, text='My Port').pack()
    EP11 = ttk.Entry(GUI2, textvariable=v_port1)
    EP11.pack(pady=5)

    LB3 = ttk.Label(GUI2, text='Server IP (ask your server)').pack()
    EP2 = ttk.Entry(GUI2, textvariable=v_ip2)
    EP2.pack(pady=5)

    LB4 = ttk.Label(GUI2, text='Server Port').pack()
    EP22 = ttk.Entry(GUI2, textvariable=v_port2)
    EP22.pack(pady=5)

    BP1 = ttk.Button(GUI2, text='Set IP', command=SetIP)
    BP1.pack(ipadx=20, ipady=20)

    GUI2.mainloop()


mainmenu = Menu(GUI)
GUI.config(menu=mainmenu)

filemenu = Menu(mainmenu, tearoff=0)
filemenu.add_command(label='Setting IP', command=Popup)
mainmenu.add_cascade(label='File', menu=filemenu)

v_message = StringVar()
E1 = ttk.Entry(GUI, textvariable=v_message, font=FONT)
E1.pack(ipadx=50, pady=20)

B1 = ttk.Button(GUI, text='Send', command=SendData)
B1.pack(ipadx=20, ipady=10)

v_result1 = StringVar()
v_result1.set('---------')

v_result2 = StringVar()
v_result2.set('---------')

Result1 = ttk.Label(GUI, textvariable=v_result1, font=FONT)
Result1.place(x=20, y=150)

Result2 = ttk.Label(GUI, textvariable=v_result2, font=FONT)
Result2.place(x=200, y=150)

##############
E1.bind('<Return>', SendData)
ThreadRunserver()
GUI.mainloop()