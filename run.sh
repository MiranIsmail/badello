#!/bin/bash

minikube start

kubectl apply -f backend.yaml
kubectl apply -f database.yaml
kubectl apply -f frontend.yaml

xdg-open "$(minikube ip):30080"
