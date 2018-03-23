#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 15:03:07 2018

@author: clebson
"""

from odm2api.ODMconnection import dbconnection
from odm2api.ODM2.services.readService import *
from odm2api.ODM2.services import CreateODM2
# Create a connection to the ODM2 database
# ----------------------------------------


#connect to database
# createconnection (dbtype, servername, dbname, username, password)
# session_factory = dbconnection.createConnection('connection type: sqlite|mysql|mssql|postgresql', '/your/path/to/db/goes/here', 2.0)#sqlite


#session_factory = dbconnection.createConnection('postgresql', 'localhost', 'postgres', 'postgres', '89635241')
# session_factory = dbconnection.createConnection('mysql', 'localhost', 'odm2', 'ODM', 'odm')#mysql
#session_factory= dbconnection.createConnection('mssql', "(local)", "ODM2", "ODM", "odm")#win MSSQL
# session_factory= dbconnection.createConnection('mssql', "arroyoodm2", "", "ODM", "odm")#mac/linux MSSQL
session_factory = dbconnection.createConnection('sqlite', 'ODM2.sqlite', 2.0)



_session = session_factory.getSession()
read = ReadODM2(session_factory)
c

# Run some basic sample queries.
# ------------------------------
# Get all of the variables from the database and print their names to the console
allVars = read.getVariables()
print ("\n-------- Information about Variables ---------")
print(allVars)
for x in allVars:
    print(x.VariableCode + ": " + x.VariableNameCV)
