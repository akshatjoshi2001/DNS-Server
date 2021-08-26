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
	tran_id = message[0] + message[1]*2
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
	index = 12   # The 12th Octet of the message contains the length of the first domain part
	flag = True # Flag to break loop when we cross the end of the QNAME section
	domain_list = []  # Contains list of all parts of the domain. Eg. ['a','b','c'] is equiv to "a.b.c"
	q_type = 0   # The question type

	while(flag):		
		length = message[index]
		domain = ""

		for i in range(0,length):
			if((index+i+1) >= len(message)):   # Can happen in case of invalid message format
				break
			if(message[index+1+i] == 0):
				flag = False
				index = index+2+i
				break
			domain += str(chr(message[index+1+i]))   # Append ASCII character to domain string

		if(not flag):
			break

		index += length+1


		domain_list.append(domain)
	if(index+1<len(message)):
		q_type = message[index] +message[index+1]*2
	return (domain_list,q_type)




while True:
	message, address = s.recvfrom(1024)
	print(message)
	get_params(message)
	s.sendto(message,0,address)
s.close()

	
