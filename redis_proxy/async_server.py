import asyncio
import socket
from redis_parser import RedisParser
from settings import SERVERS, PROXY_HOST, PROXY_PORT, RECV_SIZE


class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        self.transport = transport

    def data_received(self, data):
        message = data.decode()

        parser = RedisParser()
        parsed_command = parser.parse(message)

        # Make request to redis
        response_from_redis = self.forward_to_redis(data)

        # Return response from redis to client
        self.transport.write(response_from_redis)

        # Close the socket
        self.transport.close()

    def forward_to_redis(self, data):
        """
        Forwards raw RESP to Redis instance
        :param data: raw RESP data
        :return: Response from Redis instance
        """
        address, port = self.determine_redis_instance(data)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((address, int(port)))
        s.send(data)
        response = s.recv(RECV_SIZE)
        s.close()
        return response

    def determine_redis_instance(self, command):
        """
        Determines which redis instance to use
        :param command: Raw RESP request
        :return: (address, port) tuple of instance to use
        """
        return tuple(SERVERS[hash(command) % len(SERVERS)].split(':'))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # Each client connection will create a new protocol instance
    coro = loop.create_server(EchoServerClientProtocol, PROXY_HOST, PROXY_PORT)
    server = loop.run_until_complete(coro)

    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
