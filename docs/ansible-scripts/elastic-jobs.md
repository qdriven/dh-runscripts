# Ansible Elastic Jobs 

## elastic job console

- how to install console
```shell
ansible-playbook -i inventory/all-in-one roles/elasticjob/tasks/main.yml -tags install_console
```

- how to stop elastic job console

```shell
ansible-playbook -i inventory/all-in-one roles/elasticjob/tasks/main.yml -tags stop_console
```

- how to restart elastic job console

```shell
ansible-playbook -i inventory/all-in-one roles/elasticjob/tasks/main.yml -tags restart_console
```

## elastic job worker 

- how to install worker 
```shell
ansible-playbook -i inventory/all-in-one roles/elasticjob/tasks/main.yml -tags install_worker
```

- how to stop elastic job worker

```shell
ansible-playbook -i inventory/all-in-one roles/elasticjob/tasks/main.yml -tags stop_worker
```

- how to restart elastic job worker

```shell
ansible-playbook -i inventory/all-in-one roles/elasticjob/tasks/main.yml -tags restart_worker
```