/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import React, { useState, useEffect } from "react";
import { Box, Grid, MenuItem, Select, TextField } from "@material-ui/core";
import SelectWidget from "../widgets/SelectWidget";

function isEmptyObject(obj) {
  return JSON.stringify(obj) === "{}";
}
const DynamicTableForm = ({
  properties,
  formData,
  initialDataKey,
  onFormChange,
  pprops,
  disabled,
}) => {
  const { uiSchema, registry } = pprops;
  const { CopyButton, MoveDownButton, MoveUpButton, RemoveButton } =
    registry.templates.ButtonTemplates;
  const btnStyle = {
    flex: 1,
    paddingLeft: 6,
    paddingRight: 6,
    fontWeight: "bold",
    minWidth: 0,
  };
  const schemaTypeToHtml = {
    string: "text",
    integer: "number",
  };
  const [header, setHeader] = useState([]);
  // let fieldData = {}
  const [fieldData, setFieldData] = useState({});
  const [fields, setFields] = useState([[{ label: "", value: "" }]]);
  const [isDataLoaded, setIsDataLoaded] = useState(false);
  const myProp = properties;
  useEffect(() => {
    if (!isEmptyObject(myProp)) {
      console.log("dynamic-table-form", myProp);
      const convertObjectToFields = (obj) => {
        return Object.entries(formData).map(([index, item]) => {
          return Object.entries(obj).map(([label, value]) => {
            return { label, value: item[label] || "" };
          });
        });
      };
      const data = convertObjectToFields(myProp);
      let headers = [];
      let _fieldData = {};

      Object.keys(myProp).forEach((key) => {
        const value = myProp[key];
        console.log("valuez", value);
        const header = value["title"] || key;
        headers.push(header);
        _fieldData[key] = {
          inputProps: value,
          label: key,
          examples: value["examples"] || [],
        };
      });
      setFieldData(_fieldData);
      setHeader(headers);
      setFields(data);
      setIsDataLoaded(true);
    } else {
      setIsDataLoaded(true);
    }
  }, []);

  // console.log("fieldData", fieldData, fields);

  useEffect(() => {
    onFormChangeData(convertToKeyValues(fields));
  }, [fields]);

  const onFormChangeData = (data) => {
    if (!isEmptyObject(data)) {
      // console.log("onFormChangeData", data);
      onFormChange(initialDataKey, data);
    }
  };

  const updateValue = (fields, label, newValue, type) => {
    return fields.map((item) => {
      if (item.label === label) {
        if (type === "number") {
          newValue = Number(newValue);
        }
        return { ...item, value: newValue };
      }
      // console.log("AAAAAAHHHHHHH",item);
      return item;
    });
  };

  const handleChange = (index, e) => {
    const { name, value, type, tagName } = e.target;
    const updatedFields = [...fields];

    // console.log("value on change", value);
    updatedFields[index] = updateValue(updatedFields[index], name, value, type);
    // console.log("updatedFields", updatedFields);
    setFields(updatedFields);
    onFormChangeData(convertToKeyValues(updatedFields));
  };
  // const handleChange = (index, e) => {
  //   const { name, value, type } = e.target;
  //   const updatedFields = [...fields];
  //   const field = updatedFields[index];

  //   console.log("updatedFields", updatedFields);
  //   // const field_inner = field.find((item) => item.label === name);

  //   console.log("e.target.tagName", e.target.tagName);
  //   if (e.target.tagName === "SELECT") {
  //     console.log("SELECT", e.target.options[e.target.selectedIndex].value);
  //     // field_inner.value = e.target.options[e.target.selectedIndex].value;
  //   } else if (e.target.tagName === "TEXTFIELD") {
  //     updatedFields[index] = updateValue(
  //       updatedFields[index],
  //       name,
  //       value,
  //       type
  //     );
  //   }
  //   setFields(updatedFields);
  //   onFormChangeData(convertToKeyValues(updatedFields)); // Call the callback function with the converted form data
  // };

  // const convertToKeyValues = (data) => {
  //     return data.reduce((result, field) => {
  //         const { label, value } = field;
  //         if (label && value) {
  //             result[label] = value;
  //         }
  //         return result;
  //     }, {});
  // };

  const convertToKeyValues = (data) => {
    return data.map((arr) =>
      arr.reduce((acc, obj) => {
        acc[obj.label] = obj.value;
        return acc;
      }, {})
    );
  };
  const handleAddField = (event) => {
    event.preventDefault();
    let newItem = [];
    Object.entries(fieldData).map(([key, item]) => {
      newItem.push({ label: item.label, value: "" });
    });
    const updatedFields = [...fields, newItem];
    setFields(updatedFields);
  };

  const handleRemoveField = (index) => {
    const updatedFields = [...fields];
    updatedFields.splice(index, 1);
    setFields(updatedFields);
  };

  return (
    <Grid
      xs={12}
      style={{
        display: "flex",
        alignItems: "flex-end",
      }}
    >
      <table>
        <thead
        >
          <tr>
            {header.map((val, index) => (
              <td key={index}>{val}</td>
            ))}
          </tr>
        </thead>
        <tbody>
          {isDataLoaded &&
            fields.map((field_object, index) => (
              <React.Fragment key={index}>
                <tr key={index}>
                  {field_object.map((field_inner, index1) => {
                    // console.log(
                    //   "dynamic xyz",
                    //   field_object,
                    //   field_inner,
                    //   index,
                    //   index1
                    // );
                    const getValueOfField = (field) => {
                      if (
                        fieldData[field_inner.label]?.inputProps?.type ===
                          "number" ||
                        fieldData[field_inner.label]?.inputProps?.type ===
                          "integer"
                      ) {
                        console.log("Field", field);
                        return parseInt(field.value) || 0;
                      } else {
                        console.log("Field", field);
                        return field.value;
                      }
                    };
                    const examples = Array.isArray(
                      fieldData[field_inner.label]?.examples
                    )
                      ? fieldData[field_inner.label].examples
                      : null;

                    // console.log("examples", examples);
                    return (
                      <td key={`${index1}_${index}`}>
                        <mat-form-field
                          className="DSA_Wb_custom-form-field DSA_form_nofloatLabel"
                          floatLabel="never"
                          panelClass="DSA_wb-custom-select-panel"
                        >
                          <TextField
                            disabled={disabled}
                            key={`${index}-${index1}`}
                            type={
                              schemaTypeToHtml[
                                fieldData[field_inner.label]?.inputProps?.type
                              ] || "text"
                            }
                            InputProps={{
                              inputProps: {
                                min: fieldData[field_inner.label]?.inputProps
                                  ?.minimum,
                                max: fieldData[field_inner.label]?.inputProps
                                  ?.maximum,
                              },
                            }}
                            name={field_inner.label}
                            size="small"
                            //TODO: add the memory code here.
                            value={getValueOfField(field_inner)}
                            list={`datalist-${initialDataKey}-${index}-${index1}`}
                            autoComplete="off"
                            onChange={(e) => handleChange(index, e)}
                            style={
                              examples.length > 0
                                ? {
                                    width: "100%",
                                    // border: "GOLD 2px SOLID",
                                    marginTop: "-2px",
                                    marginRight: "25px",
                                    textAlign: "center",
                                    fontSize: "small",
                                  }
                                : {
                                    width: "100%",
                                    // border: "GRAY 2px SOLID"
                                  }
                            }
                            select={examples.length > 0 ? true : false}
                            // label={labelValue(label, hideLabel || !label, false)}
                          >
                            {examples.length > 0 &&
                              examples.map((value, index) => {
                                // console.log("xyz", value, index);
                                return (
                                  <MenuItem key={index} value={value}>
                                    {value}
                                  </MenuItem>
                                );
                              })}
                          </TextField>
                        </mat-form-field>
                      </td>
                    );
                  })}
                  <td>
                    <button
                      disabled={disabled}
                      onClick={() => handleRemoveField(index)}
                      className={`MuiButtonBase-root MuiIconButton-root MuiIconButton-colorSecondary ${
                        disabled ? "disabled" : ""
                      }`}
                      type="button"
                      title="Remove"
                      style={{
                        padding: "8px",
                        margin: "2px",
                        justifySelf: "end",
                      }}
                    >
                      <span className="MuiIconButton-label">
                        <svg
                          className="MuiSvgIcon-root MuiSvgIcon-fontSizeSmall"
                          focusable="false"
                          viewBox="0 0 24 24"
                          aria-hidden="true"
                        >
                          <path d="M19 13H5v-2h14v2z"></path>
                        </svg>
                      </span>
                      <span className="MuiTouchRipple-root"></span>
                    </button>
                  </td>
                </tr>
              </React.Fragment>
            ))}
        </tbody>
      </table>
      <button
        disabled={disabled}
        onClick={handleAddField}
        className={`MuiButtonBase-root MuiIconButton-root array-item-add MuiIconButton-colorPrimary ${
          disabled ? "disabled" : ""
        }`}
        type="button"
        title="Add Item"
        style={{
          padding: "8px",
          margin: "5px",
          position: "relative",
        }}
      >
        <span className="MuiIconButton-label">
          <svg
            className="MuiSvgIcon-root"
            focusable="false"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"></path>
          </svg>
        </span>
        <span className="MuiTouchRipple-root"></span>
      </button>
    </Grid>
  );
};

export default DynamicTableForm;
