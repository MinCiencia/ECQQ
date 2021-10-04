# Herramienta de Limpieza
## Etapa de Preprocesamiento

En este repositorio podemos encontrar el Pipeline utilizado para limpiar y formatear los datos siguiendo el modelo entidad-relacion (MER) a continuacion:

![](https://github.com/ECQQ/preprocessing/blob/main/diagrams/MER.png)

### Requisitos
- [Docker](https://docs.docker.com/engine/install/)
- [Docker-compose](https://docs.docker.com/compose/install/)

### Uso
##### Construir el contenedor
1. Ejecutar `docker-compose build` desde la carpeta raiz (i.e., donde esta el archivo `docker-compose.yml`)
2. Para iniciar el contenedor: `docker-compose up -d` (donde `-d` significa "detached")
3. De manera similar, para detener el contenedor utilizamos: `docker-compose stop`

##### Otros comandos de utilidad
Para ingresar al contenedor y ejecutar scripts o instalar alguna dependencia temporal:
1. Debemos ver los contenedores que se estan ejecutando con: `docker container ls`
2. Para entrar en el contenedor: `docker exec -it cleaner bash`. En este caso `cleaner` es el nombre de nuestro contenedor
3. Luego puedes utilizar `bash` normalmente.

Cualquier paquete o dependencia que sea instalada en modo interactivo se borrara al detener el contenedor. Para hacer persistente alguna dependencia debes modificar el `requirements.txt` (para paquetes de python) o el Dockerfile (para instalar paquetes del sistema)

##### Jupyter notebook 
Por default la imagen del contenedor inicia una sesion en jupyter notebook. Como nosotros ejecutamos el contenedor en modo "detached" no podemos ver los logs. Los logs nos indicaran la ruta donde esta corriendo el notebook (la cual tiene asociado un token de seguridad).

Una opcion es sacar el `-d` en el paso 2, sin embargo tambien podemos usar:
1. `docker logs -f cleaner` para visualizar los logs del contenedor. 
2. Luego copia el link que tiene asociado el token de seguridad en tu navegador
