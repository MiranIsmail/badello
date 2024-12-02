# Badello

This project is a much simpler and a much "dumber" version of Trello
or at least that was what it was spouse to be in the begining.
You should be able to add,update,delete and view "tasks".
## How to run
### Prerequists
you have to have:
- docker
- Kubernets
- minikube
### Commands
- `minikube start`
- `kubectl apply -f backend.yaml && kubectl apply -f database.yaml && kubectl apply -f frontend.yaml`
- `echo "$(minikube ip):30080)`
or just run the bash file if you trust it 
`./run.sh`  :exclamation:
you might need to do this before `chmod +x ./run.sh
`
## Architecture
The app consists of three microservices which are glued together using Fastapi. These microservices are located in different pods inside a cluster (minikube)
and the UI is exposed using nodePort.
Each Service is Independent which means we use the **Microservice architectrue**.
**Horizontally Scaling pattern**: because the backend and frontend is stateless and independent services we can scale them horizontally.
**Benifits:**
Modularity: beacause we use a microservice pattern we benifit from modularity
Scalability: because of the statelessness of our frontend and backend we scale horizontally.
**Challenges:**
Security: I use plain text to store credentials partly.
Nodeport: this is not ideal for production.
### Frontend
This part is a garphical interface written in python using a library named <https://streamlit.io/> and requests.
this part is exposed externally using nodePort on port 30080. It uses The backend microservies through a ClusterIP.
### Backend
This part is an api for managing the database. It is written in python FastAPI and is exposed inside the cluser using ClusterIP. It depends on the database.
### Database
This part hosts a presistent database, it is a postgresql database,why? you may ask. I just wanted to use it.
There is a single table defined and it is used for storing tasks. It has a mount for presistent data.

