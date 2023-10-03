import socket
import pickle
from constants import ADDRESS, PORT

class Network:
    """Class that represents a client conection with the server
    """

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (ADDRESS, PORT)
        self.p = self.connect()

    def getP(self):
        """Get the player id

        Returns:
            int: Player id
        """
        return self.p

    def connect(self):
        """Connect to the server

        Returns:
            int: Player id of the client sent by server
        """
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        """Send data to the server and receive the response

        Args:
            data (str): Client status

        Returns:
            Game : The Game instance sent by the server 
        """
        try:
            self.client.send(str.encode(data))
            
            return pickle.loads(self.client.recv(2048*3))
        except socket.error as e:
            print(e)

