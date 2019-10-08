# Robot Communcation

## Basic testing

### Broker
Clone the repository and run `docker-compose up -d` to start the MQTT server.

### Clients
On the client, run `python app.py --broker "mqtt://{IP_FOR_BROKER}" --label "{LABEL}" --topics-publish {PUBLISH TOPICS} --topics-subscribe {SUBSCRIBE TOPICS}` to start the Python test client.
