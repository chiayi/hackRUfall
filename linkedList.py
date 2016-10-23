
class Node:
    def __init__(self, phoneNum, msg, timeToText,  next = None):
        self.phoneNum = phoneNum
        self.msg = msg
        self.timeToText = timeToText
        self.next = None

class ListOfNumbers:
    
    def __init__(self, root):
        self.root = None
    
    def add(self, phoneNum, msg, timeToText):
        newNode = Node(phoneNum, msg, timeToText, None)
        if (self.root == None) or (self.root.timeToText >= newNode.timeToText):
            newNode.next = self.root
            self.root = newNode
            return
        curNode = self.root
        while(curNode.next != None) and (curNode.next.timeToText < newNode.timeToText):
            curNode = curNode.next
        newNode.next = curNode.next
        curNode.next = newNode

    def remove(self, phoneNum):
        if(self.root == None):
            return -1
        if(self.root.phoneNum == phoneNum):
            self.root = self.root.next
            return 1
        curNode = self.root
        while(curNode.next != None):
            if curNode.next.phoneNum == phoneNum:
                curNode.next = curNode.next.next
                return 1
            curNode = curNode.next
        return -1

    def printList(self):
        curNode = self.root
        print("Now Printing")
        while(curNode != None):
            print("%d phoneNum  %d time" % (curNode.phoneNum, curNode.timeToText))
            curNode = curNode.next
        print("")
