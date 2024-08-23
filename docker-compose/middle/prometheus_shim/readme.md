### 构建镜像
```angular2html
docker build -t my-flask-app .
```

### 运行容器
> 注意：需要共享配置
```angular2html
docker run -d --privileged=true  -v /opt/prometheus-2.43.0.linux-arm64:/opt -e PROMETHEUS_URL=172.39.200.8:9090 -p 5000:5000 prometheus_shim
```