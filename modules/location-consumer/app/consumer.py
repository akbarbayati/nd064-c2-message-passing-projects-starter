import logging
import json
from kafka import KafkaConsumer

from services import LocationService

logger = logging.getLogger("udaconnect-api")

  
TOPIC_NAME = 'location'
KAFKA_URL = 'udaconnect-kafka:9092'
in_msg_q = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_URL,
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

for message in in_msg_q:
    try:
        LocationService.create(message.value)
    except Exception as e:
        logger.error(str(e))
