# first-kubernetes

This is a sample application in Flask with the aim of understand how to deploy in Kubernetes, locally with minikube and on the cloud (GCP).

To run locally and learn, you can use **Minikube**. Minikube creates a single cluster with a node locally. Additionally to Minikube you'll also need **kubectl**.
The guide how to do it can be checked out on the official kubernetes documentation.

[Link to install Tools](https://kubernetes.io/docs/tasks/tools/)

[Link to Kubernetes Documentation](https://kubernetes.io/docs/home/)

[GKE - Google Kubernetes Engine - Deploy App Cluster](https://cloud.google.com/kubernetes-engine/docs/deploy-app-cluster)


# Get Running

## With Docker Compose

`docker compose up -d`

## With Kubernetes

1. `minikube start`
2. *Optional*: `kompose convert -f docker-compose.yml` to generate `flask-app-*.yaml` files.
3. `kubectl apply -f flask-app-deployment.yml,flask-app-service.yaml,flask-app-ingress.yaml`
4. `minikube service flask-app` or alternatively, use kubectl to forward the port: `kubectl port-forward service/flask-app 5000:5000`
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


## Using Google Kubernetes Engine - GKE

1. Create an Autopilot cluster named: 
```bash
gcloud container clusters create-auto flask-app-cluster \
    --location=us-central1
```

2. After creating your cluster, you need to get authentication credentials to interact with the cluster:
```bash
gcloud container clusters get-credentials flask-app-cluster \
    --location us-central1
```

### Deploy Manually:

3. To run flask-app in your cluster, you need to deploy the application by running the following command:
```bash
kubectl create deployment flask-app \
    --image=frgentile/flask-app:latest
```

4. After deploying the application, you need to expose it to the internet so that users can access it. You can expose your application by creating a Service, a Kubernetes resource that exposes your application to external traffic. To expose your application, run the following kubectl expose command:
```bash
kubectl expose deployment flask-app \
    --type LoadBalancer \
    --port 80 \
    --target-port 5000
```

5. Clean up to avoid incurring charges to your Google Cloud account for the resources used. Delete the application's Service by running kubectl delete:
```bash
kubectl delete service flask-app
kubectl delete deployment flask-app
```
This command deletes the Compute Engine load balancer that you created when you exposed the Deployment. Delete your cluster by running gcloud container clusters delete:
```bash
gcloud container clusters delete flask-app-cluster \
    --location us-central1
```

### Deploy applying .yaml files:




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


