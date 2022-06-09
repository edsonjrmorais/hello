#!/bin/bash

# To call this script #
# chmod +x ./test.sh 
# ./config-manager.sh pyapi-hello 2.0

# Getting variables from script command-line args
TRGT=$1
TAG=$2

# Validating App Tag
if [ $(docker images edsonjrmorais/hello:${TAG} | awk '$1 ~ /edsonjrmorais/ { print $2}') != "${TAG}" ]; then
    echo "Tag don't exists"
    echo "Building a new Docker image"
    docker build -t edsonjrmorais/hello:${TAG} .
else
    echo "Tag already exists"
fi

# Validating NameSpace
if [ "$(kubectl get ns ${TRGT} 2>&1)" == "Error from server (NotFound): namespaces "\"${TRGT}"\" not found" ]; then
    kubectl create namespace ${TRGT}
else
    echo "Namespace already exists"
fi

# Verifying if the deployment already exists
if [ "$(kubectl get deploy/${TRGT} --namespace ${TRGT} 2>&1)" == "Error from server (NotFound): deployments.apps "\"${TRGT}"\" not found" ]; then
    echo "Deployment not exists"
    echo "Applying [k8s-${TRGT}-deployment.yaml]"
    kubectl apply -f k8s-${TRGT}-deployment.yaml
    while :
    do
        POD_STATE_APPLY=$(kubectl get pods --selector app=${TRGT} --namespace ${TRGT} --no-headers | awk '{print $3}' | uniq)
        if [[ "$POD_STATE_APPLY" == "Running" ]]; then
            break
        fi
        sleep 5
    done 
else
    echo "Deployment already exists"
    echo "Updating deployment app tag to [${TAG}]"
    kubectl set image --namespace ${TRGT} deployment ${TRGT} ${TRGT}=edsonjrmorais/hello:${TAG}
    STOP=5
    while [ $STOP -ge 0 ]
    do
        POD_STATE_SET=$(kubectl get pods --selector app=${TRGT} --namespace ${TRGT} --no-headers | awk '{print $3}' | uniq)
        if [[ "$POD_STATE_SET" == "Running" ]]; then
            break
        fi
        ((STOP--))
        if [ $STOP == 0 ]; then
            echo "Something went bad with the deployment"
            echo "Undeploying to the previous valid version"
            kubectl rollout undo --namespace ${TRGT} deployment/${TRGT}
            echo "Deleting Docker image with the bad version"
            docker image rm edsonjrmorais/hello:${TAG}
        fi
        sleep 2
    done    
fi