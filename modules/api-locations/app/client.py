import grpc
import location_pb2
import location_pb2_grpc

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:30005")
stub = location_pb2_grpc.LocationServiceStub(channel)

# Update this with desired payload
location = location_pb2.Location(
    id=1,
    person_id=5,
    latitude="-122.290524",
    longitude="37.553441",
    creation_time="1970-01-01T10:10:10Z"
)

response = stub.Create(location)
print(response)
