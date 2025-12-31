/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import React, { useState, useEffect } from "react";

function isEmptyObject(obj) {
    return JSON.stringify(obj) === "{}";
}
const DynamicKeyValueForm = ({
    properties,
    formData,
    initialDataKey,
    onFormChange,
    variables
}) => {
    const [fields, setFields] = useState([{ label: "", value: "" }]);
    
    useEffect(() => {
        if (!isEmptyObject(properties)) {
            const convertObjectToFields = (obj) => {
                return Object.entries(obj).map(([label, value]) => {
                    return { label, value: formData[label] || "" };
                });
            };
            const data = convertObjectToFields(properties);
            setFields(data);
        }
    }, []);

    useEffect(() => {
        onFormChangeData(convertToKeyValues(fields));
    }, [fields]);

    const onFormChangeData = (data) => {
        if (!isEmptyObject(data)) {
            onFormChange(initialDataKey, data);
        }
    };

    const handleChange = (index, e) => {
        const { name, value } = e.target;
        const updatedFields = [...fields];
        updatedFields[index] = { ...updatedFields[index], [name]: value };
        setFields(updatedFields);
        onFormChangeData(convertToKeyValues(updatedFields)); // Call the callback function with the converted form data
    };

    const convertToKeyValues = (data) => {
        return data.reduce((result, field) => {
            const { label, value } = field;
            if (label && value) {
                result[label] = value;
            }
            return result;
        }, {});
    };

    const handleAddField = (event) => {
        
        event.preventDefault();
        const updatedFields = [...fields, { label: "", value: "" }];
        setFields(updatedFields);
    };

    const handleRemoveField = (index) => {
        const updatedFields = [...fields];
        updatedFields.splice(index, 1);
        setFields(updatedFields);
    };

    return (
        <>
            <table>
                <thead>
                    <tr>
                        <td>Key</td>
                        <td>Value</td>
                        <td>
                            <button  onClick={handleAddField} >
                                Add
                            </button>
                            {/* <AddCircleOutlineIcon onClick={handleAddField} /> */}
                        </td>
                    </tr>
                </thead>
                <tbody>
                    {fields.map((field, index) => (
                        <React.Fragment key={index}>
                            <tr>
                                <td>
                                    <mat-form-field
                                        className="DSA_Wb_custom-form-field DSA_form_nofloatLabel"
                                        floatLabel="never"
                                        panelClass="DSA_wb-custom-select-panel">
                                        <input type="text" name="label"
                                            size="sm" value={field.label}
                                            list={`datalist-label-${initialDataKey}-${index}`}
                                            autoComplete="off" onChange={(e) => handleChange(index, e)} disabled={field.label || false} />
                                    </mat-form-field>
                                </td>
                                <td>
                                    <mat-form-field
                                        className="DSA_Wb_custom-form-field DSA_form_nofloatLabel"
                                        floatLabel="never"
                                        panelClass="DSA_wb-custom-select-panel">
                                        <input
                                            type="text" name="value"
                                            size="sm" value={field.value} list={`datalist-${initialDataKey}-${index}`}
                                            autoComplete="off" onChange={(e) => handleChange(index, e)} />

                                        {/* code that show suggestions */}
                                        {variables &&
                                            Object.keys(variables).length > 0 &&
                                            field.value === "" && (
                                                <datalist id={`datalist-${initialDataKey}-${index}`}>
                                                    {Object.keys(variables).map((label) => {
                                                        return (
                                                            <option
                                                                key={label}
                                                                value={`{{pipeline.variables.` + label + "}}"}
                                                            />
                                                        );
                                                    })}
                                                </datalist>
                                            )}
                                    </mat-form-field>
                                </td>
                                <td>
                                    {!field.label &&
                                        <button  onClick={() => handleRemoveField(index)} >
                                            Remove
                                        </button>
                                        // <DeleteForeverOutlinedIcon style={{ float: "right" }} onClick={() => handleRemoveField(index)} />
                                    }
                                </td>
                            </tr>
                        </React.Fragment>
                    ))}
                </tbody>
            </table >
        </>
    );
};

export default DynamicKeyValueForm;
