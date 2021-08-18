# Edgify Home Assignment

- src folder contains the src of the web api.
- test folder contains small csv examples and small python script to send them via POST.

notes:
1. upload csv file consider without headers.
2. when price is market, the transactions need to be ordered by price. for example 
   if the "Market" transaction type is buying, than the selling transactions 
   that match it need to be lowest first to higher in the last places. Meaning 
   that all "non Market" transactions should be processed first, and then process
   "market" transactions.
3. there is a mistake in step 2 exmaple...“g8dr-7fk3” total is wrong (if I understand it correctly)
4. executeing the transactions that are not "market" can be done in multithreaded... did had the 
   time to implement it
5. what happens if only half of the matching is met ? means that not all the amount can be found, 
   only part of it... I took into account that only part of the matching is happening... (buy/sell 
   what you can...) and the transaction is defined as "Executed"
6. Docker:
   - building docker:
   sudo docker build -t test .
   - to run, check that it running and the port number
   sudo docker run -d -p 5000:5000 test
   sudo docker logs <docker>
   get the id and add it to the test_step2.py
   taken from:
   https://stackoverflow.com/questions/30323224/deploying-a-minimal-flask-app-in-docker-server-connection-issues

   need to understand better how to use the ports in the docker.