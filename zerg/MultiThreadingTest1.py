# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 21:49:11 2018

@author: User
"""

import threading
import queue


my_queue = queue.Queue()


#function to run in thread
def testFunction(imput1, out_queue):
    #function stuff
    output =  imput1 + 1
    
    #return
    out_queue.put(output)

#create thread
thread1 = threading.Thread(testFunction(1, my_queue))

#start thread
thread1.start()

#stuff to happen in main thread while other thread is doing shinanigans 






#stop until thread done
thread1.join()

#print function return
print(my_queue.get())   