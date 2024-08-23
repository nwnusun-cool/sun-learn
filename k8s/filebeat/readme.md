### 创建filebeat configmap
```
kubectl create configmap filebeat-config --from-file=filebeat.yml
```

### 创建filebeat deployment
```
kubebectl apply -f filebeat-deployment.yml
```

### 授权
```
kubectl apply -f pod-reader-binding.yaml
kubectl apply -f pod-reader-clusterrole.yaml
```