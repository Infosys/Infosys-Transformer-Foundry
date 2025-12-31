/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { useContext } from "react";
import { FormDataContext } from "../stores/form-datastore";
import { useParams } from "react-router-dom";
class PipelineService {
  constructor(formData, projectId) {
    this.formData = formData;
    this.projectId = projectId;
  }

  getPipelineData() {
    let resultData = {};
    if (
      this.formData &&
      Object.keys(this.formData).length > 0 &&
      this.formData["pipeline-config"]
    ) {
      const config = this.formData["pipeline-config"];
      const kubeflowData = {
        projectId: this.projectId,
        version: config.version,
        name: config.name,
        description: config.description,
        pipeline: config,
      };
      resultData = { kubeflowData };
      if (
        this.formData["pipeline-edges"] &&
        this.formData["pipeline-edges"].length > 0
      ) {
        const edges = this.formData["pipeline-edges"];
        const nodes = [];
        const stepDependsOn = {};
        const nodeNameSet = new Set();

        for (const edge of edges) {
          const source = edge["source"];
          const target = edge["target"];
          nodeNameSet.add(source);
          nodeNameSet.add(target);

          if (stepDependsOn[target] == null) {
            stepDependsOn[target] = [source];
          } else {
            stepDependsOn[target].push(source);
          }
        }

        const nodeConfig = {};
        for (const name of nodeNameSet) {
          const noteData = this.formData[`pipeline-node-${name}`];
          if (noteData) {
            nodeConfig[name] = noteData;
            nodeConfig[name]["dependsOn"] = [];
            if (name in stepDependsOn) {
              nodeConfig[name]["dependsOn"] = stepDependsOn[name];
            }
          }
        }

        kubeflowData["pipeline"]["flow"] = nodeConfig;
        resultData = { kubeflowData, edges, nodes };
      }
    }
    return resultData;
  }

  //added nodes for retrieving the label from node data - required for the recreate flow
  getParentNodeFlowPropertiesFor(nodeId, edges, nodes, pipeline, formData) {
    // console.log("edges", edges, "pipeline", pipeline, "formData", formData);
    const stepDependsOn = {};

    function flattenJSON(json, prefix = "") {
      let result = {};

      for (let key in json) {
        if (typeof json[key] === "object" && !Array.isArray(json[key])) {
          const flattenedObj = flattenJSON(json[key], `${prefix}${key}.`);
          result = { ...result, ...flattenedObj };
        } else {
          result[`${prefix}${key}`] = json[key];
        }
      }

      return result;
    }

    function getParentNode(nodeId, stepDependsOn, formData) {
      let parentNodeProps = [];
      if (JSON.stringify(formData) == "{}") {
        return parentNodeProps;
      }

      const traverseParents = (currentNodeId) => {
        if (currentNodeId in stepDependsOn) {
          const parentIds = stepDependsOn[currentNodeId];
          for (const parentId of parentIds) {
            //find the node where id matches parentId and get the label - required for the recreate flow
            if(!formData[parentId]){
              const label = nodes.find((obj) => obj.id === parentId).data.label; 
              parentNodeProps.push(
                flattenJSON(formData[label], `${formData[label]?.name}.`)
              );
            }
            else{
              parentNodeProps.push(
                flattenJSON(formData[parentId] || formData[label], `${formData[parentId]?.name}.`)
              );
            }
            // TODO: enable below line to show grand parent output variables
            // traverseParents(parentId);
          }
        }
      };

      traverseParents(nodeId);

      return parentNodeProps;
    }

    if (edges) {
      for (const edge of edges) {
        const source = edge["source"];
        const target = edge["target"];
        if (stepDependsOn[target] == null) {
          stepDependsOn[target] = [source];
        } else {
          stepDependsOn[target].push(source);
        }
      }
    }
    const parentNodeProps = getParentNode(nodeId, stepDependsOn, formData);
    const plConfig = pipeline;
    if (plConfig) {
      parentNodeProps.push(
        flattenJSON(plConfig["pipelineVariables"], "pipeline.variables.")
      );
    }
    const filteredData = parentNodeProps.map((obj) => {
      const filteredKeys = Object.keys(obj).filter(
        (key) => key.includes("output") || key.includes("variable")
      );
      const filteredObj = {};

      filteredKeys.forEach((key) => {
        filteredObj[key] = obj[key];
      });
      return filteredObj;
    });
    // console.log("filteredData", filteredData);
    return filteredData;
  }

