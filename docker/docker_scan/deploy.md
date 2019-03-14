# Deploy

```
curl -L https://raw.githubusercontent.com/coreos/clair/master/contrib/compose/docker-compose.yml -o $HOME/docker-compose.yml # 修改 quay.io/coreos/clair-git:latest 为 quay.io/coreos/clair:latest
vim $HOME/docker-compose.yml
mkdir $HOME/clair_config
curl -L https://raw.githubusercontent.com/coreos/clair/master/config.yaml.sample -o $HOME/clair_config/config.yaml
vim $HOME/clair_config/config.yaml # 修改 database source 为 postgresql://postgres:password@postgres:5432?sslmode=disable
docker-compose -f $HOME/docker-compose.yml up -d
```
