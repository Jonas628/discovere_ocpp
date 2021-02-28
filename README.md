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
Docker has a logging mechanism that writes everything printed to the console to a log file.
get the path to the log file:
`sudo docker inspect central-system | grep LogPath`

# run on AWS elastic container service
use the commandline to register on ECS:
`sudo -i`
`aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 203535000826.dkr.ecr.eu-west-1.amazonaws.com`
tag the image for uploading it to a ECS repository (assuming the repo is called "ocpp-central-system"):
`docker tag ocpp-cs:latest 203535000826.dkr.ecr.eu-west-1.amazonaws.com/ocpp-central-system:latest`
push the image onto the repository:
`docker push 203535000826.dkr.ecr.eu-west-1.amazonaws.com/ocpp-central-system:latest`

# get logs from the container
find the instance with
`aws wc2 describe-instances`
and find the instance id and public DNS, e.g.
ID: i-03cb6e15c45ebdc0f
DNS: ec2-18-202-56-229.eu-west-1.compute.amazonaws.com
For Linux, default user is: ec2-user

connect to the EC2 instance with ssh:
`ssh -i /home/ole/.config/mysshkey.pem ec2-user@ec2-18-202-56-229.eu-west-1.compute.amazonaws.com`


