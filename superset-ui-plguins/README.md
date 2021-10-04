# @superset-ui ecqq plugins

Collection of packages that power the
[Apache Superset ECQQ](https://github.com/ECQQ/visualizacion) UI, and can be used to craft custom
data applications that leverage a Superset backend :chart_with_upwards_trend:

## Demo

Most recent release: http://35.243.251.30:8088/

## Packages

### Core packages

| Package                                                                                                                       | Version                                                                                                                                                         |
| ----------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [@superset-ui/core](https://github.com/apache-superset/superset-ui/tree/master/packages/superset-ui-core)                     | [![Version](https://img.shields.io/npm/v/@superset-ui/core.svg?style=flat-square)](https://www.npmjs.com/package/@superset-ui/core)                             |
| [@superset-ui/chart-controls](https://github.com/apache-superset/superset-ui/tree/master/packages/superset-ui-chart-controls) | [![Version](https://img.shields.io/npm/v/@superset-ui/core.svg?style=flat-square)](https://www.npmjs.com/package/@superset-ui/chart-controls)                   |
| [@superset-ui/generator-superset](https://github.com/apache-superset/superset-ui/tree/master/packages/generator-superset)     | [![Version](https://img.shields.io/npm/v/@superset-ui/generator-superset.svg?style=flat-square)](https://www.npmjs.com/package/@superset-ui/generator-superset) |

### Chart plugin packages

`@superset-ui/legacy-*` packages are extracted from the classic
[Apache Superset](https://github.com/apache/incubator-superset) and converted into plugins. These
packages are extracted with minimal changes (almost as-is). They also depend on legacy API
(`viz.py`) to function.

| Package                                                                                                                                                              | Version                                                                                                                                                                                                     |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [@eccq/legacy-plugin-chart-chord](https://github.com/ECQQ/superset-ui-plguins/tree/main/plugins/legacy-plugin-chart-chord)                               | [![Version](https://img.shields.io/npm/v/@ecqq/legacy-plugin-chart-chord.svg?style=flat-square)](https://www.npmjs.com/package/@ecqq/legacy-plugin-chart-chord)                               |
| [@ecqq/legacy-plugin-chart-country-map-chile](https://github.com/ECQQ/superset-ui-plguins/tree/main/plugins/legacy-plugin-chart-country-map-chile)                   | [![Version](https://img.shields.io/npm/v/@ecqq/legacy-plugin-chart-country-map-chile.svg?style=flat-square)](https://www.npmjs.com/package/@ecqq/legacy-plugin-chart-country-map-chile)                   |

## Build plugins

### NPM version

These plugins requiere npm version v14.16.0, to install we recomend Node Version Manager (nvm)

#### Installing NVM

```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
```

#### Installing Node

List of node versions available

```
nvm ls-remote
```

Install version v14

```
nvm install v14.16.0
```

Set the version as default

```
nvm alias default v14.16.0
```

Set this version as the new version

```
nvm use v14.16.0
```

#### Installing yarn and lerna using npm

Run these command to installed these packages in order to build the plugins

```
npm install yarn lerna -g
```

#### Building the plugins 

##### Bootstrap Project

To link all the package together and install all dependencies

```
lerna bootstrap
```

This command will:

- Install all external dependencies
- Symlink together all the Lerna packages that are dependencies of each other.
- Run prepublish in all bootstrapped packages.

##### Building the plugins

To build the plugins in order tu upload them to the npm registry, we need to run two scripts, one for building the actual code and other to copy the assets to used in the plugins

```
yarn build && yarn build:assets
```

#### Publishing the plugins

In order to publish the plugins, we have to login to our npmjs.com account

```
npm login
```

Then, we simply use the publish comand

```
npm publish
```

If the version we are trying to publish already exists, we have to change the current version in the package.json file of the plugin directory

## Contribution and development guide

Please read the [contributing guidelines](CONTRIBUTING.md) which include development environment
setup and other things you should know about coding in this repo.

### License

Apache-2.0
