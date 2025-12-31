/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import React, { useState, useEffect } from "react";


function isEmptyObject(obj) {
    return obj && JSON.stringify(obj) === "{}";
}
const DynamicArrayValueForm = ({
    properties,
    formData,
    initialDataKey,
    onFormChange,
    variables
}) => {
    const [fields, setFields] = useState([{ label: "", value: "" }]);
    useEffect(() => {
        const arrayVal = [...properties,...formData]
        if (arrayVal && arrayVal.length>0) {
            const convertArrayToFields = (obj) => {
                return Object.entries(obj).map(([label, value]) => {
                    return { value: value };
                });
            };
            const data = convertArrayToFields(arrayVal);
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
        return data.map(item => item.value)
    };

    const handleAddField = (event) => {
        
        event.preventDefault();
        const updatedFields = [...fields, { value: "" }];
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
                        <td>Value</td>
                        <td>
                            <button onClick={handleAddField} >
                                Add
                            </button>
                        </td>
                    </tr>
                </thead>
                <tbody>
                    {fields.map((field, index) => (
                        <React.Fragment key={index}>
                            <tr>
                                <td>
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

                                </td>
                                <td>
                                    <button onClick={() => handleRemoveField(index)} >
                                        Remove
                                    </button>
                                </td>
                            </tr>
                        </React.Fragment>
                    ))}
                </tbody>
            </table >
        </>
    );
};

export default DynamicArrayValueForm;
