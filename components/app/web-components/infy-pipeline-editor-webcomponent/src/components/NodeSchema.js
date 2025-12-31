/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

export const GENRIC_NODE_PROP_SCHEMA = {
  $ref: "#/definitions/main",
  definitions: {
    main: {
      type: "object",
      // additionalProperties: false,
      properties: {
        name: {
          type: "string",
          title: "Name",
        },
        type: {
          type: "string",
          title: "Type",
        },
        input: {
          $ref: "#/definitions/Input",
        },
        output: {
          $ref: "#/definitions/Output",
        },
        stepConfig: {
          $ref: "#/definitions/StepConfig",
        },
        resourceConfig: {
          $ref: "#/definitions/ResourceConfig",
        },
      },
      required: ["name"],
    },
    Input: {
      type: "object",
      properties: {},
      required: [],
      title: "Input",
      additionalProperties: {
        type: "string",
        examples: [],
      },
    },
    Output: {
      type: "object",
      properties: {},
      required: [],
      title: "Output",
      additionalProperties: {
        type: "string",
        examples: [],
      },
    },
    ResourceConfig: {
      type: "object",
      additionalProperties: false,
      properties: {
        computes: {
          title: "Computes",
          type: "array",
          items: {
            $ref: "#/definitions/Compute",
          },
        },
        volumeSizeinGB: {
          title: "Volume Size in GB",
          type: "number",
        },
      },
      required: [],
      title: "ResourceConfig",
    },
    Compute: {
      type: "object",
      properties: {
        type: {
          title: "Type",
          type: "string",
          enumNames: ["CPU", "GPU"],
        },
        maxQty: {
          title: "Max Qty",
          type: "integer",
        },
        memory: {
          title: "Memory",
          type: "string",
        },
        minQty: {
          title: "Min Qty",
          type: "integer",
        },
      },
      required: [],
      title: "Compute",
    },
    StepConfig: {
      type: "object",
      additionalProperties: false,
      properties: {
        entryPoint: {
          title: "Entry Point",
          type: "array",
          items: {
            type: "string",
          },
        },
        stepArguments: {
          title: "Step Arguments",
          type: "array",
          items: {
            type: "string",
          },
        },
        imageUri: {
          title: "Image URI",
          type: "string",
        },
      },
      required: [],
      title: "Step Config",
    },
  },
};

export const GENERIC_FORM_PREFILL_DATA = {
  name: "",
  type: "PlaceHolder_Generic",
  // dependsOn: [],
  input: {
    name: "",
    doc_folder_path: "",
    doc_file_name: "",
  },
  output: {
    name: "/name.txt",
    folder_path: "/folder_path.txt",
    file_name: "/file_name.txt",
  },
  stepConfig: {
    entryPoint: ["python", "main.py"],
    stepArguments: [],
    imageUri: "image-uri",
  },
  resourceConfig: {
    computes: [
      {
        type: "CPU",
        maxQty: 5,
        memory: "10GB",
        minQty: 1,
      },
    ],
    volumeSizeinGB: 0.1,
  },
};

export const pipelineData = {
  pipeline: {
    variables: {
      name: "mmsrepo",
      doc_folder_path: "a/b/c",
      doc_file_name: "invoice.pdf",
    },
  },
};

export const UI_SCHEMA = {
  name: {
    "ui:autofocus": true,
  },
  // type: {
  //   // "ui:field": "CustomTextboxField"
  // },
  input: {
    // "ui:field": "CustomObjectToTableField",
    additionalProperties: {
      "ui:title": "",
    },
  },
  output: {
    // "ui:field": "CustomObjectToTableField",
    additionalProperties: {
      "ui:title": "",
    },
  },
  stepConfig: {
    entryPoint: {
      // "ui:field": "CustomArrayToTextField",
      items: {
        "ui:title": "",
      },
    },
    stepArguments: {
      // "ui:field": "CustomArrayToTextField",
      items: {
        "ui:title": "",
      },
    },
    // imageUri: {
    //   // "ui:field": "CustomTextboxField"
    // }
  },
  resourceConfig: {
    computes: {
      // "ui:field": "CustomArrayToTableField"
    },
    volumeSizeinGB: {
      // "ui:field": "CustomTextboxField"
    },
  },
};
