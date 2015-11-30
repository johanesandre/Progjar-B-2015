import sys
import socket
import io


HOST, PORT = '', 8888
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
# Bind the socket to the port
sock.bind((HOST,PORT))
sock.listen(1)
print 'starting up on port %s' % PORT
# sock.bind(server_address)

# Listen for incoming connections

while True:
    	# Wait for a connection
    	# print >>sys.stderr, 'waiting for a connection'
    	connection, client_address = sock.accept()
    	# print >>sys.stderr, 'connection from', client_address
    	# Receive the data in small chunks and retransmit it
    	# while True:
        data = connection.recv(1024)
	#print data   
	filename = data.split()
	#print filename[1]
	file1 =filename[1]	
	file2 =file1[1:]
	print file2
	#if file2 =="/" : 	
	#	f = open('android.jpg','r+')
	#	jpgdata = f.read()
	#	f.close()
	#	connection.send(outputdata[i])
	#	http_response = "\HTTP/1.1 200 OK \n\n%s"%jpgdata
	#else  : 
	f= open(file2+".jpg",'r+')
	jpgdata2 = f.read()
	f.close()
	http_response = "\HTTP/1.1 200 OK \n\n%s"%jpgdata2


		# print >>sys.stderr, 'received "%s"' % data
            	# if data:
                #	print >>sys.stderr, 'sending data back to the client'
                #	connection.sendall(data)
            	# else:
                #	print >>sys.stderr, 'no more data from', client_address
                #	break
        # Clean up the connection
	connection.sendall(http_response)
	connection.close()
