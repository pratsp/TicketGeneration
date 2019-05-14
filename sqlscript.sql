.mode column
.headers on
WITH status AS (WITH TicketTracker AS 
(SELECT DISTINCT t.ticket_id,a.status,a.performed_at 
 FROM Activity a 
 INNER JOIN FactActivityData fad ON a.activity_id=fad.activity_id 
 INNER JOIN Ticket t ON fad.ticket_id=t.ticket_id)
 SELECT t1.ticket_id,
julianday(t2.performed_at) A,
julianday(t3.performed_at) B,
julianday(t4.performed_at) C,
julianday(t5.performed_at) D,
julianday(t6.performed_at) E,
julianday(t7.performed_at) FROM 'TicketTracker' t1
LEFT OUTER JOIN 'TicketTracker' t2
ON t1.ticket_id=t2.ticket_id
AND t2.status="Open"
LEFT OUTER JOIN 'TicketTracker' t3
ON t1.ticket_id=t3.ticket_id
AND t3.status="Waiting for Customer"
LEFT OUTER JOIN 'TicketTracker' t4
ON t1.ticket_id=t4.ticket_id
AND t4.status="Waiting for Third Party"
LEFT OUTER JOIN 'TicketTracker' t5
ON t1.ticket_id=t5.ticket_id
AND t5.status="Pending"
LEFT OUTER JOIN 'TicketTracker' t6
ON t1.ticket_id=t6.ticket_id
AND t6.status="Resolved"
LEFT OUTER JOIN 'TicketTracker' t7
ON t1.ticket_id=t7.ticket_id
AND t7.status="Closed")
SELECT DISTINCT ticket_id,CAST((B-A)*24*60 AS INTEGER) AS [Time spent Open]
,CAST((C-B)*24*60 AS INTEGER) AS [Time spent Waiting on Customer ]
,CAST((E-D)*24*60 AS INTEGER) AS [Time spent waiting for response ]
,CAST((E-A)*24*60 AS INTEGER) AS [Time till resolution ]
,CAST((B-A)*24*60 AS INTEGER) AS [Time to first response] FROM Status
