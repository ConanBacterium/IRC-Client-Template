__author__ = 'rohdehoved'

import socket
import threading

#basic stuff
server = "irc.freenode.net"
channel = "#u9j9h8d31dhakjb9"
botnick = "MegaBlaster_3000"

#Function for responding to pings to prevent timeouts
def ping():
    s.send("PONG :pingis\n")

#Function for sending message to irc server
def sendmsg(channel , msg):
    s.send("PRIVMSG "+ channel +" :"+ msg +"\n")


#Making the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("irc.freenode.net", 6667))

#Sending basic info to the socket
s.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :I have no idea what this is for :) \n") # user authentication
s.send("NICK "+ botnick +"\n") # here we actually assign the nick to the bot
s.send("JOIN "+ channel +"\n") #Joins channel

#Class (thread) that waits for input from the user and sends it as a privmsg to the irc channel
class userInputSender(threading.Thread):
     #CONSTRUCTAH!
    def __init__(self):
        threading.Thread.__init__(self)
    #Run method
    def run(self):
        while 1: #Keep doing this
            message = raw_input("> ")
            sendmsg(channel, message)

#Class (thread) that listens to the server and prints out whatever it receives from the server (and prevents timeout with ping/pong)
class serverListener(threading.Thread):
     #CONSTRUCTAH!
    def __init__(self):
        threading.Thread.__init__(self)
    #Run method
    def run(self):
        while 1: # Keep doing this 
            ircmsg = s.recv(2048) # receive data from the server
            ircmsg = ircmsg.strip('\n\r') # removing any unnecessary linebreaks.
            print ircmsg # Here we print what's coming from the server

            #PING/PONG, we don't wanna time-out
            if ircmsg.find("PING :") != -1: # if the server pings us then we've got to respond!
                ping()

thread1 = serverListener()
thread2 = userInputSender()

thread1.start()
thread2.start()