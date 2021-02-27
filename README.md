A simple OCPP backend which can run in a docker container.

# build a docker image
go to the root folder of the repository and type (giving a name with the -t flag is optional):
`sudo docker build -t ocpp-cs .`

# run the container
use the -d flag to detach the container from the console (optional), and the -p flag to publish the port 8000 inside 
the container to port 8000 outside the container:
`sudo docker run --name central-system -t -d -v $(pwd):/tmp  -w /tmp -p 8000:8000 ocpp-cs`

# connect a charge_point
run the skript to connect a charge point to the central system which starts sending heart beats:
`python charge_point.py`

# reading logs locally
get the path to the log file:
`sudo docker inspect central-system | grep LogPath`

# run on AWS elastic container service
use the commandline to register on ECS:
`sudo -i`
`aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 203535000826.dkr.ecr.eu-west-1.amazonaws.com`
tag the image for uploading it to a ECS repository (assuming the repo is called "ocpp-central-system"):
`sudo docker tag ocpp-cs:latest 203535000826.dkr.ecr.eu-west-1.amazonaws.com/ocpp-central-system:latest`

