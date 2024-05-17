@echo off

docker-compose build
docker-compose up -d

timeout /t 30 > nul

curl -X POST -H "Content-Type: application/json" --data @"debezium\Jendouba-Sales-Connector.json" http://localhost:8083/connectors
curl -X POST -H "Content-Type: application/json" --data @"debezium\Beja-Sales-Connector.json" http://localhost:8083/connectors
curl -X POST -H "Content-Type: application/json" --data @"debezium\Kef-Sales-Connector.json" http://localhost:8083/connectors

echo All connectors deployed successfully.

pause
