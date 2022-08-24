FROM openjdk:8-jdk-alpine3.9

EXPOSE 9092

RUN apk add wget --no-cache curl tar bash procps

RUN wget https://dlcdn.apache.org/kafka/3.2.1/kafka_2.13-3.2.1.tgz -O - | tar -xzf -

WORKDIR kafka_2.13-3.2.1
 
ADD ./run_kafka.sh .

RUN chmod u+x ./run_kafka.sh

ENTRYPOINT ["./run_kafka.sh"]
