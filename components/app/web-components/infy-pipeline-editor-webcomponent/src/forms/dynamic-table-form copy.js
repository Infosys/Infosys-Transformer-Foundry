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

  console.log("fieldData", fieldData, fields);

  useEffect(() => {
    onFormChangeData(convertToKeyValues(fields));
  }, [fields]);

  const onFormChangeData = (data) => {
    if (!isEmptyObject(data)) {
      console.log("onFormChangeData", data);
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
      return item;
    });
  };

  const handleChange = (index, e) => {
    const { name, value, type, tagName } = e.target;
    const updatedFields = [...fields];

    console.log("value on change", value);
    updatedFields[index] = updateValue(updatedFields[index], name, value, type);
    console.log("updatedFields", updatedFields);
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
    <Box>
      <Grid item xs={11}>
        <table>
          <thead>
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
                      const examples = Array.isArray(
                        fieldData[field_inner.label]?.examples
                      )
                        ? fieldData[field_inner.label].examples
                        : null;

                      console.log("examples", examples);
                      return (
                        <td key={`${index1}_${index}`}>
                          <mat-form-field
                            className="DSA_Wb_custom-form-field DSA_form_nofloatLabel"
                            floatLabel="never"
                            panelClass="DSA_wb-custom-select-panel"
                          >
                            {true ? (
                              <TextField
                                style={{ width: "100%" }}
                                key={`${index}-${index1}`}
                                type={
                                  schemaTypeToHtml[
                                    fieldData[field_inner.label]?.inputProps
                                      ?.type
                                  ] || "text"
                                }
                                InputProps={{
                                  inputProps: {
                                    min: fieldData[field_inner.label]
                                      ?.inputProps?.minimum,
                                    max: fieldData[field_inner.label]
                                      ?.inputProps?.maximum,
                                  },
                                }}
                                name={field_inner.label}
                                size="small"
                                value={field_inner.value}
                                list={`datalist-${initialDataKey}-${index}-${index1}`}
                                autoComplete="off"
                                onChange={(e) => handleChange(index, e)}
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
                            ) : (
                              // <select
                              //   type="text"
                              //   style={{ border: "BLUE SOLID 2px" }}
                              //   className="DSA_wb-custom-Select"
                              //   onChange={(e) => handleChange(index, e)}
                              // >
                              //   {examples.map((item, index) => (
                              //     <option
                              //       key={index}
                              //       value={item}
                              //       selected={item === field_inner.value}
                              //     >
                              //       {item}
                              //     </option>
                              //   ))}
                              // </select>
                              <>
                                <TextField
                                  // style={{ border: "RED SOLID 2px" }}
                                  key={`${index}-${index1}`}
                                  type={
                                    schemaTypeToHtml[
                                      fieldData[field_inner.label]?.inputProps
                                        ?.type
                                    ] || "text"
                                  }
                                  InputProps={{
                                    inputProps: {
                                      min: fieldData[field_inner.label]
                                        ?.inputProps?.minimum,
                                      max: fieldData[field_inner.label]
                                        ?.inputProps?.maximum,
                                    },
                                  }}
                                  name={field_inner.label}
                                  size="small"
                                  value={field_inner.value}
                                  list={`datalist-${initialDataKey}-${index}-${index1}`}
                                  autoComplete="off"
                                  onChange={(e) => handleChange(index, e)}
                                />
                              </>
                            )}
                            {/* {(fieldData[field.label]?.inputProps?.ui?.widget ==="select")?(<mat-select) */}

                            {/* {!fieldData[field_inner.label]?.inputProps?.ui
                              ?.widget === "select" &&
                              fieldData[field_inner.label]?.inputProps?.type ===
                                "text" && (
                                // <TextField
                                //   key={`${index}-${index1}`}
                                //   type={
                                //     schemaTypeToHtml[
                                //       fieldData[field_inner.label]?.inputProps
                                //         ?.type
                                //     ] || "text"
                                //   }
                                //   InputProps={{
                                //     inputProps: {
                                //       min: fieldData[field_inner.label]
                                //         ?.inputProps?.minimum,
                                //       max: fieldData[field_inner.label]
                                //         ?.inputProps?.maximum,
                                //     },
                                //   }}
                                //   name={field_inner.label}
                                //   size="small"
                                //   value={field_inner.value}
                                //   list={`datalist-${initialDataKey}-${index}-${index1}`}
                                //   autoComplete="off"
                                //   onChange={(e) => handleChange(index, e)}
                                // />
                              )} */}

                            {/* {examples && (
                              <datalist
                                id={`datalist-${field_inner.label}-${index}-${index1}`}
                              >
                                {fieldData[field_inner.label]["examples"].map(
                                  (example) => {
                                    console.log(
                                      `datalist-${field_inner.label}-${index}-${index1}`,
                                      example
                                    );
                                    return (
                                      <option key={example} value={example} />
                                    );
                                  }
                                )}
                              </datalist>
                            )} */}
                          </mat-form-field>
                        </td>
                      );
                    })}
                    <td>
                      <button
                        onClick={() => handleRemoveField(index)}
                        className="MuiButtonBase-root MuiIconButton-root MuiIconButton-colorSecondary MuiIconButton-sizeSmall"
                        type="button"
                        title="Remove"
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
      </Grid>
      <Grid item xs={1}>
        <button
          onClick={handleAddField}
          className="MuiButtonBase-root MuiIconButton-root array-item-add MuiIconButton-colorPrimary"
          type="button"
          title="Add Item"
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
    </Box>
  );
};

export default DynamicTableForm;
