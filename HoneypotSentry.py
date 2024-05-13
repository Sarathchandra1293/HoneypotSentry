import tkinter as tk
import requests
import sys
from socket import *
import socket
import logging
import os
import time
import atexit
from termcolor import colored, cprint
import threading
from threading import Thread
from _thread import *
import time
import pygame
from winotify import Notification, audio
import subprocess

user_dict = 0
server_lstnr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

toast = Notification(app_id="HoneyPot Alert",
                     title="Malicious Activity Detected",
                     msg="Location:",
                     duration="long",
                     icon=r"C:\Users\Sarath chandra\Desktop\works\amrita_logo.jpg")

def HoneypotSentry_popup():
    pygame.init()

    alert_sound = pygame.mixer.Sound('alarm.mp3')
    
    popup = tk.Tk()
    popup.title("Attack")
    
    width = 400
    height = 200
    
    # Get the screen width and height
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    
    # Calculate the position of the window to center it on the screen
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    # Set the geometry of the window
    popup.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    label = tk.Label(popup, text="\nAttack\n", fg="red")
    label.pack(pady=20)

    label = tk.Label(popup, text="\nMalicious Activity Detected", fg="blue")
    label.pack(pady=10)
    def stop_audio():
        alert_sound.stop()
    
    def open_log_file():
        stop_audio()
        subprocess.Popen(["notepad.exe", "log.txt"])
        popup.destroy()
    
    button = tk.Button(popup, text="LOG", command=lambda: [open_log_file(), popup.destroy])
    button.pack(pady=10)
    
    alert_sound.play()
    popup.mainloop()

def exit_handler():
    print ('\n[*] Honeypot is shutting down!')
    server_lstnr.close()

def writeLog(clt, data='', user='', pas='', client_ip='', location_data=''):
    separator = '=' * 50
    with open('./log.txt', 'a', encoding='utf-8') as fopen:
        fopen.write('Time: %s\nIP: %s\nPort: %d\nData: %s\n' % (time.ctime(), clt[0], clt[1], data))
        fopen.write('Username is:%s\nPassword is:%s\n\n%s\n' % (user, pas, separator))
        fopen.write('Client IP Address: %s\n' % (client_ip))
        if isinstance(location_data, dict):
            location_str = ", ".join([f"{key}: {value}" for key, value in location_data.items()])
            fopen.write('Location: %s\n' % (location_str.encode('utf-8')))
        else:
            fopen.write('Location: %s\n' % (location_data))
        fopen.write('=' * 50 + '\n')



def storeCommands(user_cmd,ip):
	fopen = open('./log.txt', 'a')
	fopen.write('%s->%s'%(user_cmd,ip))
	fopen.write('\n')
	fopen.close()