  getFlowData(nodeList, edges, formData) {

    console.log("In getFlowData", nodeList, edges, formData);

    // for (const obj of nodeList) {
    //   const id = obj.id;
    //   if (id in formData) {
    //     result[id] = formData[id];
    //   }
    // }

    this.getDependsOn(nodeList, edges, formData);

    return this.getOrderByDependsOn(nodeList, edges, formData);
  }

  getDependsOn(nodes, edges, flowData) {
    // when only one node exists, simple append dependsOn[] to it and return;
    if (nodes.length == 1) {
      console.log("nodes", nodes, flowData);

      const nodeID = nodes[0].id;
      const nodeLabel = nodes[0].data.label;

      if (nodeID in flowData) flowData[nodeID]["dependsOn"] = [];
      else if (nodeLabel in flowData) flowData[nodeLabel]["dependsOn"] = [];
      return;
    }
    //process for multiple nodes
    const stepDependsOn = {};
    const nodeNameSet = new Set();

    console.log("getDependsOn", nodes, flowData);

    for (const edge of edges) {
      const source = edge["source"];
      const target = edge["target"];
      nodeNameSet.add(source);
      nodeNameSet.add(target);

      if (stepDependsOn[target] == null) {
        stepDependsOn[target] = [this.getlabelFromSrcId(source, nodes)];
      } else {
        stepDependsOn[target].push(this.getlabelFromSrcId(source, nodes));
      }
    }

    for (const nodeId of nodeNameSet) {
      //find the node where nodeid matches parentId and get the label - required for the recreate flow
      const label = this.getlabelFromSrcId(nodeId, nodes)
      if (flowData[nodeId]) {
        flowData[nodeId]["dependsOn"] = stepDependsOn[nodeId] || [];
      }
      else if (flowData[label]){
        flowData[label]["dependsOn"] = stepDependsOn[nodeId] || [];
      }
    }
  }

  getOrderByDependsOn(nodes, edges, flowData) {
    const nodeSeq = this.findCorrectNodeSequence(nodes, edges);

    // Reorder the object based on the correct sequence of nodes
    const flowData0 = this.reorderObjectBasedOnSequence(nodeSeq, flowData);

    return flowData0;
  }

  // reorders nodes from arrays
  findCorrectNodeSequence(nodes, edges) {
    const graph = new Map();
    const inDegrees = new Map();

    // Initialize graph and inDegrees
    for (const node of nodes) {
      graph.set(node.id, []);
      inDegrees.set(node.id, 0);
    }

    // Build the graph and calculate in-degrees
    for (const edge of edges) {
      graph.get(edge.source).push(edge.target);
      inDegrees.set(edge.target, inDegrees.get(edge.target) + 1);
    }

    // Perform topological sorting
    const queue = [];
    for (const [nodeId, degree] of inDegrees.entries()) {
      if (degree === 0) {
        queue.push(nodeId);
      }
    }

    const result = [];
    while (queue.length > 0) {
      const current = queue.shift();
      result.push(nodes.find((node) => node.id === current));
      for (const neighbor of graph.get(current)) {
        inDegrees.set(neighbor, inDegrees.get(neighbor) - 1);
        if (inDegrees.get(neighbor) === 0) {
          queue.push(neighbor);
        }
      }
    }
    return result;
  }

