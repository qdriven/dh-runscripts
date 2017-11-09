# README 

Includes server ansible scripts for testing enviroment preparation.
There are several roles:

- skywalking: a tracing system
- ignite: Apache Ignite
- hadoop: Hadoop
- hive: Hive
- hbase: hbase

## skywalking usage

For skywalking,there are threr different components:

- skywalking agent
- skywalking collector
- skywalking server

and each component,there are several different tags:

- install_agent
- uninstall_agent
- install_collector
- uninstall_collector
- install_web
- uninstall_web
- start_web
- stop_web

The command is like this:

```sh
ansible-playbook -i inventory/<your_env> roles/skywalking/task/main.yml -tags <tag_name>
```
