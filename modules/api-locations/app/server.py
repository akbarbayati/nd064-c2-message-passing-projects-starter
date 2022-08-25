from concurrent import futures
import logging
import json
import time
from kafka import KafkaProducer

import grpc
import location_pb2
import location_pb2_grpc


logger = logging.getLogger("udaconnect-api")

  
TOPIC_NAME = 'location'
KAFKA_URL = 'udaconnect-kafka:9092'
msg_q = KafkaProducer(bootstrap_servers=KAFKA_URL,
                      value_serializer=lambda v: json.dumps(v).encode('utf-8'))


class LocationServicer(location_pb2_grpc.LocationServiceServicer):
   
    def Create(self, request, context):
        global msg_q
        request_value = {
            "id": int(request.id),
            "person_id": int(request.person_id),
            "longitude": request.longitude,
            "latitude": request.latitude,
            "creation_time": request.creation_time,
        }
        msg_q.send(TOPIC_NAME,request_value)
        msg_q.flush()
        return location_pb2.Location(**request_value)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)

logger.info("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)