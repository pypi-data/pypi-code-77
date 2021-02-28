#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 14:44:37 2021

@author: jamesdoucette
"""
from linked_list import ListNode

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.len=0
        
    def __str__(self):
        if len(self)==0:
            return 'Empty Queue'
        else:
            return str(self.head)
        
    def __repr__(self):
        return str(self)
         
    def __len__(self):
        return self.len
    
    def enqueue(self, val):
        if len(self)==0:
            self.head=ListNode(val,None)
            self.tail=self.head
            self.len=1
            
        else:
            self.tail.next=ListNode(val,None)
            self.tail=self.tail.next
            self.len+=1
            
    def front(self):
        if len(self)==0:
            raise Exception('Called front on empty queue')
        
        return self.head.val
    
    def dequeue(self):
        if len(self)==0:
            raise Exception('Called dequeue on empty queue')
        
        res=self.head.val
        self.head=self.head.next
        if self.head is None:
            self.tail = None
        self.len-=1
        
        return res