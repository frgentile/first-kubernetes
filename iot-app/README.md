For using with docker compose:
docker compose up --build -d

For using with kubernetes:

1. kompose convert -f docker-compose.yml

2. kubectl apply -f mongodb-deployment.yaml,mongodb-ingress.yaml,mongodb-service.yaml,mosquitto-cm0-configmap.yaml,mosquitto-deployment.yaml,mosquitto-ingress.yaml,mosquitto-service.yaml,mqtt-backend-deployment.yaml

3. kubectl delete -f mongodb-deployment.yaml,mongodb-ingress.yaml,mongodb-service.yaml,mosquitto-cm0-configmap.yaml,mosquitto-deployment.yaml,mosquitto-ingress.yaml,mosquitto-service.yaml,mqtt-backend-deployment.yaml
 
4. 