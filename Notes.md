## Notes 


Observations from my deployment 

1. I had to manually pull the docker image using:
     ''' 
        docker pull python:3.9.18-slim
     ''' 
    before I could build with 
    ''' 
        sudo docker build -t analytics-dashboard .
    '''