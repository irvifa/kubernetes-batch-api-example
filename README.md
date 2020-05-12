# kubernetes-batch-api-example

## Build

```aidl
docker build -t <dockerimage-name> \
  --build-arg SLACK_WEBHOOK_URL_ARG=${SLACK_WEBHOOK_URL} \
  --build-arg CLUSTER_NAMESPACE_ARG=${CLUSTER_NAMESPACE}
```

After building the image you can run this in your local, however
it's not recommended to include your secret like the webhook into
your `Dockerimage` directly. 

## Deployment

- Build
```
docker build -t <dockerimage-name>
```
- Push `Dockerimage`
- Create a `Secret`
```
kubectl -n <NAMESPACE> create secret generic app-secret --from-literal=slackwebhook='<SLACK_WEBHOOK>'
```
- Change the fields of `$namespace`, `$clusterNamespace`, and `$imageName`.
- You can use `kubectl apply -f k8s --recursive`
