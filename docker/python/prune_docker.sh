docker system prune


#docker image prune -f
# docker save --output image.tar ImageID-or-Name
# docker image prune -fa
# docker load --input image.tar
# $(docker images -a|grep "<none>"|awk '$1=="<none>" {print $3}')
