import sys
import random
import json
import string
import datetime

input=sys.argv
count=int(input[1])
file_name=input[2]

class Ticket:
    ticket_id=0
    def __init__(self,start_at):
        self.start_at=start_at
        Ticket.ticket_id+=1
        self.shipping_address=random.choice(["N/A","","2/A st","56/T st"])
        self.shipment_date=(str)(start_at+datetime.timedelta(days=random.randrange(1,10)))[0:10]
        self.category=random.choice(["Phone","Laptop","Tablet","TV","N/A"])
        self.contacted_customer=random.choice(["true","false"])
        self.issue_type=random.choice(["Incident","workrequest","N/A"])
        self.source=random.randrange(1,3)
        self.priority=random.randrange(1,4)
        self.group=random.choice(["refund","replacement","repair"])
        self.agent_id=random.randrange(11111,99999)
        self.requester=random.randrange(11111,99999)
        self.product=random.choice(["mobile","Ipad","N/A"])

class Activity:
    start_at=datetime.datetime.now()
    end_at=datetime.datetime.now()
    def __init__(self,start_at,end_at):
        self.start_at=start_at
        self.end_at=end_at
        self.performed_at=start_at+(end_at-start_at)*random.random()
        self.performer_type=random.choice(["user","engineer"])
        self.performer_id=random.randrange(111111,999999)

def generateNote(note_id):
    type=random.randrange(1,5)
    note={"id":note_id,"type":type}
    return note

def generateActivity(t,a,note_id,status):
    if status=="" and random.randrange(1,3)==1 : 
        activity_data={"performed_at":a.performed_at,"ticket_id":t.ticket_id,"performer_type":a.performer_type,"performer_id":a.performer_id,"activity":{"note":generateNote(note_id)}}
    else:
            if random.randrange(1,3)==1:
                activity={"shipping_address":t.shipping_address,
                          "shipment_date":t.shipment_date,
                          "category":t.category,
                          "contacted_customer":t.contacted_customer,
                          "issue_type":t.issue_type,
                          "source":t.source,
                          "status":status,
                          "priority":t.priority,
                          "group":t.group,
                          "agent_id":t.agent_id,
                          "requester":t.requester,
                          "product":t.product}
                activity_data={"performed_at":a.performed_at,"ticket_id":t.ticket_id,"performer_type":a.performer_type,"performer_id":a.performer_id,"activity":activity}
            else:
                activity_data={"performed_at":a.performed_at,"ticket_id":t.ticket_id,"performer_type":a.performer_type,"performer_id":a.performer_id,"activity":{"note":generateNote(note_id),
                "shipping_address":t.shipping_address,
                "shipment_date":t.shipment_date,
                "category":t.category,
                "contacted_customer":t.contacted_customer,
                "issue_type":t.issue_type,
                "source":t.source,
                "status":status,
                "priority":t.priority,
                "group":t.group,
                "agent_id":t.agent_id,
                "requester":t.requester,
                "product":t.product}}
    return activity_data

start_at=datetime.datetime.combine(datetime.datetime.now()+(datetime.datetime(2000, 1, 1, 00, 00, 00)-datetime.datetime.now())*random.random(),datetime.time(22,0,0))
end_at=start_at+datetime.timedelta(days=-1)+datetime.timedelta(seconds=-1)
act_count=0
note_id=0
jsonstr=""
statuses=["Closed","Resolved","Pending","Waiting for Third Party","Waiting for Customer","Open",""]        

for i in range(count):
    start_at1=start_at
    t=Ticket(start_at)
    for status in statuses:
        a=Activity(start_at1,end_at)
        activity_data=generateActivity(t,a,note_id,status)
        start_at1=a.performed_at
        jsonstr=jsonstr+json.dumps(activity_data, indent=4, sort_keys=False, default=str)+","
        act_count=act_count+1
        note_id=note_id+1

metadata={"metadata": {"start_at": start_at,"end_at": end_at,"activities_count": act_count}}
act=",\"activities_data\":["
jsonstr=json.dumps(metadata, indent=4, sort_keys=False, default=str)[:-1]+act+jsonstr[:-1]+"]}"

with open(file_name,"w") as write_file:
 json.dump(jsonstr,write_file)

 

