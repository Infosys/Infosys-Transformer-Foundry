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
const DynamicTextValueForm = ({
    properties,
    formData,
    initialDataKey,
    onFormChange,
    variables
}) => {
    const [fields, setFields] = useState("");
    
    useEffect(() => {
        if (!isEmptyObject(formData)) {
            setFields(formData);
        }
    }, []);

    useEffect(() => {
        onFormChangeData(fields);
    }, [fields]);

    const onFormChangeData = (data) => {
        if (!isEmptyObject(data)) {
            onFormChange(initialDataKey, data);
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFields(value);
        onFormChangeData(fields); // Call the callback function with the converted form data
    };

    return (
        <>
            <input type="text" name={initialDataKey}
                value={fields} onChange={(e) => handleChange(e)} />
        </>
    );
};

export default DynamicTextValueForm;
