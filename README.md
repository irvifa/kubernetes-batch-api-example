# kubernetes-batch-api-example

## Build

```aidl
docker build -t <dockerimage-name> \
  --build-arg SLACK_WEBHOOK_URL_ARG=${SLACK_WEBHOOK_URL} \
  --build-arg CLUSTER_NAMESPACE_ARG=${CLUSTER_NAMESPACE}
```
