CONTAINERID=$(docker ps -l --format "{{.ID}}")
docker exec -it $CONTAINERID /bin/ash