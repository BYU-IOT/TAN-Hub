# TAN-Hub
Trailer Area Network Hub

Thinking that for the User Interface it would be easiest to use Python's Flask web application import that would privide a web app for the touch display. Here are some examples of flask that I have been playing around with to better understand how to have the website not just be a passive one but one that can update and provide current info passed on from the D1 Mini. This is done through web sockets that open a bidirectional communication between the java script/html and the server.

The examples show this application through a chat interface that I am trying to change to simply show a recieved number from the current sensor that is a live number, constantly updating form the input to the raspberrry pi. It also needs to be able to send the commands from the web app on updating both the "ADCFrq" and the "Interval" on the raspberry pi. 
