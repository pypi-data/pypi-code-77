#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 14:40:20 2021

@author: jamesdoucette
"""
from linked_list import ListNode

class Stack:
    def __init__(self):
        self.head=None
        self.len=0
        
    def __str__(self):
        if len(self)==0:
            return 'Empty Stack'
        else:
            return str(self.head)
        
    def __repr__(self):
        return str(self)
        
    def __len__(self) -> int:
        return self.len
    
    
    def push(self, val):
        self.head = ListNode(val,self.head)
        self.len+=1
        
        
    def top(self):
        if len(self)==0:
            raise Exception('Called top on empty stack')
            
        return self.head.val
        
    def pop(self):
        if len(self)==0:
            raise Exception('Called pop on empty stack')
        
        res=self.head.val
        self.head=self.head.next
        self.len-=1
        
        return res