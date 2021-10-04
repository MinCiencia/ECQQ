# Preprocesamiento de Datos NNA

En este repositorio puedes encontrar todos los pasos utilizados para el preprocesamiento de los 
Diálogos NNA. Aquí encuentras algunos archivos sueltos y tres carpetas importantes:

- input: Contiene 4 tablas *.csv* con los Compromisos, Necesidades y Propuestas desagregados y la tabla principal que contiene la información general de los 862 Diálogos.
- temp: Contiene outputs temporales tras el preprocesamiento y la creación de las variables tópico y keywords más relevante en cada sección. Además,  a la tabla general se le suma una nueva variable que contiene las instituciones participantes de forma estandarizada.
- output: Contiene los *.csv* definitivos para su uso en análisis y visualización del Dashboard.

Los archivos sueltos trabajan e interactuan con cada una de estas carpetas, entre ellos encontramos:

**Python**:

- NNA_Compromisos.py: Limpieza, tokenización, lematización y detección de Tópicos de los Compromisos.
- NNA_Necesidades.py: Limpieza, tokenización, lematización y detección de Tópicos de las Necesidades.
- NNA_Propuestas.py: Limpieza, tokenización, lematización y detección de Tópicos de las Propuestas.

**R**:

- add_labels.R: Agrega etiquetas a variables *contexto_id* y *rangos_edad_id*.
- script_to_csv_dash.R: Genera los *.csv* definitivos para la visualización del Dashboard
