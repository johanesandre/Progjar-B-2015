import sys
import socket
import select
import pickle 
import time
import string
 
def chat_client():

	host = '127.0.0.1' #localhost	
    # create TCP/IP socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     
    # connect to remote host
	try :
		s.connect((host, 3636))
	except :
		print 'Gagal Connect'
		sys.exit()
     
	print 'Client sudah terhubung,silahkan chat'
	sys.stdout.write('>> '); sys.stdout.flush()
     
	while 1:
		socket_list = [sys.stdin, s]
		 
		# Get the list sockets which are readable
		ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
		 
		for sock in ready_to_read:      
		
			if sock == s:
				# incoming message from remote server, s
				data = sock.recv(4096)
				if not data :
					print '\nAnda Disconnect'
					sys.exit()
				else :
					#print data
					sys.stdout.write(data)
					sys.stdout.write('>> '); sys.stdout.flush()     
			
			else :
				# user entered a message
				msg = []
				temp = sys.stdin.readline()
				temp1 = string.split(temp[:-1])
				
				d=len(temp1)
				if temp1[0]=="login" :
					if d>2:
						print('Username Hanya boleh 1 kata aja')
					elif d<2:
						print('Masukkan username untuk login')
					else:
						s.send(temp) #kalo bener ngirim ke socket server
						
				elif temp1[0]=="send" :
					if d<3:
						print('Perintah salah')
					else:
						s.send(temp)
						
				elif temp1[0]=="sendall" :
					if d<2:
						print("Perintah salah")
					else:
						s.send(temp)
						
				elif temp1[0]=="list" :
					if d>1:
						print('Lakukan login terlebih dulu')
					else:
						s.send(temp)		
				else:
					print ('Perintah salah')
				
				#s.send(temp)
				sys.stdout.write('>> '); sys.stdout.flush() 


chat_client()