  // Reorder the object based on the correct sequence of nodes
  reorderObjectBasedOnSequence(nodesArray, flowData) {
    const reorderedObject = {};

    // Create a map to quickly find node data by ID
    // const nodeDataMap = new Map();
    // for (const node of nodesArray) {
    //   nodeDataMap.set(node.id, node.data);
    // }

    // Reorder the object based on the correct sequence of nodes
    for (const node of nodesArray) {
      const nodeId = node.id;
      const nodeLabel = node.data.label;

      if (flowData.hasOwnProperty(nodeId)) {
        reorderedObject[nodeId] = flowData[nodeId];
      } else if (flowData.hasOwnProperty(nodeLabel)) {
        reorderedObject[nodeLabel] = flowData[nodeLabel];
      }
    }

    return reorderedObject;
  }

  // --------------extra functions in case previous doesn't work--------------
  // reorderObjectBasedOnSequence1(nodesArray, edgesArray, originalObject) {
  //   const reorderedObject = {};

  //   // Create a map to quickly find node data by ID
  //   const nodeDataMap = new Map();
  //   for (const node of nodesArray) {
  //     nodeDataMap.set(node.id, node.data);
  //   }

  //   // Create a map to group nodes by their parent ID
  //   const parentChildMap = new Map();
  //   for (const edge of edgesArray) {
  //     const parentID = edge.source;
  //     const childID = edge.target;

  //     if (!parentChildMap.has(parentID)) {
  //       parentChildMap.set(parentID, []);
  //     }

  //     parentChildMap.get(parentID).push(childID);
  //   }

  //   // Function to recursively reorder children nodes
  //   function reorderChildren(parentID) {
  //     if (originalObject.hasOwnProperty(parentID)) {
  //       reorderedObject[parentID] = nodeDataMap.get(parentID);

  //       if (parentChildMap.has(parentID)) {
  //         const children = parentChildMap.get(parentID);
  //         for (const childID of children) {
  //           reorderChildren(childID);
  //         }
  //       }
  //     }
  //   }

  //   // Start reordering from the nodes with no parents
  //   const nodesWithNoParents = nodesArray.filter(
  //     (node) => !parentChildMap.has(node.id)
  //   );
  //   for (const node of nodesWithNoParents) {
  //     reorderChildren(node.id);
  //   }

  //   return reorderedObject;
  // }

  // getOrderByDependsOn(nodes, edges) {
  //   const jsonData = {
  //     edges: edges,
  //     nodes: nodes,
  //   };
  //   // Function to order the nodes based on the connected edges
  //   const orderNodesByEdges = (jsonData) => {
  //     const { edges, nodes } = jsonData;
  //     // Create a mapping of node IDs to their corresponding index in the nodes array
  //     const nodeIndexMap = new Map();
  //     nodes.forEach((node, index) => {
  //       nodeIndexMap.set(node.id, index);
  //     });
  //     // Helper function to get the index of the node in the nodes array based on its connection (source/target) in the edges
  //     const getNodeIndexFromEdge = (edge, target) => {
  //       const nodeId = target ? edge.target : edge.source;
  //       return nodeIndexMap.get(nodeId);
  //     };
  //     // Sort the nodes array based on the connected edges
  //     const sortedNodes = nodes.sort((a, b) => {
  //       const aSourceIndex = getNodeIndexFromEdge(
  //         edges.find((edge) => edge.target === a.id)
  //       );
  //       const bSourceIndex = getNodeIndexFromEdge(
  //         edges.find((edge) => edge.target === b.id)
  //       );
  //       // If the source node indexes are the same, compare the target node indexes
  //       if (aSourceIndex === bSourceIndex) {
  //         const aTargetIndex = getNodeIndexFromEdge(
  //           edges.find((edge) => edge.source === a.id),
  //           true
  //         );
  //         const bTargetIndex = getNodeIndexFromEdge(
  //           edges.find((edge) => edge.source === b.id),
  //           true
  //         );
  //         return aTargetIndex - bTargetIndex;
  //       }

  //       return aSourceIndex - bSourceIndex;
  //     });

