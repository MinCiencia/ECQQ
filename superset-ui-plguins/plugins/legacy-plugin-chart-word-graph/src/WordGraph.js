/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
/* eslint-disable no-param-reassign, react/sort-prop-types */
import { Network } from 'vis-network';
import PropTypes from 'prop-types';
import { CategoricalColorNamespace } from '@superset-ui/core';

const propTypes = {
  data: PropTypes.arrayOf(
    PropTypes.shape({
      source: PropTypes.string,
      target: PropTypes.string,
      value: PropTypes.number,
    }),
  ),
  width: PropTypes.number,
  height: PropTypes.number,
  colorScheme: PropTypes.string,
};

function WordGraph(element, props) {
  const { data, width, height, colorScheme } = props;

  element.className = `${element.className} superset-legacy-word-graph`;

  const colorFn = CategoricalColorNamespace.getScale(colorScheme);

  // nodes
  const nodeMap = new Map();
  let k = 1;

  data.forEach(link => {
    if (!nodeMap.has(link.source)) {
      nodeMap.set(link.source, { id: k, value: 0, color: colorFn(k) });
      k += 1;
    }

    if (!nodeMap.has(link.target)) {
      nodeMap.set(link.target, { id: k, value: 0, color: colorFn(k) });
      k += 1;
    }
  });

  // edges
  const edgeSet = new Set();
  const edges = [];
  let title;
  let counterTitle;
  let sourceNode;
  let targetNode;

  data.forEach(link => {
    sourceNode = nodeMap.get(link.source);
    targetNode = nodeMap.get(link.target);

    sourceNode.value += link.value;
    targetNode.value += link.value;

    title = `${link.source} ${link.target}`;

    if (edgeSet.has(title)) return;

    counterTitle = `${link.target} ${link.source}`;
    edgeSet.add(title);
    edgeSet.add(counterTitle);

    edges.push({
      from: sourceNode.id,
      to: targetNode.id,
      value: link.value,
      title,
      color: sourceNode.color,
    });
  });

  const nodes = [];
  nodeMap.forEach((node, key) => {
    nodes.push({
      id: node.id,
      value: node.value,
      label: key,
      color: node.color,
    });
  });

  // create network
  const graphData = {
    nodes,
    edges,
  };

  const options = {
    width: `${width}px`,
    height: `${height}px`,
    nodes: {
      shape: 'dot',
    },
  };

  // eslint-disable-next-line no-new
  new Network(element, graphData, options);
}

WordGraph.displayName = 'WordGraph';
WordGraph.propTypes = propTypes;

export default WordGraph;
