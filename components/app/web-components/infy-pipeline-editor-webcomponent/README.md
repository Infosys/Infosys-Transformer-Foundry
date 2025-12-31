# pipeline-editor

#### Build

`npm run build`

Command used to generate `*bundle.js` of web component.

#### Run

`npm run start`

### `Input` _(via props)_

```js
//in parent application, refer examples below for detailed input structure
<body>
  <pipeline-editor></pipeline-editor>
  <script>
    const NODE_DATA = { "nodePanelSchema": [], "namedNodePropertySchema": {}, "namedNodeUiSchema": {} }
    const PIPELINE_DATA = { "flowData": {}, "nodes": [], "edges": [], "sequence": {} }

    window.addEventListener('load', function () {
      window.dispatchEvent(new CustomEvent('receiveDataFromParent', {
        detail: { nodeData: NODE_DATA, pipeline: PIPELINE_DATA, isReadOnlyMode: false }
      }));
    });
  </script>
</body>
```

| Prop name      | Description                                                                                                                                                                      |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| nodeData       | contains node configuration details for creating side panel, providing nodes their form properties and values.<br> `{nodepanel:[],namedNodePropertySchema:{}, namedNodeUiSchema:{}}` |
| pipeline       | contains existing pipeline details for plotting the pipeline on the canvas if any.<br> `{pipelineVariables:{}, flowData:{}, nodes:[], edges:[], sequence:{}}`                    |
| isReadOnlyMode | `boolean` marks if flow and details are editable.<br> Default is `true`                                                                                                          |

### `Output` _(via events)_

In web component, emitting data on certain events such as node save or pipeline change

```js
//to emit flow details
const event = new CustomEvent("onFlowChange", { detail: flowData });
window.dispatchEvent(event);

//to emit pipeline details
const event = new CustomEvent("onPipelineChange", { detail: pipelineData });
window.dispatchEvent(event);
```

In parent app, handling emitted values and adding them to apps local storage.

```js
window.addEventListener("onPipelineChange", function (event) {
  const data = event.detail; // Access the data sent from the React web component
});

window.addEventListener("onNodeDoubleClick", function (event) {
  const data = event.detail; // Access the data sent from the React web component
});
```

| Prop name | Description                                                                                                                                                                     |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| pipelineData  | this variable is emitted everytime the canvas changes. (new node created, node moved, edges added, node deleted). <br>`{ edges:[], nodes:[], sequence:{} }`                     |
| flowData  | this node contains the flow ( diagram created by user on canvas ) along with the details of each node and its relation with other nodes.<br> eg. `{ "node1": {}, "node2': {} }` |

##### _Note\* - canvas is the space where uses can drag and drop nodes and create flows_

## *Example Input *to* web component*

### `nodeData`
contains configuration for side panel, `rjsf` form structure for each node type and uiSchema for configuring the properties within form for

