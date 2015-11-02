import sys
import socket
import select
import pickle
import string

HOST = 'localhost' 
SOCKET_LIST = []
NAME_LIST = []
RECV_BUFFER = 4096 
PORT = 3636
def chat_server():

	
	#creating TCP/IP socket
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	# bxinding the socket
	server_socket.bind((HOST, PORT))
	server_socket.listen(10)

	# add server socket object to the list of readable connections
	SOCKET_LIST.append(server_socket)

	print "Chat server dimulai dengan port " + str(PORT)
	#print "and the Host is " + str(HOST)

	while True:
		# get the list sockets which are ready to be read through select
		# 4th arg, time_out  = 0 : poll and never block
		ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
	  
		for sock in ready_to_read:
			# when new connection request received
			if sock == server_socket: 
				sockfd, addr = server_socket.accept()
				SOCKET_LIST.append(sockfd)
				print "Client (%s, %s) tersambung" % addr
				 
				#broadcast(server_socket, sockfd, "[%s:%s] has joined the chat\n" % addr)
			 
			# a message from a client, not a new connection
			else:
				# process data received from client, 
				try:
					# receiving data from the socket.
					data = sock.recv(RECV_BUFFER)
					#data = pickle.loads(data)
					if data:
						#broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)  
						#pemisah command dan message
						temp1 = string.split(data[:-1])
						d=len(temp1) #panjangnya temp1
						#pengecekan index pertama yg berupa command , kalau bener masuk ke fungsi2
						if temp1[0]=="login" :
							log_in(sock, str(temp1[1]))	
						elif temp1[0]=="send" :
							logged = 0 #cek apa sudah login
							user = ""
							#x merupakan iterator sebanyak banyaknya isi array name_list
							for x in range (len(NAME_LIST)):
								#kalau alamat kita sudah ada di name_list jadi kamu sudah login
								if NAME_LIST[x]==sock:
									logged=1
									#masukkan nama user yang diinputkan ke variabel user
									user=NAME_LIST[x+1] #name_list itu adalah array,alokasi array di sini selalu Alamat,nama,alamat nama..makanya + 1
							#kalau belom login
							if logged==0:
								send_msg(sock, "Login diperlukan\n")
							#kalau sudah login
							else:
								temp2=""
								for x in range (len(temp1)):
									if x>1: #maksudnya command/kata ke 2 yang berupa perintah yang dikirim 
									#jika temp2 masih kosong, temp2 diisi kata index ke 2 dari temp1
										if not temp2:
											temp2+=str(temp1[x])
										#jika temp2 sudah ada isinya(kirim psn panjang) alamat brikutnya diisi spasi
										else:
											temp2+=" "
											temp2+=str(temp1[x])
								#buat ngirim ke user yang menjadi target
								for x in range (len(NAME_LIST)):
									#temp1[1] nama target yang mau dikirim message
									if NAME_LIST[x]==temp1[1]:
										send_msg(NAME_LIST[x-1], "["+user+"] : "+temp2+"\n")
								
						elif temp1[0]=="sendall" :
							
							logged = 0
							user = ""
							for x in range (len(NAME_LIST)):
								if NAME_LIST[x]==sock:
									logged=1
									user=NAME_LIST[x+1]
							
							if logged==0:
								send_msg(sock, "Login diperlukan\n")
							
							else:
								temp2=""
								for x in range(len(temp1)):
									
										if not temp2:
											temp2=str(temp1[x])
										else:
											temp2+=" "
											temp2+=temp1[x]
								#broadcast itu seperti codingan seblum nya, ngirim ke semua user
								broadcast(server_socket, sock, "["+user+"] : "+temp2+"\n")
						#lihat list user yang terconnect
						elif temp1[0]=="list" :
							logged = 0
							for x in range (len(NAME_LIST)):
								if NAME_LIST[x]==sock:
									logged=1
							
							if logged==0:
								send_msg(sock, "Login diperlukan\n")
							
							else:
								temp2=""
								for x in range (len(NAME_LIST)):
									#nyari  nama dari array name_list yang berada di index ganjil
									if x%2==1:
										temp2+=" "
										temp2+=str(NAME_LIST[x])
								send_msg(sock, "[List_User] : "+temp2+"\n")
						else:
							print ('Perintah salah')
					else:
						# remove the socket that's broken    
						if sock in SOCKET_LIST:
							SOCKET_LIST.remove(sock)

						# at this stage, no data means probably the connection has been broken
						broadcast(server_socket, sock, "Client (%s, %s) offline\n" % addr) 

				# exception 
				except:
					broadcast(server_socket, sock, "Client (%s, %s)  offline\n" % addr)
					continue

	server_socket.close()
    
# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, message):
    for x in range (len(NAME_LIST)):
		
        # send the message only to peer
        if NAME_LIST[x] != server_socket and NAME_LIST[x] != sock and x%2==0 :
            try :
                NAME_LIST[x].send(message)
            except :
                # broken socket connection
                NAME_LIST[x].close()
                # broken socket, remove it
                if NAME_LIST[x] in SOCKET_LIST:
                    SOCKET_LIST.remove(NAME_LIST[x])
 
def send_msg (sock, message):
	try:
		sock.send(message)
	except:
		sock.close()
		
		if sock in SOCKET_LIST:
			SOCKET_LIST.remove(sock)

def log_in (sock, user):
	cekuser = 0
	ceklogin = 0
	for name in NAME_LIST:
		if name == user:
			cekuser = 1
		if name == sock:
			ceklogin = 1
	
	if ceklogin==1:
		send_msg(sock, "Anda Sudah login\n")
	elif cekuser==1:
		send_msg(sock, "Username sudah dipakai\n")
	else:
		#masukkan data user ke array
		NAME_LIST.append(sock)
		NAME_LIST.append(user)
		send_msg(sock, "Login berhasil\n")
	
chat_server()
xxx
