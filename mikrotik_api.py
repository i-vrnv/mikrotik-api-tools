#!/usr/bin/python
# get from https://wiki.mikrotik.com/wiki/Manual:API

import sys, posix, time, binascii, socket, select, hashlib, mikrotik_backup, mikrotik_device


class ApiRos(object):
    """
    Routeros API
    """

    def __init__(self, sock):
        self.sock = sock
        self.current_tag = 0

    def login(self, username, pwd):
        chal = None

        for repl, attrs in self.talk(["/login"]):
            chal = binascii.unhexlify(attrs['=ret'])
        md = hashlib.md5()
        md.update('\x00')
        md.update(pwd)
        md.update(chal)
        self.talk(["/login", "=name=" + username,
                   "=response=00" + binascii.hexlify(md.digest())])

    def talk(self, words):
        if self.write_sentence(words) == 0:
            return
        r = []
        while True:
            i = self.read_sentence()
            if len(i) == 0:
                continue
            reply = i[0]
            attrs = {}
            for w in i[1:]:
                j = w.find('=', 1)
                if j == -1:
                    attrs[w] = ''
                else:
                    attrs[w[:j]] = w[j + 1:]
            r.append((reply, attrs))
            if reply == '!done':
                return r

    def write_sentence(self, words):
        ret = 0
        for w in words:
            self.write_word(w)
            ret += 1
        self.write_word('')
        return ret

    def read_sentence(self):
        r = []
        while True:
            w = self.read_word()
            if w == '':
                return r
            r.append(w)

    def write_word(self, w):
        # Uncomment to debug
        print "<<< " + w
        self.write_len(len(w))
        self.write_str(w)

    def read_word(self):
        ret = self.read_str(self.read_len())
        # Uncomment to debug
        print ">>> " + ret
        return ret

    def write_len(self, l):
        if l < 0x80:
            self.write_str(chr(l))
        elif l < 0x4000:
            l |= 0x8000
            self.write_str(chr((l >> 8) & 0xFF))
            self.write_str(chr(l & 0xFF))
        elif l < 0x200000:
            l |= 0xC00000
            self.write_str(chr((l >> 16) & 0xFF))
            self.write_str(chr((l >> 8) & 0xFF))
            self.write_str(chr(l & 0xFF))
        elif l < 0x10000000:
            l |= 0xE0000000
            self.write_str(chr((l >> 24) & 0xFF))
            self.write_str(chr((l >> 16) & 0xFF))
            self.write_str(chr((l >> 8) & 0xFF))
            self.write_str(chr(l & 0xFF))
        else:
            self.write_str(chr(0xF0))
            self.write_str(chr((l >> 24) & 0xFF))
            self.write_str(chr((l >> 16) & 0xFF))
            self.write_str(chr((l >> 8) & 0xFF))
            self.write_str(chr(l & 0xFF))

    def read_len(self):
        c = ord(self.read_str(1))
        if (c & 0x80) == 0x00:
            pass
        elif (c & 0xC0) == 0x80:
            c &= ~0xC0
            c <<= 8
            c += ord(self.read_str(1))
        elif (c & 0xE0) == 0xC0:
            c &= ~0xE0
            c <<= 8
            c += ord(self.read_str(1))
            c <<= 8
            c += ord(self.read_str(1))
        elif (c & 0xF0) == 0xE0:
            c &= ~0xF0
            c <<= 8
            c += ord(self.read_str(1))
            c <<= 8
            c += ord(self.read_str(1))
            c <<= 8
            c += ord(self.read_str(1))
        elif (c & 0xF8) == 0xF0:
            c = ord(self.read_str(1))
            c <<= 8
            c += ord(self.read_str(1))
            c <<= 8
            c += ord(self.read_str(1))
            c <<= 8
            c += ord(self.read_str(1))
        return c

    def write_str(self, string):
        n = 0
        while n < len(string):
            r = self.sock.send(string[n:])
            if r == 0:
                raise RuntimeError("connection closed by remote end")
            n += r

    def read_str(self, length):
        ret = ''
        while len(ret) < length:
            s = self.sock.recv(length - len(ret))
            if s == '':
                raise RuntimeError("connection closed by remote end")
            ret += s
        return ret

    def parse_out(self):
        """
        Parse output after write_sentence
        :return: dictionary
        """
        r = select.select([self.sock], [], [], None)
        while self.sock in r[0]:
            # Something to read in socket, read sentence
            output_data = self.read_sentence()
            # Read result, return '!done' if all ok
            # output_status = self.read_sentence()

            # Dictionary for return
            output = {}

            # Check return status, if "!re" command executed correct
            if output_data[0] == "!re":
                # Read output lines
                for line in output_data[1:]:
                    line = str(line).split('=')[1:]
                    output[line[0]] = line[1]
                # Return dictionary
                return output

    def execute(self, command):
        self.write_sentence(command)
        return self.parse_out()


def main():
    # Create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((sys.argv[1], 8728))

    # Create apiros instance
    apiros = ApiRos(sock)
    apiros.login(sys.argv[2], sys.argv[3])

    # Create MtDevice instance
    # mt_dev = mikrotik_device.MtDevice(apiros)
    # mikrotik_backup.backup(mt_dev)

    input_sentence = []

    while True:
        r = select.select([sock, sys.stdin], [], [], None)
        if sock in r[0]:
            # Something to read in socket, read sentence
            x = apiros.read_sentence()

        if sys.stdin in r[0]:
            # Read line from input and strip off newline
            l = sys.stdin.readline()
            l = l[:-1]

            # If empty line, send sentence and start with new
            # otherwise append to input sentence
            if l == '':
                apiros.write_sentence(input_sentence)
                input_sentence = []
            else:
                input_sentence.append(l)


if __name__ == '__main__':
    main()
