/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import React from "react";
import DynamicKeyValueForm from "../forms/dynamic-key-value-form";
const CustomObjectToTableField = (props) => {
    const { name, schema, formData = {}, onChange } = props;
    const { title, properties } = schema;
    const handleValueChange = (key, value) => {
        onChange({ ...formData, ...value });
    };
    return (
        <>
            <header>{title || name}</header>
            &nbsp;
            <DynamicKeyValueForm properties={properties} formData={formData} initialDataKey={name}
                onFormChange={handleValueChange} variables={{}} />
        </>
    );
}

export default CustomObjectToTableField;