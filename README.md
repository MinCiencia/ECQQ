# ECQQ
En este repositorio se pueden encontrar laas siguientes carpetas de repositorios

## base-datos
Este repositorio contiene jupyter notebooks para el procesamiento de datos relacionados con la base de datos como el uniformar nombres de comunas y regiones, entre otros (en la carpeta jupyter_scripts). Para que funcione la creación de la base de datos en necesario contar con los csv, los cuales se pueden contrar en:

[data-final.zip](https://drive.google.com/file/d/1bgMpIMipvGo3BLaYNW7pivsgr-KTLAgM/view?usp=sharing)

O en la carpeta de este repositorio ECQQ/preprocessing/db/data.7z
## contributions_rnn
Este repositorio contiene los procedimientos para realizar la clasificación de las contribuciones con redes neuronales. El jupyter notebook CreateRecords.ipynb prepara los datos . El entrenamiento del modelo se realiza con train.py. Finalmente la evaluación y predicción está contenida en Results.ipynb
## nemotion
Este repositorio contiene jupyter notebooks principales. Por un lado Grouping Emotions.ipynb que sirve para sistematizar las Emociones. Por otra parte el jupyternotebook Analisis de Topicos - Necesidades.ipynb para ayudar a sistematizar tanto las Necesidades Personales como las del País.
## preoprocess_nna
Contiene los procedimientos referentes a los datos de NNA. Están por una parte los scripts add_labels.R y script_to_csv_dash.R para formatear los datos y NNA_Compromisos.py, NNA_Necesidades.py y NNA_Propuestas.py para procesar las categorías que aparecen en sus respectivos nombres.
## preprocessing
En este repositorio se encuentra el jupyter notebook Pipeline.ipynb que realiza la limpieza de datos correspondientes a Consultas individuales y Diálogos y crea todas las tablas necesarias para responder las 5 preguntas descritas en detalle. La creación de las tablas se realiza con los scripts presentes en la carpeta use_cases.
## randomforest
Este repositorio contiene los procedimientos para realizar la clasificación de las contribuciones con árboles de decisión. El entrenamiento del modelo se realiza con train.py. Finalmente la evaluación y predicción está contenida en Results.ipynb
## superset-ecqq
En este repositorio se encuentra la descripción de cómo instalar el Dashboard o panel de datos en base a sencillos pasos descritos al interior de este.
## superset-ui-plguins
En este repositorio se encuentra la herramienta para poder crear pluggins en Superset.
## tutoriales
En este repositorio se encuentran algunos totoriales para hacer cruce de datos, entre otros. 
## Enlaces a los Datos

Además de lo anterior es posible encontrar los siguientes elementos de interés:

### Datos sin procesar

[data_origen.zip](https://drive.google.com/file/d/17CQrODs55Bb2wV-BeIAgcSlD9h72jhzn/view?usp=sharing)

### Datos en formato CSV y SQL insert
[data-final.zip](https://drive.google.com/file/d/1bgMpIMipvGo3BLaYNW7pivsgr-KTLAgM/view?usp=sharing)

O en la carpeta/archivo de este repositorio 
ECQQ/preprocessing/db/data.7z
### Respaldo de Base de Datos
[back_up.sql](https://drive.google.com/file/d/1OM3Avv2sTF1aIVVrQ6ecMGWFYXfqsIcR/view?usp=sharing)

O en la carpeta/archivo de este repositorio 
ECQQ/preprocessing/db/back_up.7z.001
ECQQ/preprocessing/db/back_up.7z.002
