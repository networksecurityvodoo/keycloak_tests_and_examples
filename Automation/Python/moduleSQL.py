#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pyodbc
#####################################
# Connection via Microsoft SQL ODBC #
#####################################

_connection = None 


def get_connection():
    
    server = 'tcp:HOST.database.windows.net' 
    database = 'DB' 
    username = 'USER' 
    password = 'PASSWORD;' 
    
    global _connection
    if not _connection:
        _connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    return _connection

    # List of Stuff which is available after this module was loaded
    __all__=['getConnection']    
    

