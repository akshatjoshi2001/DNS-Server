import socket
print("Server starting..")
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(("0.0.0.0",53))

print("Server started.")


def get_params(message):
	index = 12
	flag = True
	domain_list = []
	q_type = 0
	while(flag):
		
		length = message[index]
		domain = ""
		

		for i in range(0,length):
			if((index+i+1) >= len(message)):
				break
			if(message[index+1+i] == 0):
				flag = False
				index = index+2+i
				break
			domain += str(chr(message[index+1+i]))
		if(not flag):
			break

		index += length+1


		domain_list.append(domain)
	if(index+1<len(message)):
		q_type = message[index] +message[index+1]*2
	print((domain_list,q_type))




while True:
	message, address = s.recvfrom(1024)
	print(message)
	get_params(message)
	s.sendto(message,0,address)
s.close()

	
