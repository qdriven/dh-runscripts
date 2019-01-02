#! /bin/sh
docker_id=`docker run --name=mysql-test -itd -p 3306:3306 -v $PWD/data/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=password mysql:latest`
docker logs $docker_id
docker ps -a

# -v ./data/mysql:/var/lib/mysql