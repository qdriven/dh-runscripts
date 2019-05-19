## K8S Conceptions

- `Node`: a node/machine/container run in k8s
- `Pod`: serveral containers composites a app which shared a volumn
- `pos-states`: container lifecycle states
- `services`: abstraction layer of k8s internal containers, and expose to external users
- `volumes`
- `labels`
- `accessing_the_api`
- `ux`
- `cli`

## Kubectl Command List

How to Use Kubectl：

```bash
kubectl [flags]
kubectl [command]
```

## Commands:

|Command|Usage|Comments|
|------|------|--------|
|get|get resources||
|describe|describe resources||
|create|create resources||
|update|update resources||
|delete|delete resources||
|log|log resources||
|rolling-update|rolling-update resources||
|exec |exec internal resources||
|port-forward|local port forward to pod port||
|proxy|start k8s API Server's proxy server ||
|expose|expose replication/pod servie to k8s servie ||
|label|resource label||
|config|k8s configuration file||
|cluster-info|cluster-info of k8s cluster configuration file||
|help |help|

