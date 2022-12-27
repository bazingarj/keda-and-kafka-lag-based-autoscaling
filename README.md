# keda-and-kafka-lag-based-autoscaling

Prerequisites

```
minikube setup with prometheus and grafana
docker
```

Note: Make sure to give enough CPU and Memory to minikube before Creating, I have use 4 cpu and 8 Gig memory.
you need to setup the both config before setting up a fresh minikube environment. e.g.

```
minikube config set cpus 4
minikube config set memory 8192
minikube start
```

# Step 1:  Setup zookeeper & kafka
Install zookeeper 
```
kubectl apply -f zookeeper.yml
```

Go to kafka.yml and kafka-1.yml , replace the MACHINE_IP with your instance or system ip which you can check using 
```
hostname -i (linux)
hostname  (mac)
```

Now install kafka brokers using
```
kubectl apply -f kafka.yml
kubectl apply -f kafka-1.yml

#Now expose kafka brokers on host ports in background

nohup kubectl port-forward --address 0.0.0.0 svc/kafka-service 30092:9092 &
nohup kubectl port-forward --address 0.0.0.0 svc/kafka-service-1 30093:9092 &

#To check kafka port are still available 
ps aux | grep "9092"
```

# Step 2: setup kafka lag Exporter
Note: Replace Machine IP in below command as well
Install kafka lag Exporter
```
helm repo add kafka-lag-exporter https://seglo.github.io/kafka-lag-exporter/repo/
helm repo update
helm install kafka-lag-exporter kafka-lag-exporter/kafka-lag-exporter  --set clusters\[0\].name=my-cluster   --set clusters\[0\].bootstrapBrokers="MACHINE_IP:30092\,MACHINE_IP:30093"
```
Now we need to tell prometheus to include kafka-lag-exporter in target list, To do that we need to edit prometheus config map using

```
kubectl edit configmap prometheus-server
```
if it says prometheus-server not found , check configmap correct name using **kubectl get configmap**

Add the above config in configMap **scrape_configs** section:

```
    - job_name: kafka-lag-exporter
      static_configs:
      - targets:
        - kafka-lag-exporter-service.default.svc.cluster.local:8000
```
Post this you need to restart prometheus using

```
kubectl rollout restart deployment prometheus-server
```
check the correct name from **kubectl get deployment**

you can expose prometheus using **kubectl port-forward --address 0.0.0.0 svc/prometheus-server 9092:80** to check if the newly added target is healthy and visible

# Step 3: Setup keda

```
helm repo add kedacore https://kedacore.github.io/charts
helm repo update
kubectl create namespace keda
helm install keda kedacore/keda --namespace keda
```

# Step 4: keda config

change the deployment name before applying
```
kubectl apply -f keda-scaledObject.yml
```


# Addition Content:

Sample consumer and Producer code which create 10 event lag each second

For consumer
```
cd consumer
docker build -t consumer:latest . 
kubectl apply -f consumer.yml
```


For Producer

```
cd producer
docker build -t producer:latest . 
kubectl apply -f producer.yml
```
