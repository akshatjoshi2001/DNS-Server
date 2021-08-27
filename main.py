import socket
print("Server starting..")
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(("0.0.0.0",53))

print("Server started.")



def get_params(message):
	print("Request recieved. Details:")
	print(get_header_params(message))
	print(get_question_params(message))
	print("--------------------------\n\n")

''' Get the parameters in the header section of the DNS request '''
def get_header_params(message):
	tran_id = (message[0]<<1) + message[1]
	rd = (message[2]>>0)&1
	tc = (message[2]>>1)&1
	aa = (message[2]>>2)&1
	opcode = (message[2]>>3)&1 + ((message[2]>>4)&1)*2 + ((message[2]>>5)&1)*4 + ((message[2]>>6)&1)*8
	qr = message[2]>>7
	rcode = (message[3]>>0)&1 +((message[3]>>1)&1)<<1 + ((message[3]>>2)&1)<<2 + ((message[3]>>3)&1)<<3
	ra = (message[3]>>7)&1

	return (tran_id,rd,tc,aa,opcode,qr,rcode,ra)




''' Get the parameters in the question section of the DNS request '''
def get_question_params(message):
	domain2 = []
	qname = get_domain(12,domain2)  # Fetch the domain with labels/pointers starting at 12 (takes care of compression)
	index = -1  # Get the byte index for QTYPE field
	for i in range(12,len(message)):
		if(message[i] == 0):
			index = i+1
			break
		elif(message[i]>=192):
			index = i+2
			break
	qtype = (message[index]<<1) + (message[index+1])
	qclass = (message[index+2]<<1) + (message[index+3])
	
	return (qname,qtype,qclass)






def get_domain(start,domain=[]):
	index = start
	
	if((message[index]) >= 192):
		print("Detected compression")
		return get_domain((message[index]<<1)+(message[index+1])-192)
	else:
		length = message[index]
		label = ""
		for i in range(0,length):
			label += str(chr(message[index+i+1]))
		domain.append(label)
		
		if(message[index+length+1] == 0):
			return domain	
		return get_domain(index+length+1,domain)







while True:
	message, address = s.recvfrom(1024)
	
	get_params(message)
	s.sendto(message,0,address)
s.close()

	
