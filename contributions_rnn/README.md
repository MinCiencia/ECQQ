# Red Neural Recurrente para la Clasificacion de Contribuciones
## Etapa de Sistematizacion

En este repositorio se encuentra el modelo utilizado para clasificar las contribuciones.

![](https://github.com/ECQQ/contributions_rnn/blob/main/figures/cm.png?raw=true)

Metric | Precision | Recall | Macro F1 |
--- | --- | --- | --- |
Value | 0.64 +- 0.07 | 0.64 +- 0.06 | 0.61 +- 0.08 |

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
2. Para entrar en el contenedor: `docker exec -it cleaner bash`. En este caso `rnn_ecqq` es el nombre de nuestro contenedor
3. Luego puedes utilizar `bash` normalmente.

Cualquier paquete o dependencia que sea instalada en modo interactivo se borrara al detener el contenedor. Para hacer persistente alguna dependencia debes modificar el `requirements.txt` (para paquetes de python) o el Dockerfile (para instalar paquetes del sistema)

##### Jupyter notebook 
Por default la imagen del contenedor inicia una sesion en jupyter notebook. Como nosotros ejecutamos el contenedor en modo "detached" no podemos ver los logs. Los logs nos indicaran la ruta donde esta corriendo el notebook (la cual tiene asociado un token de seguridad).

Una opcion es sacar el `-d` en el paso 2, sin embargo tambien podemos usar:
1. `docker logs -f rnn_ecqq` para visualizar los logs del contenedor. 
2. Luego copia el link que tiene asociado el token de seguridad en tu navegador

##### Entrenamiento 
Antes de entrenar debemos prepar nuestros datos. Para ello podemos hacer uso del notebook tutorial `CreateRecords.ipynb`. Sigue las instrucciones y generaras los `tf.record` necesarios para entrenar, evaluar y predecir.

El script de entrenamiento se encuentra en la carpeta raiz `train.py`.
Los parametros posibles son:
```
    # TRAINING PAREMETERS
    parser.add_argument('--data', default='./data/records/contrib_ft/', type=str,
                        help='Dataset folder containing the records files')
    parser.add_argument('--p', default="./experiments/test", type=str,
                        help='Proyect path. Here will be stored weights and metrics')
    parser.add_argument('--batch-size', default=64, type=int,
                        help='batch size')
    parser.add_argument('--epochs', default=2000, type=int,
                        help='Number of epochs')
    parser.add_argument('--n-batches', default=100, type=int,
                        help='Number of batches to sample')
    # MODEL HIPERPARAMETERS
    parser.add_argument('--layers', default=2, type=int,
                        help='Number of encoder layers')
    parser.add_argument('--units', default=128, type=int,
                        help='Number of units within the recurrent unit(s)')
    parser.add_argument('--dropout', default=0.25, type=float,
                        help='Dropout applied to the output of the RNN')
    parser.add_argument('--lr', default=1e-3, type=int,
                        help='Optimizer learning rate')
```
Un ejemplo de ejecucion puede ser:
```
python train.py --data ./out/records/fold_0/ --p ./experiments/fold_0 --n-batches 200
```

##### Evaluacion y prediccion
El notebook tutorial se encuentra en `Results.ipynb` sigue las instruccion para cargar los pesos del modelo ajustado, evaluar y etiquetar las muestras.

Al final del notebook, dejamos dos ejemplos explorativos para futuras investigaciones, tales como la **visualizacion del estado oculto** de la red y la **entropia de las clases** dada las probabilidades de salida del modelo.

![](https://github.com/ECQQ/contributions_rnn/blob/main/figures/entropy.png?raw=true)
