#!/usr/bin/python3

import sys
import sqlite3
import json
import random

input=sys.argv
file_name=input[1]
db_name=input[2]

conn = sqlite3.connect(db_name)
c=conn.cursor()

c.execute("DROP TABLE IF EXISTS Metadata")
c.execute("CREATE TABLE Metadata(metadata_id int,start_at text,end_at text,activities_count int)")

c.execute("DROP TABLE IF EXISTS Ticket")
c.execute("CREATE TABLE Ticket(ticket_id int,shipping_address text,shipment_date text,category text,contacted_customer text,issue_type text,source int,priority int,groups text,agent_id int,requester int,product text)")

c.execute("DROP TABLE IF EXISTS FactActivityData")
c.execute("CREATE TABLE FactActivitydata(ticket_id int,activity_id int,note_id int,metadata_id int)")

c.execute("DROP TABLE IF EXISTS Activity")
c.execute("CREATE TABLE Activity(activity_id int,performed_at text,peformer_type text,performer_id int,status text)")

c.execute("DROP TABLE IF EXISTS Note")
c.execute("CREATE TABLE Note(note_id int,note_type text)")

c.execute("DROP TABLE IF EXISTS TicketTracker")
c.execute("CREATE TABLE TicketTracker(ticket_id int, status text, act_performed_at text)")

with open(file_name,"r") as read_file:
    j = json.load(read_file)
jsonstr=json.loads(j)
count=jsonstr["metadata"]["activities_count"]

metadata_id=random.randrange(1111,9999)
activity_id=1
note_id=0

c.execute("INSERT INTO Metadata VALUES (?,?,?,?)",
          (metadata_id,jsonstr["metadata"]["start_at"],jsonstr["metadata"]["end_at"],count))
 
activities=jsonstr["activities_data"]
ticket_id=0
for act in activities :
    note_present=0
    act_present=0
    if "note" in act["activity"]:
        note_id=act["activity"]["note"]["id"]
        note_present=1
        c.execute("INSERT INTO Note VALUES(?,?)",(note_id,act["activity"]["note"]["type"]))
    if "status" in act["activity"]:
        act_present=1
        if(ticket_id!=act["ticket_id"]):
            c.execute("INSERT INTO Ticket VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (act["ticket_id"],act["activity"]["shipping_address"],act["activity"]["shipment_date"],act["activity"]["category"],
            act["activity"]["contacted_customer"],act["activity"]["issue_type"],
            act["activity"]["source"],act["activity"]["priority"],act["activity"]["group"],
            act["activity"]["agent_id"],act["activity"]["requester"],act["activity"]["product"]))
            ticket_id=act["ticket_id"]
        c.execute("INSERT INTO ACTIVITY VALUES (?,?,?,?,?)",
        (activity_id,act["performed_at"],act["performer_type"],act["performer_id"],act["activity"]["status"]))
        activity_id=activity_id+1
    c.execute("INSERT INTO FactActivityData VALUES (?,?,?,?)",
    (act["ticket_id"],activity_id*act_present,note_id*note_present,metadata_id))
         

conn.commit()
conn.close()
