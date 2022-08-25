'''
Client side code: server client communication start from the client side.
Client request for detection result using a command Result
Then it will receive the detection result from the server and save the detection result in a folder called received_result
'''
import socket


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 4001))

BUFFER_SIZE = 4096
# input_data = input(" ->") # take input

while True:
    input_data = input("Please enter Result: ")
    if input_data == "Result":

        print("Connecting to server....")
        break
    else:
        print("\nThat is incorrect, please enter Result.\n")

input_data = bytes(input_data, 'utf-8')
client.send(input_data)

 ## Receive result from the server
with open('received_result/Detection_result.jpg', 'wb') as file:
    recv_data = client.recv(BUFFER_SIZE)

    while True:
        if recv_data == b'':
            print("Result received from the server")
            print("Please check the result under received_result folder, -- Thank you. ")
            break
        file.write(recv_data)
        recv_data = client.recv(BUFFER_SIZE)





