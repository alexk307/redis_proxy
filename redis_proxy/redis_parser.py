class RedisParser(object):
    """
    Class to parse RESP http://redis.io/topics/protocol
    """

    def parse(self, string):
        """
        Parses raw RESP into readable Redis commands
        :param string: Raw RESP command
        :return: Human readable Redis command
        """
        string = string.split('\r\n')
        first_char = string[0][0]

        if first_char == '*':
            return self.parse_array(string)
        elif first_char in ['-', '+', ':']:
            return self.parse_simple(string)
        elif first_char == '$':
            return self.parse_bulk_string(string)
        else:
            raise RedisParserException()

    def parse_array(self, string):
        """
        Parses RESP array responses
        """
        size_of_array = int(string[0][1:])
        command_list = [string[2:][i*2] for i in range(size_of_array)]
        return RedisCommand(command_list[0], command_list[1:])

    def parse_simple(self, string):
        """
        Parses simple responses (integers, errors, simple strings)
        """
        return RedisCommand(string[:1][0][1:])

    def parse_bulk_string(self, string):
        """
        Parses bulk string responses
        """
        return RedisCommand(string[1])


class RedisCommand(object):

    def __init__(self, command, *args):
        self.command = command
        self.args = args

class RedisParserException(Exception):
    pass
