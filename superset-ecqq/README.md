<!--
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
-->

## Como instalar superset localmente

### Paso 1: Instalar docker y docker-compose

**docker**

Actualizar el indice de paquetes e instala los prerequisitos:

```
sudo apt-get update
```

```
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
 ```
 
Luego añade la clave de GPC de docker

```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

Añade el repositorio oficial

```
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```  

Instala Docker Engine

Actualiza apt e isntala docker

```
sudo apt-get update
```

```
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

Agrega tu usario al grupo docker

```
sudo usermod -aG docker $USER
```

Haz log out y log y verifica que se haya instalado corriendo hello-world

```
sudo docker run hello-world
```

Deberias ver el siguiente mensaje:
```
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
b8dfde127a29: Pull complete 
Digest: sha256:f2266cbfc127c960fd30e76b7c792dc23b588c0db76233517e1891a4e357d519
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
 ```
 
**docker-compose**

Descarga la version 1.29.1 de docker-compose

```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

Otorgale permisos de ejecución a los binarios
```
sudo chmod +x /usr/local/bin/docker-compose
```
Reinicia el sistema

### Paso 2: Clonar repositorio
```
git clone https://github.com/ECQQ/superset-ecqq
```

Lanzar superset con docker-compose

```
cd superset-ecqq
```
```
sudo docker-compose up
```

Esto puede tomar tiempo, debes ser paciente.

Cuando termine deberias ver un mensaje como:

```
superset_init            | Init Step 4/4 [Complete] -- Loading examples
superset_init            | 
superset_init            | 
superset_init            | ######################################################################
superset_init            | 
superset_init exited with code 0
```

Si todo salió bien, entra a http://localhost:8088. Deberías ver una ventana para hacer login

### Paso 3: Restablecer bd con datos y dashboards

descarga la repo con los scripts para cargar la BD

```
git clone https://github.com/ECQQ/preprocessing
```

Descarga el zip los archivos csv's de los datos y un archivo sql con el backup de los dashboards de superset.

[data-final.zip](https://drive.google.com/file/d/1bgMpIMipvGo3BLaYNW7pivsgr-KTLAgM/view?usp=sharing)

[back_up.sql](https://drive.google.com/file/d/1OM3Avv2sTF1aIVVrQ6ecMGWFYXfqsIcR/view?usp=sharing)

Mueve los archivos a la repo

```
mv data-final.zip preprocessing/db
```
```
mv back_up.sql preprocessing/db
```

Entra al repo y descomprime los archivos

```
cd preprocessing/db
```
```
unzip data-final.zip
```

Corre el script para restaurar los dashboards

```
./restore_database.sh
```

Corre el script para subir los datos a la base de datos

```
./upload_data
```

## Paso 5: Login en superset

Entra a http://localhost:8088, deberías ver una ventana de inicio de sesión.

Para entrar debes usar el usuario admin y contraseña admin.

Y listo, ya tienes superset corriendo localmente, puedes explorar los datos, dashboards y graficos.


Superset
=========

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/apache/superset)
[![Build Status](https://github.com/apache/superset/workflows/Python/badge.svg)](https://github.com/apache/superset/actions)
[![PyPI version](https://badge.fury.io/py/apache-superset.svg)](https://badge.fury.io/py/apache-superset)
[![Coverage Status](https://codecov.io/github/apache/superset/coverage.svg?branch=master)](https://codecov.io/github/apache/superset)
[![PyPI](https://img.shields.io/pypi/pyversions/apache-superset.svg?maxAge=2592000)](https://pypi.python.org/pypi/apache-superset)
[![Get on Slack](https://img.shields.io/badge/slack-join-orange.svg)](https://join.slack.com/t/apache-superset/shared_invite/zt-g8lpruog-HeqpgYrwdfrD5OYhlU7hPQ)
[![Documentation](https://img.shields.io/badge/docs-apache.org-blue.svg)](https://superset.apache.org)
[![Dependencies Status](https://david-dm.org/apache/superset/status.svg?path=superset-frontend)](https://david-dm.org/apache/superset?path=superset-frontend)

<img
  src="https://github.com/apache/superset/raw/master/superset-frontend/branding/superset-logo-horiz-apache.png"
  alt="Superset"
  width="500"
/>

A modern, enterprise-ready business intelligence web application.

[**Why Superset?**](#why-superset) |
[**Supported Databases**](#supported-databases) |
[**Installation and Configuration**](#installation-and-configuration) |
[**Release Notes**](RELEASING/release-notes-0-38/README.md) |
[**Get Involved**](#get-involved) |
[**Contributor Guide**](#contributor-guide) |
[**Resources**](#resources) |
[**Organizations Using Superset**](INTHEWILD.md)


## Screenshots & Gifs

**Gallery**

<kbd><a href="https://superset.apache.org/gallery"><img title="Gallery" src="https://raw.githubusercontent.com/apache/superset/master/superset-frontend/images/screenshots/gallery.jpg"></a></kbd><br/>

**View Dashboards**

<kbd><img title="View Dashboards" src="https://raw.githubusercontent.com/apache/superset/master/superset-frontend/images/screenshots/slack_dash.jpg"></kbd><br/>

**Slice & dice your data**

<kbd><img title="Slice & dice your data" src="https://raw.githubusercontent.com/apache/superset/master/superset-frontend/images/screenshots/explore.jpg"></kbd><br/>

**Query and visualize your data with SQL Lab**

<kbd><img title="SQL Lab" src="https://raw.githubusercontent.com/apache/superset/master/superset-frontend/images/screenshots/sql_lab.jpg"></kbd><br/>

**Visualize geospatial data with deck.gl**

<kbd><img title="Geospatial" src="https://raw.githubusercontent.com/apache/superset/master/superset-frontend/images/screenshots/geospatial_dash.jpg"></kbd><br/>

**Choose from a wide array of visualizations**

<kbd><img title="Visualizations" src="https://raw.githubusercontent.com/apache/superset/master/superset-frontend/images/screenshots/explore_visualizations.jpg"></kbd><br/>


## Why Superset?

Superset provides:

* An intuitive interface for visualizing datasets and
    crafting interactive dashboards
* A wide array of beautiful visualizations to showcase your data
* Code-free visualization builder to extract and present datasets
* A world-class SQL IDE for preparing data for visualization, including a rich metadata browser
* A lightweight semantic layer which empowers data analysts to quickly define custom dimensions and metrics
* Out-of-the-box support for most SQL-speaking databases
* Seamless, in-memory asynchronous caching and queries
* An extensible security model that allows configuration of very intricate rules on
    on who can access which product features and datasets.
* Integration with major
    authentication backends (database, OpenID, LDAP, OAuth, REMOTE_USER, etc)
* The ability to add custom visualization plugins
* An API for programmatic customization
* A cloud-native archiecture designed from the ground up for scale

## Supported Databases

Superset can query data from any SQL-speaking datastore or data engine (e.g. Presto or Athena) that has a Python DB-API driver and a SQLAlchemy dialect.

Here are some of the major database solutions that are supported:

<p align="center">
  <img src="https://raw.githubusercontent.com/apache/superset/master/superset-frontend/images/redshift.png" alt="redshift" border="0" width="106" height="41"/>
  <img src="https://raw.githubusercontent.com/apache/superset/master/superset-frontend/images/google-biquery.png" alt="google-biquery" border="0" width="114" height="43"/>
  <img src="https://raw.githubusercontent.com/apache/superset/master/superset-frontend/images/snowflake.png" alt="snowflake" border="0" width="152" height="46"/>
  <img src="https://raw.githubusercontent.com/apache/superset/master/superset-frontend/images/presto.png" alt="presto" border="0" width="152" height="46"/>
  <img src="https://raw.githubusercontent.com/apache/superset/master/superset-frontend/images/druid.png" alt="druid" border="0" width="135" height="37" />
  <img src="https://raw.githubusercontent.com/apache/superset/master/superset-frontend/images/postgresql.png" alt="postgresql" border="0" width="132" height="81" />
  <img src="https://raw.githubusercontent.com/apache/superset/master/superset-frontend/images/mysql.png" alt="mysql" border="0" width="119" height="62" />
  <img src="https://raw.githubusercontent.com/apache/superset/master/superset-frontend/images/mssql-server.png" alt="mssql-server" border="0" width="93" height="74" />
  <img src="https://raw.githubusercontent.com/apache/superset/master/superset-frontend/images/db2.png" alt="db2" border="0" width="62" height="62" />
  <img src="https://raw.githubusercontent.com/apache/superset/master/superset-frontend/images/sqlite.png" alt="sqlite" border="0" width="102" height="45" />
  <img src="https://raw.githubusercontent.com/apache/superset/master/superset-frontend/images/sybase.png" alt="sybase" border="0" width="128" height="47" />
  <img src="https://raw.githubusercontent.com/apache/superset/master/superset-frontend/images/mariadb.png" alt="mariadb" border="0" width="83" height="63" />
  <img src="https://raw.githubusercontent.com/apache/superset/master/superset-frontend/images/vertica.png" alt="vertica" border="0" width="128" height="40" />
  <img src="https://raw.githubusercontent.com/apache/superset/master/superset-frontend/images/oracle.png" alt="oracle" border="0" width="121" height="66" />
  <img src="https://raw.githubusercontent.com/apache/superset/master/superset-frontend/images/firebird.png" alt="firebird" border="0" width="86" height="56" />
  <img src="https://raw.githubusercontent.com/apache/superset/master/superset-frontend/images/greenplum.png" alt="greenplum" border="0" width="140" height="45" />
  <img src="https://raw.githubusercontent.com/apache/superset/master/superset-frontend/images/clickhouse.png" alt="clickhouse" border="0" width="133" height="34" />
  <img src="https://raw.githubusercontent.com/apache/superset/master/superset-frontend/images/exasol.png" alt="exasol" border="0" width="106" height="59" />
  <img src="https://raw.githubusercontent.com/apache/superset/master/superset-frontend/images/monet-db.png" alt="monet-db" border="0" width="106" height="46" />
  <img src="https://raw.githubusercontent.com/apache/superset/master/superset-frontend/images/apache-kylin.png" alt="apache-kylin" border="0" width="56" height="64"/>
</p>

**A more comprehensive list of supported databases** along with the configuration instructions can be found
[here](https://superset.apache.org/docs/databases/installing-database-drivers).

Want to add support for your datastore or data engine? Read more [here](https://superset.apache.org/docs/frequently-asked-questions#does-superset-work-with-insert-database-engine-here) about the technical requirements.


## Installation and Configuration

[Extended documentation for Superset](https://superset.apache.org/docs/installation/installing-superset-using-docker-compose)

## Adding plugins to superset-frontend

To add a new plugin to superset, we need to add the plugin as a dependency, then modify the code, install the packages and finally build the new docker image.

### Adding the plugin as a dependency

All the plugins are uploaded to npmjs.com under the organization [ecqq](https://www.npmjs.com/org/ecqq).

We need to edit the file package.json in the superset-frontend directory to add the plugin as a dependency, to do so we add a line in under dependencies, for example, the plugin [legacy-plugin-chart-country-map-chile](https://www.npmjs.com/package/@ecqq/legacy-plugin-chart-country-map-chile) is added as:

```
"@ecqq/legacy-plugin-chart-country-map-chile": "^0.17.16",
```

this line has to include the version of the package

### Modifying the source code

To add the plugin to the frontend, we can follow this official tutorial, but only the part that modifies the javascript code in the src directory [building custom viz plugins](https://superset.apache.org/docs/installation/building-custom-viz-plugins) 

### Installing the dependencies with the plugin

After we have added the plugin as a dependency and we have imported the plugin into the code, we have to run the following command under the superset-frontend directory

```
npm install
```

### Creating the new Docker image

After all this we have to create a new docker image. first we have to go in the root directory and execute the following command:

```
docker build -t ecqq:superset .
```

where ecqq:superset is the name of this new docker image, this name is important because is the name used in the docker-compose file.


## Get Involved

* Ask and answer questions on [StackOverflow](https://stackoverflow.com/questions/tagged/apache-superset) using the **apache-superset** tag
* [Join our community's Slack](https://join.slack.com/t/apache-superset/shared_invite/zt-g8lpruog-HeqpgYrwdfrD5OYhlU7hPQ)
  and please read our [Slack Community Guidelines](CODE_OF_CONDUCT.md#slack-community-guidelines)
* [Join our dev@superset.apache.org Mailing list](https://lists.apache.org/list.html?dev@superset.apache.org)


## Contributor Guide

Interested in contributing? Check out our
[CONTRIBUTING.md](https://github.com/apache/superset/blob/master/CONTRIBUTING.md)
to find resources around contributing along with a detailed guide on
how to set up a development environment.


## Resources

* Superset 1.0
  * [Superset 1.0 Milestone](https://superset.apache.org/docs/version-one)
  * [Superset 1.0 Release Notes](https://github.com/apache/superset/tree/master/RELEASING/release-notes-1-0)
  * [Presentation on Superset 1.0 Public Roadmap](https://docs.google.com/presentation/d/1FGgyI8tLWLUPSQ5eEno78bylLfobj9O2W4yoUoFYHH8/edit#slide=id.g9c182b81b9_1_0)
  * [Public Superset Roadmap](https://github.com/apache-superset/superset-roadmap/projects/1)
* Superset 101 -- Getting Started Guide (From [Preset Blog](https://preset.io/blog/))
  * [Installing Apache Superset Locally](https://preset.io/blog/2020-05-11-getting-started-installing-superset/)
  * [Installing Database Drivers](https://preset.io/blog/2020-05-18-install-db-drivers/)
  * [Connect Superset To Google Sheets](https://preset.io/blog/2020-06-01-connect-superset-google-sheets/)
  * [Create Your First Chart](https://preset.io/blog/2020-06-08-first-chart/)
  * [Create Time Series Charts](https://preset.io/blog/2020-06-26-timeseries-chart/)
* [Documentation for End-Users (by Preset)](https://docs.preset.io/)
* [Docker image](https://hub.docker.com/r/apache/superset)
* [Recordings of Community Events](https://www.youtube.com/channel/UCMuwrvBsg_jjI2gLcm04R0g)
  * [May 2020: Virtual Meetup. Topics: 0.36 Overview, Committers Self-Intro, Roadmap](https://www.youtube.com/watch?v=tXGDmqjmcTs&t=20s)
  * [July 2020: Virtual Meetup. Topics: Visualization Plugins, 0.37 Preview, Demo](https://www.youtube.com/watch?v=f6up5x_iRbI)
  * [November 2020: Virtual Meetup. Topics: Superset 1.0 & the Roadmap](https://www.youtube.com/watch?v=GwtWRUSEjk4)
  * [November 2020: Live Demo. Topic: Superset Semantic Layer](https://www.youtube.com/watch?v=8VL4ZPLFUYI)
  * [December 2020: Live Demo. Topic: Annotations](https://www.youtube.com/watch?v=Yk6bKgphj1Q)
* Custom Visualizations
  * [Building Custom Viz Plugins](https://superset.apache.org/docs/installation/building-custom-viz-plugins)
  * [Managing and Deploying Custom Viz Plugins](https://medium.com/nmc-techblog/apache-superset-manage-custom-viz-plugins-in-production-9fde1a708e55)
* [Superset API](https://superset.apache.org/docs/rest-api)
