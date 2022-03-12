#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 10:32:48 2022

@author: cati
"""
from multiprocessing import Value
from multiprocessing import Condition, Lock

class Table():
    def __init__(self,nphil,manager):
        self.phil = [False]*nphil
        self.eating = Value('i',0)
        self.actual = None
        self.mutex = Lock()
        self.freefork = Condition(self.mutex)
    def set_current_phil(self,i):
        self.actual = i 
    def vecinos_libres(self):
        i = self.actual 
        return not (self.phil[(i+1)% len(self.phil)])  and not(self.phil[(i-1)%len(self.phil)] )
    def wants_eat( self,i):
        self.mutex.acquire()
        self.freefork.wait_for(self.vecinos_libres)
        self.phil[i] = True
        self.eating.value += 1
        self.mutex.release() 
        #mutex cuando tenga variables compartidas tengo que poner el mutex para no modificarlas a la vez 
    def wants_think(self,i):
        self.mutex.acquire()
        self.phil[i] = False
        self.eating.value -= 1
        self.freefork.notify() # notificar al resto que has acabado 
        self.mutex.release()
        
        