```js
const nodeData = {
      "nodePanelSchema": [
        {
          "group": "Generic",
          "nodes": [
            {
              "label": "Node",
              "propertyNamedRef": "custom-1"
            },
            {
              "label": "K V Pair",
              "propertyNamedRef": "custom-1"
            }
          ]
        }],
      "namedNodePropertySchema": {
        "custom-1": {
          "$ref": "#/definitions/main",
          "definitions": {
            "main": {
              "type": "object",
              "additionalProperties": false,
              "properties": {
                "name": {
                  "type": "string",
                  "title": "Name"
                },
                "type": {
                  "type": "string",
                  "title": "Type",
                  "default": "generic"
                },
                "input": {
                  "$ref": "#/definitions/Input"
                },
                "output": {
                  "$ref": "#/definitions/Output"
                },
                "stepConfig": {
                  "$ref": "#/definitions/StepConfig"
                },
                "resourceConfig": {
                  "$ref": "#/definitions/ResourceConfig"
                }
              },
              "required": [
                "name",
                "type",
                "input",
                "output",
              ]
            },
            "Input": {
              "type": "object",
              "properties": {
              },
              "required": [

              ],
              "title": "Input",
              "additionalProperties": {
                "type": "string",
                "title": "Value",
                "examples": [

                ]
              }
            },
            "Output": {
              "type": "object",
              "properties": {
              },
              "required": [

              ],
              "title": "Output",
              "additionalProperties": {
                "type": "string",
                "title": "Value",
                "examples": [

                ]
              }
            },
            "ResourceConfig": {
              "type": "object",
              "additionalProperties": false,
              "properties": {
                "computes": {
                  "title": "Computes",
                  "type": "array",
                  "minItems": 1,
                  "items": {
                    "$ref": "#/definitions/Compute"
                  }
                },
                "volumeSizeinGB": {
                  "title": "Volume Size in GB",
                  "type": "number"
                }
              },
              "required": [
              ],
              "title": "Resource Configuration"
            },
            "StepConfig": {
              "type": "object",
              "additionalProperties": false,
              "properties": {
                "entryPoint": {
                  "title": "Entry Point",
                  "type": "array",
                  "items": {
                    "type": "string"
                  }
                },
                "stepArguments": {
                  "title": "Step Arguments",
                  "type": "array",
                  "items": {
                    "type": "string"
                  }
                },
                "imageUri": {
                  "title": "Image URI",
                  "type": "string"
                }
              },
              "required": [

              ],
              "title": "Step Config"
            },
            "Compute": {
              "type": "object",
              "additionalProperties": false,
              "description": "CPU/GPU parent",
              "properties": {
                "type": {
                  "title": "Type",
                  "type": "string",
                  "enum": ["CPU", "GPU"]
                },
                "maxQty": {
                  "title": "Max Qty",
                  "type": "integer"
                },
                "memory": {
                  "title": "Memory",
                  "type": "string"
                },
                "minQty": {
                  "title": "Min Qty",
                  "type": "integer",
                  "minimum": 0
                }
              },
              "required": [

              ],
              "title": "Compute"
            }
          }
        }
      },
      "namedNodeUiSchema": {
        "custom-1": {
          "name": {
            "ui:autofocus": true
          },
          "type": {
            "ui:disabled": true
          },
          "input": {
            "additionalProperties": {
              "ui:title": ""
            }
          },
          "output": {
            "additionalProperties": {
              "ui:title": ""
            }
          },
          "stepConfig": {
            "entryPoint": {
              "items": {
                "ui:title": ""
              }
            },
            "stepArguments": {
              "items": {
                "ui:title": ""
              }
            }
          },
          "resourceConfig": {
            "computes": {
               "ui:field": "CustomArrayToTableField"
            },
            "volumeSizeinGB": {
            }
          },
        }
      }
    }
```

### `pipeline`
contains existing pipline details, these are used to plot the existing pipeline data,
everytime the web component reloads or when it opens in read only mode.

```js
const pipeline = {
  "pipelineVariables": {
    "variables": {
      //variables come from the pipeline details page.
    }
  },
  //---------------------two node config example---------------------
  "flowData": {
    "Step1": {
      "type": "generic",
      "dependsOn": [],// empty because first node
      "input": {
        //entered values
        key : value  // value suggestions from pipeline details
        },
      "output": {
      //entered values
        key : value
      },
      "stepConfig": {
        "entryPoint": [],
        "stepArguments": [],
        "imageUri": string
      },
      "resourceConfig": {
        "computes": [
          {
            "type": "CPU"|"GPU",
            "maxQty": number,
            "memory": string   // eg. - "10GB"
            "minQty": number
          }
        ],
        "volumeSizeinGB": number
      }
    },

    "Step2": {
      "type": "generic",
      "dependsOn": [
        "Step1" // parent nodes
      ],
      "input": {
        // user entered values.
        key : value // value suggestions from pipeline details and parent node
      },
      "output": {
        key : value
      },
      "stepConfig": {
        "entryPoint": [],
        "stepArguments": [],
        "imageUri": string
      },
      "resourceConfig": {
        "computes": [
          {
            "type": "CPU"|"GPU",
            "maxQty": number,
            "memory": string   // eg. - "10GB"
            "minQty": number
          }
        ],
        "volumeSizeinGB": number
      },
    }
  },
  "nodes": [
    {
      "id": "a7699b46-fa60-4925-b91b-c30aca1ef250",
      "type": "default",
      "position": {
        "x": 314.85936737060547,
        "y": 161.25
      },
      "data": {
        "label": "Step1",
        "propertyNamedRef": "custom-1"
      },
      "deletable": true,
      "sourcePosition": "right",
      "targetPosition": "left",
      "style": {
        "fontSize": 6,
        "width": "auto",
        "height": "auto",
        "padding": 5,
        "background": "rgb(221, 221, 221)",
        "color": "#333",
        "border": "1px solid #222138"
      },
      "width": 27,
      "height": 18,
      "selected": false,
      "positionAbsolute": {
        "x": 314.85936737060547,
        "y": 161.25
      },
      "dragging": false
    },
    {
      "id": "5f85cd51-f77f-463c-bd56-da3e170d1dc9",
      "type": "default",
      "position": {
        "x": 379.85936737060547,
        "y": 127.75
      },
      "data": {
        "label": "Step2",
        "propertyNamedRef": "custom-1"
      },
      "deletable": true,
      "sourcePosition": "right",
      "targetPosition": "left",
      "style": {
        "fontSize": 6,
        "width": "auto",
        "height": "auto",
        "padding": 5,
        "background": "rgb(221, 221, 221)",
        "color": "#333",
        "border": "1px solid #222138"
      },
      "width": 27,
      "height": 18,
      "selected": false,
      "positionAbsolute": {
        "x": 379.85936737060547,
        "y": 127.75
      },
      "dragging": false
    }
  ],
       "edges": [
         {
           "source": "a7699b46-fa60-4925-b91b-c30aca1ef250",
           "sourceHandle": null,
           "target": "5f85cd51-f77f-463c-bd56-da3e170d1dc9",
           "targetHandle": null,
           "animated": true,
           "id": "reactflow__edge-a7699b46-fa60-4925-b91b-c30aca1ef250-5f85cd51-f77f-463c-bd56-da3e170d1dc9"
         },
      ],
       "sequence": {
         node-type : number
         // (exapmle: "TableExtraction : 2 )
       }
}
```

