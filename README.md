[An UI presentation :)](https://docs.google.com/presentation/d/e/2PACX-1vT-EUM4xLxx20RHzT5iE6WtQaJ3y1e-LymmuW8yTf8u9eX1IKaF42DOwLZBr1uVpDsvwCeIo9DZDUWQ/pub?start=false&loop=false&delayms=3000)

### Application Database
The informations are stored in the Google Firebase table “Users” from the project“HelloPyAPI”.

It's a personal project of Edson Morais for this reason, when “Running From the Source Code” you should consider:

- Using your own Firebase project:

1 - Export your Firebase project service account.

2 - Create the file ./App/.env with the content below:

    DATABASE_URL="<< your Firebase database URL >>"
    CREDENTIAL_PATH="<< Firebase project service account json file path >>"

- Using the Edson Morais’ Firebase project:
Please contact me :) [edsonjr.morais@gmail.com]

### Running From the Source Code

1 - Getting the source code:
git clone https://github.com/edsonjrmorais/hello.git 

Before moving on, take a look at the topic “Using your own Firebase project”

2 - Moving to the application folder:
    cd hello/App

3 - Installing the Python packages:
    pip install -r requirements.txt

4 - Running the application from the source code:
    Python main.py

### “Fast Installation”
You must have Docker or a K8S already installed in your computer/environment.

- Using only Docker:

1 - Getting the Docker image from the Docker Hub:
docker pull edsonjrmorais/hello:1.0

2 - Starting a container with the previous image:
docker run -d -p 8181:8181 edsonjrmorais/hello:1.0

- Using K8S:

1 - Getting the Docker image from the Docker Hub:
docker pull [edsonjrmorais/hello:1.0](https://hub.docker.com/r/edsonjrmorais/hello)

2 - Creating a deployment with with the previous image:
kubectl create deployment pyapi-hello-deployment --image edsonjrmorais/hello:1.0 --port=8181

### Utilization
- Getting User birthday information:

GET | http://{docker/K8S ip}:8181/hello/

**Examples & Behaviors:**

GET | http://{docker/K8S ip}:8181/hello/edinho
GET | http://{docker/K8S ip}:8181/hello/dompedro
GET | http://{docker/K8S ip}:8181/hello/myname1
GET | http://{docker/K8S ip}:8181/hello/myname+-*

- Setting/Updating User birthday information:

PUT | http://{docker/K8S ip}:8181/hello/

JSON Payload { "username": "Peter", "dateOfBirth": "2022-06-15" }

**Examples & Behaviors:**

PUT | http://{docker/K8S ip}:8181/hello/
{ "username": "Peter", "dateOfBirth": "2022-12-15" }	

GET | http://{docker/K8S ip}:8181/hello/Peter

PUT | http://{docker/K8S ip}:8181/hello/
{ "username": "Peter", "dateOfBirth": "<-Today->" }

<-Today-> must be in format "YYYY-MM-DD"

GET | http://{docker/K8S ip}:8181/hello/Peter