I LOVE PROGRAMMING IT IS SO COOL I PROMISE

minikube start

docker build -t frontend:local -f Dockerfile .
docker build -t backend:local -f Dockerfile .

minikube image load backend:latest
minikube image load frontend:latest

kubectl apply -f backend.yaml
kubectl apply -f frontend.yaml
kubectl apply -f database.yaml


kubectl get pods
minikube stop
