import logging
from concurrent import futures
import threading
import app

from kafka import KafkaProducer, KafkaConsumer
import json

import grpc
import app.udaconnect.location_pb2 as location_pb2
import app.udaconnect.location_pb2_grpc as location_pb2_grpc
from app.udaconnect.services import LocationService
from app.udaconnect.models import Location
from app import app

logger = logging.getLogger("udaconnect-api")

TOPIC_NAME = 'location'
KAFKA_URL = 'udaconnect-kafka:9092'
msg_q = KafkaProducer(bootstrap_servers=KAFKA_URL)
in_msg_q = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_URL)

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
        msg_q.send(TOPIC_NAME, json.dumps(request_value, indent=2).encode('utf-8'))
        msg_q.flush()
        logger.error('XXXX')
        logger.error(request_value)
        return location_pb2.Location(**request_value)

    def Get(self, request, context):
        with app.app_context():
            location: Location = LocationService.retrieve(int(request.id))
            response_value = {
                "id": int(location.id),
                "person_id": int(location.person_id),
                "longitude": location.longitude,
                "latitude": location.latitude,
                "creation_time": str(location.creation_time),
            }
            return location_pb2.Location(**response_value)
    
class GrpcServer:
    def __init__(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
        location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), self.server)
        self.persist_thread = threading.Thread(target=self.persist_locations)
    
    def persist_locations(self):
        global in_msg_q
        for message in in_msg_q:
            logger.error(message)
            with app.app_context():
                LocationService.create(json.load(message.value))
        logger.error('YYYY')

    def start(self):
        logger.info("Server starting on port 5005...")
        self.server.add_insecure_port("[::]:5005")
        self.server.start()
        self.persist_thread.start()
