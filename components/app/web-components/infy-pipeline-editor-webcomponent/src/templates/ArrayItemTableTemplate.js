/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import React, { useState, useEffect } from "react";
import {
  ariaDescribedByIds,
  examplesId,
  getInputProps,
  labelValue,
} from "@rjsf/utils";

import Box from "@material-ui/core/Box";
import Grid from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";
import { getTemplate, getUiOptions } from "@rjsf/utils";
import FieldTemplate from "./FieldTemplate";
import BaseInputTemplate from "./BaseInputTemplate";

const ArrayItemTableTemplate = (props) => {
  const {
    canAdd,
    disabled,
    children,
    hasToolbar,
    hasCopy,
    hasMoveDown,
    hasMoveUp,
    hasRemove,
    onDropIndexClick,
    onReorderClick,
    onCopyIndexClick,
    index,
  } = props;

  const {
    idSchema,
    uiSchema,
    items,
    onAddClick,
    readonly,
    registry,
    required,
    schema,
    name,
    formData = {},
    onChange,
  } = children.props;

  const uiOptions = getUiOptions(uiSchema);
  // const referencedSchema = retrieveSchema(schema, undefined, {});
  const { title, properties } = schema;
  // Button templates are not overridden in the uiSchema
  const {
    ButtonTemplates: { AddButton },
  } = registry.templates;
  const { CopyButton, MoveDownButton, MoveUpButton, RemoveButton } =
    registry.templates.ButtonTemplates;
  const btnStyle = {
    flex: 1,
    paddingLeft: 6,
    paddingRight: 6,
    fontWeight: "bold",
    minWidth: 0,
  };
  // >>>>>>>>>>>>>..

  const [fields, setFields] = useState([[{ label: "", value: "" }]]);
  useEffect(() => {
    if (!isEmptyObject(properties)) {
      const convertObjectToFields = (obj) => {
        return Object.entries(obj).map(([label, value]) => {
          return { label, value: formData[label] || "" };
        });
      };
      const data = convertObjectToFields(properties);
      setFields([data]);
    }
  }, []);

  useEffect(() => {
    onFormChangeData(convertToKeyValues(fields));
  }, [fields]);

  const onFormChangeData = (data) => {
    if (!isEmptyObject(data)) {
      onChange({ ...formData, ...data });
    }
  };

  const updateValue = (fields, label, newValue) => {
    return fields.map((item) => {
      if (item.label === label) {
        return { ...item, value: newValue };
      }
      return item;
    });
  };

  const handleChange = (index, e) => {
    const { name, value } = e.target;
    const updatedFields = [...fields];
    updatedFields[index] = updateValue(updatedFields[index], name, value);

    onFormChangeData(convertToKeyValues(updatedFields)); // Call the callback function with the converted form data
    setFields(updatedFields);
  };

  const convertToKeyValues = (data) => {
    return data.map((arr) =>
      arr.reduce((acc, obj) => {
        acc[obj.label] = obj.value;

        return acc;
      }, {})
    );
  };
  return (
    <tbody style={{width:"100%", border:"CYAN 2px SOLID"}}>
      <tr>
        {Object.entries(formData).map(([label, value]) => (
          // return { label, value: formData[label] || "" };
          <td>
            <mat-form-field
              className="DSA_Wb_custom-form-field DSA_form_nofloatLabel"
              floatLabel="never"
              panelClass="DSA_wb-custom-select-panel"
            >
              <input
                key={`${index}`}
                type="text"
                name={label}
                size="sm"
                value={value}
                autoComplete="off"
                onChange={(e) => handleChange(index, e)}
              />

              {Array.isArray(schema.examples) && (
                <datalist id={examplesId(id)}>
                  {schema.examples
                    .concat(
                      schema.default &&
                        !schema.examples.includes(schema.default)
                        ? [schema.default]
                        : []
                    )
                    .map((example) => {
                      return <option key={example} value={example} />;
                    })}
                </datalist>
              )}
            </mat-form-field>
          </td>
        ))}
        <td>
          {hasToolbar && (
            <Grid item={true}>
              {hasRemove && (
                <RemoveButton
                  style={btnStyle}
                  disabled={disabled || readonly}
                  onClick={onDropIndexClick(index)}
                  uiSchema={uiSchema}
                  registry={registry}
                />
              )}
            </Grid>
          )}
        </td>
      </tr>

      {/* {fields.map((field1, index) => (
                <tr key={index}>
                    {field1.map((field, index1) => (
                        <td>
                            <mat-form-field
                                className="DSA_Wb_custom-form-field DSA_form_nofloatLabel"
                                floatLabel="never"
                                panelClass="DSA_wb-custom-select-panel">
                                <input key={`${index}-${index1}`}
                                    type="text" name={field.label}
                                    size="sm" value={field.value} list={`datalist-${name}-${index}-${index1}`}
                                    autoComplete="off" onChange={(e) => handleChange(index, e)} />

                                {Array.isArray(schema.examples) && (
                                    <datalist id={examplesId(id)}>
                                        {schema.examples
                                            .concat(
                                                schema.default && !schema.examples.includes(schema.default)
                                                    ? [schema.default]
                                                    : []
                                            )
                                            .map(example => {
                                                return <option key={example} value={example} />
                                            })}
                                    </datalist>
                                )}
                            </mat-form-field>
                        </td>
                    ))}


                </tr>
            ))} */}
    </tbody>
  );
};

function isEmptyObject(obj) {
  return JSON.stringify(obj) === "{}";
}
export default ArrayItemTableTemplate;
