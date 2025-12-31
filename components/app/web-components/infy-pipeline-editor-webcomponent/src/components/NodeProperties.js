/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import React, { useContext, useState, useEffect, useRef } from "react";
import { FormDataContext } from "../stores/form-datastore";
import usePipelineService from "../services/pipeline-service";
import Form from "@rjsf/material-ui";
import validator from "@rjsf/validator-ajv8";

// custom templates
import ArrayFieldItemTemplate from "../templates/ArrayFieldItemTemplate";
import ArrayFieldTemplate from "../templates/ArrayFieldTemplate";
import ObjectFieldTemplate from "../templates/ObjectFieldTemplate";
import FieldTemplate from "../templates/FieldTemplate";
import BaseInputTemplate from "../templates/BaseInputTemplate";
import WrapIfAdditionalTemplate from "../templates/WrapIfAdditionalTemplate";
import TitleFieldTemplate from "../templates/TitleFieldTemplate";

// custom fields
import CustomArrayToTableField from "../fields/CustomArrayToTableField";
import CustomArrayToTextField from "../fields/CustomArrayToTextField";
import CustomObjectToTableField from "../fields/CustomObjectToTableField";
import CustomTextboxField from "../fields/CustomTextboxField";
import SelectWidget from "../widgets/SelectWidget";
function NodeProperties({
  node,
  edges,
  //passing node data for recreate flow
  nodes,
  formSchemaData,
  formUiSchemaData,
  formPreData,
  isReadOnlyMode,
  suggestionVariables,
  passnewName,
  onNodeSave,
  onClose,
}) {
  const pipelineService = usePipelineService();
  const { formData, addFormData } = useContext(FormDataContext);

  const [formValues, setFormValues] = useState(formPreData || {});

  const [schema, setschema] = useState(formSchemaData);
  const [uiSchema, setUiSchema] = useState(formUiSchemaData);

  const log = (type) => console.log.bind(console, type);
  const [flag, setflag] = useState(false);
  const [postToParent, setPostToParent] = useState(false);
  const [postToParentOnSubmit, setPostToParentOnSubmit] = useState(false);

  const fields = {
    CustomTextboxField: CustomTextboxField,
    CustomArrayToTextField: CustomArrayToTextField,
    CustomObjectToTableField: CustomObjectToTableField,
    CustomArrayToTableField: CustomArrayToTableField,
  };

  //useEffect for setting name, example fields in Input/Output Variables.
  useEffect(() => {
    if (schema && !flag) {
      // sets initial name for the node.
      if (node.data.label) {
        setFormValues({ ...formValues, ["name"]: node.data.label });
      }

      console.log("fromValues", formValues);
      const { definitions } = schema;
      Object.keys(definitions).forEach((key) => {
        const { additionalProperties } = definitions[key];
        if (additionalProperties && "examples" in additionalProperties) {
          // get suggestion (pipeline + parent)
          const flatjson = pipelineService.getParentNodeFlowPropertiesFor(
            node.id,
            edges,
            //passing node data for recreate flow
            nodes,
            suggestionVariables,
            formData
          );
          const exampleData = [];
          Object.entries(flatjson).map(([key, value]) => {
            Object.keys(value).map((val) => {
              exampleData.push(`{{${val}}}`);
            });
          });
          // console.log("flatjson", exampleData);
          additionalProperties.examples = exampleData;
        }
      });
      setschema({ ...schema, ["definitions"]: definitions });
      
    }
    console.log("schema", schema);
    setflag(true);
  }, []);

  // send the save event, only when the context.formdata changes
  useEffect(() => {
    if (JSON.stringify(formData) !== "{}") {
      //the values in formdata are changed to effect the key as node's name if it is different in formdata - recreate flow
      console.log("Changes to effect the key as node's name if it is different in formdata", formData)
      Object.keys(formData).forEach((key) => {
        console.log("iterating the formdata keys",formData[key].name, node.data.label, formData[key].name == node.data.label && key != node.data.label);
        if (formData[key].name == node.data.label && key != node.data.label) {
          if (formData[formData[key].name]){
            console.log("before deletion", formData[formData[key].name]);
            delete formData[formData[key].name];
            console.log("after deletion of the old node's form data", formData);
          }
          formData[node.data.label] = formData[key];
          delete formData[key];
          console.log("Changes to name, inside if", formData)
        }
      });
      console.log("Form data changed pipwlinw", formData);
      onNodeSave(formData);
      setPostToParent(true);
    }
  }, [formData]);

  useEffect(() => {
    if (postToParent && postToParentOnSubmit) {
      onClose();
      setPostToParentOnSubmit(false);
      setPostToParent(false);
    }
  }, [postToParent, postToParentOnSubmit]);

  // splices the entryPoints array if any item has space separated values
  const normalizeEntryPoints = (formData) => {
    const { stepConfig } = formData;
    const { entryPoints } = stepConfig;

    const normalizedEntryPoints = entryPoints.flatMap((entryPoint) => {
      const values = entryPoint.trim().split(/\s+/);
      return values.map((value) => value.trim());
    });

    stepConfig.entryPoints = normalizedEntryPoints;

    return formData;
  };

  // adds new node to context.formData
  const handleSubmit = (formEvent_submit) => {
    const formData = formEvent_submit.formData;
    // const normalizedFormValues = normalizeEntryPoints({
    //   ...formData,
    //   stepConfig: {
    //     ...formData.stepConfig,
    //     entryPoints: formData.stepConfig.entryPoints.slice(),
    //   },
    // });
    addFormData(node.id, formData);
    setPostToParentOnSubmit(true);
  };

  //handle all form changes.
  const handleChange = (formEvent_change) => {
    setFormValues(formEvent_change.formData);
    handleIfNameChange(formEvent_change);
  };

  // handles name change and propagates it back to parent
  const handleIfNameChange = (formEvent_nameChange) => {
    if (formEvent_nameChange?.formData?.name) {
      let new_name = formEvent_nameChange.formData.name;
      new_name = new_name.trim();
      if (/^([a-zA-Z0-9]+)$/.test(new_name)) {
        log("new_name : ", new_name);
        passnewName(new_name);
      } else {
        console.log("error name", new_name);
      }
    }
  };

  // validate name field for alphanumeric and no spaces.
  const validateNameAndImage = (formData, errors) => {
    if (formData?.name) {
      let formName = formData.name;
      formName = formName.trim();
      if (formName && !/^([a-zA-Z0-9]+)$/.test(formName))
        errors.name.addError(
          "Name should be alphanumeric and not contain spaces"
        );
    }

    if(formData?.imageUri){
      let image = formData.imageUri.trim();
      const imageRegex = /^infyartifactory\.jfrog\.io\/[A-Za-z\-\/_]+:[vV](\d+([\._]\d)*)/
      if(image && !imageRegex.test(image))
        errors.imageUri.addError(
      "Invalid image URI"
      )
    }
    return errors;
  };
  // const validateName = (formData, errors) => {
  //   if (formData?.name) {
  //     let formName = formData.name;
  //     formName = formName.trim();
  //     if (formName && !/^([a-zA-Z0-9]+)$/.test(formName))
  //       errors.name.addError(
  //         "Name should be alphanumeric and not contain spaces"
  //       );
  //   }
  //   return errors;
  // };

  return (
    <>
      {schema && (
        <aside className="node-prop">
          <div>
            <h4 style={{ marginLeft: "20px" }}>Node Properties</h4>
          </div>
          <Form
            //readonlyprop
            disabled={isReadOnlyMode}
            //structural props
            schema={schema}
            uiSchema={uiSchema}
            formData={formValues}
            //validation props
            liveValidate={true}
            validator={validator}
            showErrorList={false}
            // customValidate={validateName}
            customValidate={validateNameAndImage}
            //state handlers
            onChange={handleChange}
            onSubmit={handleSubmit}
            onError={log("errors")}
            templates={{
              TitleFieldTemplate,
              ArrayFieldItemTemplate,
              ArrayFieldTemplate,
              ObjectFieldTemplate,
              FieldTemplate,
              BaseInputTemplate,
              WrapIfAdditionalTemplate,
            }}
            widgets={{ SelectWidget }}
            fields={fields}
          >
            <div
              className="modal-footer"
              style={{ marginTop: "20px", marginRight: "50px" }}
            >
              <button
                type="submit"
                disabled={isReadOnlyMode || false}
                                className="tf_button"
              >
                Ok
              </button>{" "}
              <button
                type="button"
                onClick={() => onClose()}
                className="tf_button_secondary"
              >
                Close
              </button>
            </div>
          </Form>
        </aside>
      )}
    </>
  );
}

export default NodeProperties;
