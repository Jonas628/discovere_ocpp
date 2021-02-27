A simple OCPP backend which can run in a docker container.

# build a docker image
go to the root folder of the repository and type (giving a name with the -t flag is optional):
`sudo docker build -t ocpp-cs .`

# run the container
use the -d flag to detach the container from the console (optional), and the -p flag to publish the port 8000 inside 
the container to port 8000 outside the container:
`sudo docker run -d -p 8000:8000 ocpp-cs`

# reading logs



