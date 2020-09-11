#!/usr/bin/python


#part 1
kRequest = 'a'
kReply   = 'b'

#part 2
kOnlineNodes = 'a'    # select online nodes
kNodeMsg = 'b'        # select node's msg
kNs3 = 'c'
kOne2Many = 'd'       # emulation, one2many, this character is useful for web server
kOne2ManyServer = 'e' # emulation, it is useful for real UAN node
kOne2ManyClient = 'f' # emulation, it is useful for real UAN node

# part `3
kConstHeaderLen = 14
kCheckHeaderLen = 4
kCheckHeaderArray = [0x35, 0x71, 0x49, 0x68]

class UAN_Common:
    def __init__(self):
        ## method type
        self.id = 0
