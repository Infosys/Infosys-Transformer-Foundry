/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import React, {
  useState,
  useRef,
  useCallback,
  useContext,
  useEffect,
} from "react";
import ReactFlow, {
  ReactFlowProvider,
  addEdge,
  useNodesState,
  useEdgesState,
  Controls,
  Background,
} from "reactflow";
import "reactflow/dist/style.css";
import NodePanel from "./NodePanel";
import NodeProperties from "./NodeProperties";
import CommonUtil from "../utils/common-util";
import { FormDataContext } from "../stores/form-datastore";
import { toast } from "react-toastify";

import { v4 as uuidv4 } from "uuid";
import usePipelineService from "../services/pipeline-service";

let id = 0;
const getId = () => uuidv4();

const ReactFlowWrapper = ({
  nodeData,
  pipeline, //has edges,  nodes, flowData, variables, sequence
  nodeSetting,
  isReadOnlyMode,
}) => {
  const pipelineService = usePipelineService();

  const reactFlowWrapper = useRef(null);
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [sequence, setSequence] = useState({});
  const [reactFlowInstance, setReactFlowInstance] = useState(null);
  const [selectedNode, setSelectedNode] = useState(null);

  const { formData, clearFormData, setNewFormData } =
    useContext(FormDataContext);

  const [panelData, setpanelData] = useState([]);
  const [namedNodeData, setNamedNodeData] = useState([]);
  const [namedNodeUiSchema, setNamedNodeUiSchema] = useState({});

  const newflattenJSON = (json, prefix = "") => {
    let result = {};

    for (let key in json) {
      if (typeof json[key] === "object" && !Array.isArray(json[key])) {
        const flattenedObj = newflattenJSON(json[key], `${prefix}${key}.`);
        result = { ...result, ...flattenedObj };
      } else {
        result[`${prefix}${key}`] = json[key];
      }
    }

    return result;
  };

  const [nodeStore, setNodeStore] = useState({});

  // initialize nodepanel, nodeproperties, nodeuischema
  useEffect(() => {
    if (pipeline?.flowdata) {
      Object.entries(pipeline.flowdata).map(([key, value]) => {
        value["name"] = key;
      });
      setNewFormData(pipeline.flowdata);
    }
    setpanelData(nodeData["nodePanelSchema"]);
    setNamedNodeData(nodeData["namedNodePropertySchema"]);
    setNamedNodeUiSchema(nodeData["namedNodeUiSchema"]);
  }, []);

  // initialize nodes and edges for react flow
  useEffect(() => {
    if (pipeline?.nodes) {
      setNodes(pipeline["nodes"]);
      setEdges(pipeline["edges"]);
      setSequence(pipeline["sequence"] || {});
    }
  }, [pipeline]);

  // emit pipeline on change.
  useEffect(() => {
    // console.log("useEffect", nodes);
    if (!isReadOnlyMode && nodes && nodes.length > 0) {
      emitPipelineChange({ nodes: nodes, edges: edges, sequence: sequence });
    }
  }, [nodes, edges, sequence]);

  //empty condition
  useEffect(() => {
    if (selectedNode) {
      // No click event propagation not required.
      // emitNodeClicked(selectedNode);
    } else {
      // setNodePropFormData({});
    }
  }, [selectedNode]);

  // Fetches data for a node already in flow.
  const fetchExistingData = (node) => {
    console.log("fetchExistingData - Node", node, "formData ", formData);
    if (formData && JSON.stringify(formData) !== "{}") {
      var obj =
        formData[node.data.label] ||
        formData[node.id] ||
        fetchNodePrefillData(node);
      if (obj) delete obj.dependsOn;
      return obj;
    } else {
      return fetchNodePrefillData(node);
    }
  };

  // fetch if any default data is present for a node based on namedId
  const fetchNodePrefillData = (node) => {
    // TODO
    var prefill =
      nodeData.namedFormDefaultData[node.data.nodeAttribute.namedId];
    return prefill !== "{}" ? prefill : {};
  };

  // fetches the form data for the node based on propertyNamedRef value.
  const fetchNodePropFormData = (node) => {
    if (namedNodeData) {
      const nodeFormSchema =
        namedNodeData[node.data.nodeAttribute.propertyNamedRef];
      // console.log("nodeFormSchema", nodeFormSchema);
      return nodeFormSchema;
    }
    return null;
  };

  // fetch the uiSchema for the node based on uiNamedRef value.
  const fetchFormConfig = (node) => {
    if (namedNodeData) {
      const nodeFormUiSchema =
        namedNodeUiSchema[node.data.nodeAttribute.uiNamedRef];
      // console.log("nodeFormUiSchema", nodeFormUiSchema);
      return nodeFormUiSchema;
    }
    return null;
  };

  // whenever a node is saved or ~a edge connected~ , call this function to emit the flow.
  const handleNodeSave = (received_formData) => {
    console.log("handleNodeSave called");
    try {
      if (!isReadOnlyMode && received_formData) {
        console.log("handleNodeSave called, in try");
        const flow = pipelineService.getFlowData(
          nodes,
          edges,
          received_formData
        );
        console.log("emitFlowChange", flow);
        emitFlowChange(flow);
      }
    } catch (e) {
      console.log(e);
    }
  };

  // Emits a flow when a node is saved.
  // User should ensure edges are connected before saving.
  const emitFlowChange = (flowData) => {
    // if (JSON.stringify(flowData) !== "{}") {
    if (true) {
      flowData = processFlowData(flowData);
      flowData = validateStructure(flowData);
      console.log("emitFlowChange: ", flowData);
      const event = new CustomEvent("onFlowChange", { detail: flowData });
      window.dispatchEvent(event);
    }
  };

  // Removes uuid and puts name as top level keys before emitting.
  // also removes the name key.
  const processFlowData = (flowDataWithUUID) => {
    const flowDataWithNames = Object.keys(flowDataWithUUID).reduce(
      (result, key) => {
        const { name, ...otherprops } = flowDataWithUUID[key];
        if ("name" in otherprops) delete otherprops["name"];
        result[name] = otherprops;
        return result;
      },
      {}
    );
    return flowDataWithNames;
  };

  //function to handle case where user doesn't add any input/output to a node
  const validateStructure = (flowData) => {
    const validFlow = flowData;
    Object.keys(flowData).forEach((key) => {
      const props = Object.keys(flowData[key]);
      if (!"input" in props) validFlow[key]["input"] = {};
      if (!"output" in props) validFlow[key]["output"] = {};
    });
    return validFlow;
  };

  // emits pipeline change event
  const emitPipelineChange = (pipelineData) => {
    console.log("emitPipelineChange: ", pipelineData);
    const event = new CustomEvent("onPipelineChange", { detail: pipelineData });
    window.dispatchEvent(event);
  };

  const onNodeDoubleClick = (event, node) => {
    if (event.target.classList.contains("react-flow__handle-remove")) {
      onNodeDelete(node);
      // setNodePropFormData({});
    } else {
      setSelectedNode(node);
      // setNodePropFormData(fetchNodePropFormData(node));
    }
  };

  // deletes nodes if in create mode, No action otherwise.
  const onNodeDelete = useCallback((nodesToRemove) => {
    if (!isReadOnlyMode) {
      setNodes(
        // filteredNodes
        (prevElements) =>
          prevElements.filter((el) => el.id !== nodesToRemove[0].id)
      );
      // clearFormData(node);

      // console.log("here shuld be emit flow", nodes, nodesTemp, edges, formData);

      // const nodesTemp = removeItem(nodesToRemove[0]);
      emitPipelineChange({
        nodes: nodes,
        edges: edges,
        sequence: sequence,
      });

      const flow = pipelineService.getFlowData(nodes, edges, formData);
      console.log("onNodeSave, now flow", flow);
      emitFlowChange(flow);
    }
  }, []);
  

  // validate if a valid edge is connected
  // ChangeLog: changed the function from callback to normal function
  const onConnect = (connection) => {
    if (!isReadOnlyMode) {
      if (checkConnectionValidity(connection))
        setEdges((eds) => addEdge({ ...connection, animated: true }, eds));
    } else {
      toast(`Cannot add edge in read only mode`, {
        type: "error",
        position: toast.POSITION.BOTTOM_CENTER,
      });
    }
  };

  const checkConnectionValidity = (connection) => {
    console.log("checkConnectionValidity", connection);
    const sourceAttr = nodes.find((n) => n.id === connection.source).data
      .nodeAttribute;
    const targetAttr = nodes.find((n) => n.id === connection.target).data
      .nodeAttribute;

    //if parentNamedIds has no values defined, all parent edges are possible.
    if (
      targetAttr.parentNamedIds.length === 0 ||
      targetAttr.parentNamedIds.includes(sourceAttr.namedId)
    )
      return true;
    else {
      toast(
        `Invalid relationship: ${sourceAttr.namedId} cannot be parent of ${targetAttr.namedId}`,
        { type: "error", position: toast.POSITION.BOTTOM_CENTER }
      );
      return false;
    }
  };

  const onDragOver = useCallback((event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = "move";
  }, []);

  const onDrop = useCallback(
    (event) => {
      event.preventDefault();

      // dont allow drop if in readonly mode.
      if (isReadOnlyMode) return;

      const reactFlowBounds = reactFlowWrapper.current.getBoundingClientRect();
      const nodeProp = JSON.parse(
        event.dataTransfer.getData("application/pipeline-editor")
      );

      //if node of type x is already present in flow, increment the sequence number.
      // else add x to sequence with value 1.
      if (nodeProp.name in sequence) {
        sequence[nodeProp.name] = sequence[nodeProp.name] + 1;
      } else {
        sequence[nodeProp.name] = 1;
      }

      const nodeNumber = sequence[nodeProp.name];
      // remove spaces from default node name.
      const nodeName = nodeProp.name.replace(/[^a-zA-Z0-9]/g, "");

      const position = reactFlowInstance.project({
        x: event.clientX - reactFlowBounds.left,
        y: event.clientY - reactFlowBounds.top,
      });

      const nodeId = getId();

      let newNode = {
        id: nodeId,
        type: "default",
        position,
        data: {
          label: `${nodeName}${nodeNumber}`,
          // propertyNamedRef: nodeProp.propertyNamedRef,
          nodeAttribute: nodeProp.nodeAttribute,
        },
        deletable: true,
        sourcePosition: "right",
        targetPosition: "left",
        style: {
          width: "auto",
          height: "auto",
          padding: 5,
          background:
            nodeProp.nodeAttribute["backgroundColor"] || "rgb(221, 221, 221)",
          color: "#333",
          border: "1px solid #222138",
        },
      };

      if (nodeSetting && Object.keys(nodeSetting).length > 0) {
        newNode = CommonUtil.deepMerge({}, newNode, nodeSetting);
      }
      setNodes((nds) => nds.concat([newNode]));
      // console.log("onDrop", reactFlowInstance.getNodes());
    },
    [reactFlowInstance]
  );

  //here name of node change should reflect, change the nodesValue.
  //change in nodes state to change it instantly
  const onNodeNameChangeInNodeProp = (new_name) => {
    setNodes((prevNodes) => {
      const updateNodes = prevNodes.map((node) => {
        if (node.id === selectedNode.id) {
          return { ...node, data: { ...node.data, label: new_name } };
        }
        return node;
      });
      return updateNodes;
    });
  };

  return (
    <div style={{ height: "100vh" }} className="dndflow">
      <NodePanel
        nodePanelData={{ panelData }}
        isReadOnlyMode={isReadOnlyMode}
      />
      <ReactFlowProvider>
        <div className="reactflow-wrapper" ref={reactFlowWrapper}>
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            // if this prop passed, it triggers multiple times for any edge.
            // isValidConnection={checkConnectionValidity}
            onInit={setReactFlowInstance}
            onDrop={onDrop}
            onDragOver={onDragOver}
            onNodeDoubleClick={onNodeDoubleClick}
            deleteKeyCode={isReadOnlyMode ? null : "Delete"}
            onNodesDelete={onNodeDelete}
          >
            <Background color="#ccc" variant={"lines"} />
            <Controls />
          </ReactFlow>
        </div>
      </ReactFlowProvider>
      {selectedNode && (
        <NodeProperties
          node={selectedNode}
          // // TODO Pass nodeProperty data
          edges={edges}
          //passing node data for recreate flow
          nodes={nodes}
          // send schema
          formSchemaData={fetchNodePropFormData(selectedNode)}
          formUiSchemaData={fetchFormConfig(selectedNode)}
          formPreData={fetchExistingData(selectedNode)}
          isReadOnlyMode={isReadOnlyMode || false}
          suggestionVariables={pipeline}
          //pass related functions
          passnewName={onNodeNameChangeInNodeProp}
          onNodeSave={handleNodeSave}
          onClose={() => setSelectedNode(null)}
        />
      )}
    </div>
  );
};

export default ReactFlowWrapper;
