#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 11:29:36 2020

@author: jamesdoucette
"""
import random

class ListNode:
    def __init__(self, val, next_node):
        self.val=val
        self.next=next_node
        
    def __str__(self):
        node=self
        res=''
        for node in self:
            if len(res)>0:
                res+=', '
            res+=str(node.val)
        return res

    
    def __repr__(self):
        return str(self)
    
    
    def __contains__(self, val):
        for node in self:
            if node.val == val:
                return True
        return False


    def __eq__(self,other):
        if self.val != other.val:
            return False
        
        elif self.next is None and other.next is None:
            return True
        
        elif self.next is None or other.next is None:
            return False
        
        else:
            return self.next == other.next
        
        
    def __iter__(self):
        current = self
        while current is not None:
            yield current
            current = current.next
          

        
            

    