  //     return sortedNodes;
  //   };
  //   console.log("orderNodesByEdges", orderNodesByEdges(jsonData));
  // }
  // getOrderByDependsOn(nodes, edges, flowData) {
  // Function to order the JSON data based on source and target fields
  // function orderEdges(edges) {
  //   try {
  //     const sortededges = edges.sort((a, b) => {
  //       if (a.source < b.source) return -1;
  //       if (a.source > b.source) return 1;
  //       if (a.target < b.target) return -1;
  //       if (a.target > b.target) return 1;
  //       return 0;
  //     });
  //     console.log("sortedEdges", sortededges);
  //     return sortededges;
  //   } catch (e) {
  //     console.log("in sortedges", e);
  //   }
  // }

  // function orderNodes(sortedEdges, nodes) {
  //   try {
  //     const prevOrderMap = new Map();
  //     sortedEdges.forEach((item, index) => prevOrderMap.set(item.id, index));
  //     const sortedData = nodes.sort((a, b) => {
  //       const aOrder = prevOrderMap.get(a.id);
  //       const bOrder = prevOrderMap.get(b.id);
  //       return aOrder - bOrder;
  //     });
  //     return sortedData;
  //   } catch (e) {
  //     console.log("in sortnodes", e);
  //   }
  // }

  // const sortededges = orderEdges(edges);

  // const sortednodes = orderNodes(sortededges, nodes);

  // console.log("sorted nodes", sortednodes);

  // getOrderByDependsOn(flowData) {
  //   const orderedflowData = {};

  //   function visit(flowItem) {
  //     if (!orderedflowData.hasOwnProperty(flowItem)) {
  //       const item = flowData[flowItem];
  //       item.dependsOn.forEach((parentKey) => visit(parentKey));
  //       orderedflowData[flowItem] = item;
  //     }
  //   }
  //   Object.keys(flowData).forEach((flowItem) => visit(flowItem));

  //   return orderedflowData;
  // }

  // getOrderByDependsOn(flowData) {
  //   {
  //     const result = [];
  //     const visited = new Set();
  //     const nodes = Object.keys(flowData);

  //     function visit(node) {
  //       if (!visited.has(node)) {
  //         visited.add(node);

  //         if (flowData[node] && flowData[node].dependsOn) {
  //           flowData[node].dependsOn.forEach((dependency) => {
  //             if (!visited.has(dependency)) {
  //               visit(dependency);
  //             }
  //           });
  //         }

  //         result.unshift(node);
  //       }
  //     }

  //     nodes.forEach(visit);

  //     const reorderedJSON = {};
  //     result.forEach((node) => {
  //       reorderedJSON[node] = flowData[node];
  //     });

  //     return reorderedJSON;
  //   }
  // }

  // reorderNodesByEdges = (inputData) => {
  //   const visitedNodes = new Set();
  //   const sortedNodes = [];

  //   const dfs = (nodeId) => {
  //     visitedNodes.add(nodeId);
  //     const edges = inputData.edges.filter((edge) => edge.source === nodeId);

  //     edges.forEach((edge) => {
  //       const targetId = edge.target;
  //       if (!visitedNodes.has(targetId)) {
  //         dfs(targetId);
  //       }
  //     });

  //     sortedNodes.unshift(inputData.nodes.find((node) => node.id === nodeId));
  //   };

  //   inputData.nodes.forEach((node) => {
  //     if (!visitedNodes.has(node.id)) {
  //       dfs(node.id);
  //     }
  //   });

  //   return { nodes: sortedNodes };
  // };

  // gets node.data.label from nodeId
  getlabelFromSrcId(nodeId, nodesList) {
    let nodeLabel = nodeId;
    const nodeMatch = nodesList.find((obj) => obj.id === nodeId);
    nodeLabel = nodeMatch ? nodeMatch.data.label : null;
    return nodeLabel;
  }
}

const usePipelineService = () => {
  const { formData } = useContext(FormDataContext);
  const { projectId } = useParams();

  return new PipelineService(formData, projectId);
};

export default usePipelineService;
