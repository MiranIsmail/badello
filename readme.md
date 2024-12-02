# Badello

This project is a much simpler and a much "dumber" version of Trello
or at least that was what it was spouse to be in the begining.
## How to run
### Prerequists
you have to have:
- docker
- Kubernets
- minikube
### Commands
- `minikube start`
- `kubectl apply -f backend.yaml && kubectl apply -f database.yaml && kubectl apply -f frontend.yaml`
- `xdg-open "$(minikube ip):30080)`
or just run the bash file if you trust it 
`./run.sh`
## Architecture
The app consists of three microservices which are glued together using Fastapi :
![Alt text](a.jpg)
### Frontend
### Backend
### Database

