## @superset-ui/legacy-plugin-chart-chord

[![Version](https://img.shields.io/npm/v/@superset-ui/legacy-plugin-chart-chord.svg?style=flat-square)](https://www.npmjs.com/package/@ecqq/legacy-plugin-chart-word-graph)

This plugin provides Chord Diagram for Superset.

### Usage

Configure `key`, which can be any `string`, and register the plugin. This `key` will be used to
lookup this chart throughout the app.

```js
import WordGraphChartPlugin from '@ecqq/legacy-plugin-chart-word-graph';

new WordGraphChartPlugin().configure({ key: 'word_graph' }).register();
```

Then use it via `SuperChart`. See
[storybook](https://apache-superset.github.io/superset-ui-plugins/?selectedKind=plugin-chart-chord)
for more details.

```js
<SuperChart
  chartType="word-graph"
  width={600}
  height={600}
  formData={...}
  queriesData={[{
    data: {...},
  }]}
/>
```
