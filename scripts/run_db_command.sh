# Usage: pass in the DB container ID as the argument

# Set database configurations
export CT_DB_USERNAME=ct_admin
export CT_DB_NAME=geoconnections


cat ./db/2020-08-15_init-db.sql | kubectl exec -i $1 -- bash -c "psql -U $CT_DB_USERNAME -d $CT_DB_NAME"

cat ./db/udaconnect_public_person.sql | kubectl exec -i $1 -- bash -c "psql -U $CT_DB_USERNAME -d $CT_DB_NAME"

cat ./db/udaconnect_public_location.sql | kubectl exec -i $1 -- bash -c "psql -U $CT_DB_USERNAME -d $CT_DB_NAME"


# kubectl delete svc udaconnect-api-persons
# kubectl delete svc udaconnect-api-connections
# kubectl delete deploy udaconnect-api-connections
# kubectl delete deploy udaconnect-api-persons
# sudo docker build -t udaconnect-api-connections ./modules/api-connections/
# sudo docker tag udaconnect-api-connections:latest akbayati/udaconnect-api-connections:latest
# sudo docker push akbayati/udaconnect-api-connections:latest

kubectl delete svc udaconnect-api-locations
kubectl delete deploy udaconnect-api-locations
sudo docker build -t udaconnect-api-locations ./modules/api-locations/
sudo docker tag udaconnect-api-locations:latest akbayati/udaconnect-api-locations:latest
sudo docker push akbayati/udaconnect-api-locations:latest
kubectl apply -f deployment/udaconnect-api.yaml 

kubectl delete svc udaconnect-kafka
kubectl delete deploy udaconnect-kafka
docker build -t udaconnect-kafka ./modules/kafka/
docker tag udaconnect-kafka:latest akbayati/udaconnect-kafka:latest
docker push akbayati/udaconnect-kafka:latest
kubectl apply -f deployment/udaconnect-api.yaml 