### `isReadOnlyMode`
marks wheather to open the web component in read only mode, editing of nodes and their properties is disabled.

```js
const isReadOnlyMode: boolean
```

## Example outputs _from_ web component
_these values are emitted by event dispatchers from the web component and must be handled by parent._
##### names of emitted variables are arbitrary and only used to represent them here, since data is bound to  `event.details`
### `pipeline`
`nodes[]` and `edges[]` are generated by react-flow<br>

`sequence` depends on number of nodes and is used to maintain the proper node numering.

```js
{
  "nodes": [
    {
      "id": "4695fc16-9c40-4811-92af-06f70c321c21",
      "type": "default",
      "position": {
        "x": 190,
        "y": 117.85415649414062
      },
      "data": {
        "label": "Node1",
        "propertyNamedRef": "custom-1"
      },
      "deletable": true,
      "sourcePosition": "right",
      "targetPosition": "left",
      "style": {
        "width": "auto",
        "height": "auto",
        "padding": 5,
        "background": "rgb(221, 221, 221)",
        "color": "#333",
        "border": "1px solid #222138"
      },
      "width": 47,
      "height": 23
    },
    {
      "id": "35838ce0-186f-4bbf-bee2-59941c2850b9",
      "type": "default",
      "position": {
        "x": 444,
        "y": 186.85415649414062
      },
      "data": {
        "label": "Node2",
        "propertyNamedRef": "custom-1"
      },
      "deletable": true,
      "sourcePosition": "right",
      "targetPosition": "left",
      "style": {
        "width": "auto",
        "height": "auto",
        "padding": 5,
        "background": "rgb(221, 221, 221)",
        "color": "#333",
        "border": "1px solid #222138"
      },
      " width": 47,
      " height": 23
    }
  ],

  "edges": [
    {
      "source": "4695fc16-9c40-4811-92af-06f70c321c21",
      "sourceHandle": null,
      "target": "35838ce0-186f-4bbf-bee2-59941c2850b9",
      "targetHandle": null,
      "animated": true,
      "id": "reactflow__edge-4695fc16-9c40-4811-92af-06f70c321c21-35838ce0-186f-4bbf-bee2-59941c2850b9"
    }
  ],

  "sequence": {
    "Node": 2
  },
}
```

### `flowData`

details of each node, where UUID had been replaced by node name.

```js
"flowData": {
  "Node1": {
    "type": "generic",
    "stepConfig": {
      "entryPoint": ["x"],
      "stepArguments": [],
      "imageUri": "s"
    },
    "resourceConfig": {
      "computes": [
        {
          "type": "CPU",
          "memory": "10GB",
          "maxQty": 5,
          "minQty": 1
        }
      ],
      "volumeSizeinGB": 0.1
    },
    "dependsOn": []
  },
  "Node2": {
    "type": "generic",
    "stepConfig": {
      "entryPoint": ["y"],
      "stepArguments": [],
      "imageUri": "x"
    },
    "resourceConfig": {
      "computes": [
        {
          "type": "CPU",
          "memory": "10GB",
          "maxQty": 5,
          "minQty": 1
        }
      ],
      "volumeSizeinGB": 0.1
    },
    "input": {},
    "output": {},
    "dependsOn": ["Node1"]
  }
}


```
