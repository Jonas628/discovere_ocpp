A simple OCPP backend which can run in a docker container.

# Run in a Docker container on AWS

### Step 1: build a docker image
go to the root folder of the repository and type : \
`sudo docker build -t ocpp-cs .`

### Step 2: run the container
Run the container to check that it was built correctly: \
`sudo docker run --name central-system -t -d -v $(pwd):/tmp  -w /tmp -p 8000:8000 ocpp-cs` \
use the -d flag to detach the container from the console (optional), and the -p flag to publish the port 8000 inside 
the container to port 8000 outside the container.

### Step 3: connect a charge point locally
To check that the script runs properly, use the charge_point.py script.
run the skript to connect a charge point to the central system which sends messages: \
Note that the host name in the websocket must be "localhost" or "0.0.0.0"
`python charge_point.py`

### Step 4: login using the aws cli
`sudo -i`
`aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 203535000826.dkr.ecr.eu-west-1.amazonaws.com`
This should return "Login Succeeded"
NOTE: the aws cli must be configured before

### Step 5: tag and push the docker image to aws:
tag the image for uploading it to a ECS repository (assuming the repo is called "ocpp-central-system"): \
`docker tag ocpp-cs:latest 203535000826.dkr.ecr.eu-west-1.amazonaws.com/ocpp-central-system:latest`
push the image onto the repository: \
`docker push 203535000826.dkr.ecr.eu-west-1.amazonaws.com/ocpp-central-system:latest`

### Step 6: run the image in an elastic container on aws
This step involves some configuration in the aws console. Here is a follow-along video:
https://www.youtube.com/watch?v=zs3tyVgiBQQ&t=515s

### Step 7: connect a charge point to aws
Now you should be able to connect a charge point.
Make sure that the host address in the websocket is the url of the
aws instance, then run the charge point: \
`sudo docker build -t ocpp-cs .`

### Step 8: connect to the aws instance with ssh
To access the log of the container it is required to connect to the instance
using shh. The ssh command needs the path to the locally stored private key,
and the public DNS of the aws instance: \
`ssh -i /home/ole/.config/mysshkey.pem ec2-user@ec2-18-202-56-229.eu-west-1.compute.amazonaws.com`
va
### Step 9: get the log:
find the name of the running container: \
`sudo docker ps` \
get the location of the log file: \
`sudo docker inspect *container_name* | grep LogPath`
open the log file in the console:
`sudo cat *path_to_log*`


# Access
## Django superuser
superuser: technical.support

password: @CentralSystem

## Elephant PostgreSQL DB
technical.support@discovere.de
@CentralSystem