def sendCommands(fromip, message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((RHOST, RPORT))
    s.send('IP:' , fromip , ' Port:' , str(port) , ' | ' , message.replace('\r\n', ' '))
    s.close()

def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

def cat_command(file,inp_cmd,c):
	if('Password.txt' in str(file) and inp_cmd==7):
		data = '\n Cyber_Forensics@123 \n Amma@123\n Fraud@17 \n IamnotPassword'
		c.sendall(bytes(data,'utf-8'))


def commandLS(inp_cmd):
	if(inp_cmd==0):
		return 'Desktop\t\tDocuments\t\tDownloads\t\tPictures\t\tPublic\t\tVideos\t\tDatabase'
	elif(inp_cmd==1):
		return 'confidential.rar'
	elif(inp_cmd==2):
		return 'clientinfo.txt'
	elif(inp_cmd==3):
		return 'wallpaper.jpeg'
	elif(inp_cmd==4):
		return 'tree.jpeg\tsnip.jpeg'
	elif(inp_cmd==5):
		return ''
	elif(inp_cmd==6):
		return 'transaction.mp4\tvisit.mp4'
	elif(inp_cmd==7):
		return 'Password.txt\tAccount_Database'

def sendCmds(inp_cmd,c):
	if(inp_cmd==0):
		cmd_prompt=colored(255, 0, 0, '\n┌──(root@user)-[/home/user]└─#')
	elif(inp_cmd==1):
		cmd_prompt=colored(255, 0, 0, '\n┌──(root@user)-[/home/user/Desktop]└─#')
	elif(inp_cmd==2):
		cmd_prompt=colored(255, 0, 0, '\n┌──(root@user)-[/home/user/Documents]└─#')
	elif(inp_cmd==3):
		cmd_prompt=colored(255, 0, 0, '\n┌──(root@user)-[/home/user/Downloads]└─#')
	elif(inp_cmd==4):
		cmd_prompt=colored(255, 0, 0, '\n┌──(root@user)-[/home/user/Pictures]└─#')
	elif(inp_cmd==5):
		cmd_prompt=colored(255, 0, 0, '\n┌──(root@user)-[/home/user/Public]└─#')
	elif(inp_cmd==6):
		cmd_prompt=colored(255, 0, 0, '\n┌──(root@user)-[/home/user/Videos]└─#')
	elif(inp_cmd==7):
		cmd_prompt=colored(255, 0, 0, '\n┌──(root@user)-[/home/user/Databse]└─#')
	c.sendall(bytes(cmd_prompt,'utf-8'))

	
def HoneypotSentryAct(c):
	print("\nAttack\n")
	data=cprint('\nMalicious Activity Detected', 'blue', attrs=['blink'])

	toast.show()
	HoneypotSentry_popup()
	print("\n Logged attacker activity")
	while True:
		new=1


def cmdTerm(user_cmd,c,user_dict):

	if('ls' in str(user_cmd)):

		lsdir=commandLS(user_dict)
		lsdir=colored(141,182,205,lsdir)#lsdir
		c.sendall(bytes(lsdir,'utf-8'))
		sendCmds(0,c)
	elif('cd Desktop' in str(user_cmd)):
		user_dict=1
		sendCmds(1,c)

	elif('cd Documents' in str(user_cmd)):
		user_dict=2
		sendCmds(2,c)

	elif('cd Downloads' in str(user_cmd)):
		user_dict=3
		sendCmds(3,c)

	elif('cd Pictures' in str(user_cmd)):
		user_dict=4
		sendCmds(4,c)

	elif('cd Public' in str(user_cmd)):
		user_dict=5
		sendCmds(5,c)

	elif('cd Videos' in str(user_cmd)):
		user_dict=6
		sendCmds(6,c)

	elif('cd Database' in str(user_cmd)):
		user_dict=7
		sendCmds(7,c)
	elif('cat Password.txt' in str(user_cmd)):
		user_dict=7
		cat_command('Password.txt',user_dict,c)
		sendCmds(7,c)

	elif('rm Password.txt' in str(user_cmd)):
		sendCmds(7,c)
		HoneypotSentryAct(c)
		
	elif('cd Account_Database' in str(user_cmd) and user_dict==7):#redirect to Database user_dict
		user_dict=-1
		HoneypotSentryAct(c)
		
	elif('cd ..' in str(user_cmd) or 'cd' in str(user_cmd)):
		user_dict=0
		sendCmds(0,c)
	elif('whoami' in str(user_cmd) or 'cd ~' in str(user_cmd)):
		data=colored(255, 0, 0,'root')
		c.sendall(bytes(data,'utf-8'))		
		sendCmds(user_dict,c)
	elif('install' in str(user_cmd)):
		c.sendall(bytes('E: Could not get lock /var/lib/dpkg/lock - open(11:Resource temporarily unavailable)\n','utf-8'))		
		sendCmds(user_dict,c)

	else:
		c.sendall(bytes('Command not found','utf-8'))
		sendCmds(user_dict,c)

	return user_dict

def charRemove(clt_name):
	clt_list = list(str(clt_name))
	clt_list[0]=''
	clt_list[1]=''
	clt_list[-1]=''
	clt_list[-2]=''
	clt_list[-3]=''
	clt_list[-4]=''
	clt_list[-5]=''

	''.join(clt_list)
	user=""
	for x in clt_list:
		user+=x

	return user

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.RequestException:
        return None

sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host='192.168.182.30'
port=23
default_user='user'
default_pas='Password'
display='Kali login:'
display1='Password:'
RHOST = '192.168.246.152'
RPORT = 9000

atexit.register(exit_handler)
server_lstnr.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_lstnr.bind((host, port))
++32
100
server_lstnr.listen(10)

def get_location(ip_address, api_token):
    url = f'https://ipinfo.io/{ip_address}/json?token={api_token}'
    response = requests.get(url)
    data = response.json()
    return data

def threaded_client(c):
	c.sendall(bytes('Kali GNU/Linux Rolling\n','utf-8'))
	c.sendall(bytes('(','utf-8'))
	c.sendall(bytes(host,'utf-8'))
	c.sendall(bytes(') :anonymous\n','utf-8'))

	# Get client IP address
	client_ip = client_public_ip #c.getpeername()[0]
	location_data = get_location(client_ip, '27cd62f09fc14c')  # Replace with your actual API token
	print(location_data)  # You can print or log this information as needed

	user_dict=0
	cnt_check=1
	while True:
		c.sendall(bytes(display,'utf-8'))
		
		if(cnt_check==1): 
			c.recv(1024)
			cnt_check=2

		clt_name=c.recv(1024)
		c.sendall(bytes(display1,'utf-8'))
		clt_pass=c.recv(1024)
		clt_name=charRemove(clt_name)
		clt_pass=charRemove(clt_pass)

		writeLog(addr,addr,clt_name,clt_pass,client_ip,location_data)



		print(clt_name)
		print(clt_pass)

		if('admin' in str(clt_name) and 'admin' in str(clt_pass)):
			c.sendall(bytes('You are getting in the system.\n','utf-8'))
			sendCmds(0,c)
			user_dict=0
			while True:
				user_cmd=c.recv(1024)
				user_cmd=charRemove(user_cmd)
				storeCommands(user_cmd,addr)
				user_dict=cmdTerm(user_cmd,c,user_dict)#second argument for socket

			break
		else:
			c.sendall(bytes('Authentication Failed\n','utf-8'))
	c.close()

while True:
	getClt,addr=server_lstnr.accept()
	print("Connection Established with IP Address: ",addr)
	client_public_ip = get_public_ip()
	if client_public_ip:
		print("Client's Public IP Address:", client_public_ip)
	else:
		print("Failed to retrieve client's public IP address")
        
	start_new_thread(threaded_client, (getClt, ))


print("Weldone")
server_lstnr.close()