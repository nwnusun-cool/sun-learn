### 创建logstash configmap

```angular2html
kubectl create configmap logstash-config --from-file=pipelines.yml --from-file=logstash-beat.conf
```

### 创建logstash deployment

```angular2html
kubebectl apply -f logstash-deployment.yml
```