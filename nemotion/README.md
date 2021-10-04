# NEMOTION: Need & Emotions Post-Processing

This repository includes functions that take files made by [the cleaning pipeline](https://github.com/ECQQ/preprocessing).


### Requirements
- [Docker](https://docs.docker.com/engine/install/)
- [Docker-compose](https://docs.docker.com/compose/install/)

### Usage
##### Building images and container 
1. Run `docker-compose build` from the root folder (where `docker-compose.yml` is alocated)
2. To star the container use: `docker-compose up -d` (where `-d` means detached)
3. Similarly, for the container stopping run: `docker-compose stop`

##### Running scripts 
To run scripts inside the container, we need to open an interactive session.
1. We already known our container is named `nemotion`, but if you want to see running containers just use: `docker container ls`
2. To initialize an interactive session use: `docker exec -it nemotion bash`
3. Then you can use bash command as usually

##### Jupyter notebook 
By default the image container starts jupyter notebook service (in background). You may see the jupyter logs by removing `-d` argument in *step 2 on Building images and container Section*. 

1. If our container is running in *detached mode* just use: `docker logs nemotion -f` to display logs. 
2. Then, copy the notebook link which includes the security token and and paste it on your browser.
