# first-kubernetes

This is a sample application in Flask with the aim of understand how to deploy in Kubernetes, locally with minikube and on the cloud (GCP).

To run locally and learn, you can use **Minikube**. Minikube creates a single cluster with a node locally. Additionally to Minikube you'll also need **kubectl**.
The guide how to do it can be checked out on the official kubernetes documentation.

[Link to install Tools](https://kubernetes.io/docs/tasks/tools/)

[Link to Kubernetes Documentation](https://kubernetes.io/docs/home/)


# Get Running

## With Docker Compose

`docker compose up -d`

## With Kubernetes

1. `minikube start`
2. *Optional*: `kompose convert -f docker-compose.yml` to generate `flask-app-*.yaml` files.
3. `kubectl apply -f flask-app-deployment.yml,flask-app-service.yaml,flask-app-ingress.yaml`
4. `minikube service flask-app`
5. `minikube stop`
6. *Optional*: `minikube delete`


**NOTE**:

If you're running minikube with Docker Desktop as the container driver, a minikube tunnel is needed. This is because containers inside Docker Desktop are isolated from your host computer.

In a separate terminal window, execute:
`minikube service flask-app --url`

The output looks like this:
```bash
http://127.0.0.1:51082
!  Because you are using a Docker driver on darwin, the terminal needs to be open to run it.
```

Then use the given URL to access the app:
curl 127.0.0.1:51082


# Kompose

For running on Kubernetes you need to translate the `docker-compose.yml` file to one or several files in the Kubernetes format. To do this, use `kompose`, a tool that must be installed.

More information [HERE](https://kubernetes.io/docs/tasks/configure-pod-container/translate-compose-kubernetes/)

## To convert a working docker-compose.yml file use:

```bash
kompose convert -f docker-compose.yml
```

In this case, two files were generated: `flask-app-deployment.yaml` and `flask-app-service.yaml`.

To run you must use `kubectl apply` (or `docker stack ...` if minikube was configured to understand docker stack as kubectl apply):

```bash
kubectl apply -f flask-app-deployment.yaml,flask-app-service.yaml
```

## To access the application:

1. minikube service flask-app
2. kubectl describe service flask-app


## To delete the resources and deployment:

```bash
kubectl delete -f flask-app-deployment.yaml,flask-app-service.yaml
```


