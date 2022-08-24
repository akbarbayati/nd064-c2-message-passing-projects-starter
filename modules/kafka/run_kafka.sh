#!/bin/bash

# make kafka container accessible from outside
sed -i '$ a listeners=PLAINTEXT://:9092' config/server.properties
sed -i '$ a advertised.listeners=PLAINTEXT://udaconnect-kafka:9092' config/server.properties

bin/zookeeper-server-start.sh config/zookeeper.properties &
bin/kafka-server-start.sh config/server.properties &

bin/kafka-topics.sh --create --topic location --replication-factor 1 --partitions 2 --bootstrap-server localhost:9092

bin/kafka-server-stop.sh
bin/kafka-server-start.sh config/server.properties