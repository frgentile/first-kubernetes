# MQTT Backend

This code aims to take the messages sent to the mqtt broker (mosquitto) and persist them into MongoDB.

## Steps to generate the Docker container to be used (possibly) on Kubernetes

1. Generate the container from the root dir:
```bash
docker buildx build --target deploy -t frgentile/mqtt-backend:latest .
```

Where `frgentile/mqtt-backend` is my docker hub repository.

2. Push to docker hub:
```bash
docker push frgentile/mqtt-backend:latest
```

If you have an error, could be you need to login first with `docker login`.
