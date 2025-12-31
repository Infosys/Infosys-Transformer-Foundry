/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import React from "react";
import DynamicTextValueForm from "../forms/dynamic-text-value-form";
import { getDefaultRegistry } from '@rjsf/core';
const { templates: { BaseInputTemplate, ArrayFieldItemTemplate } } = getDefaultRegistry();
const CustomTextboxField = (props) => {
    const { name, schema, formData = {},disabled, readonly, required, multiple, onChange, value, options, registry } = props;
    const { title, properties = "" } = schema;
    const handleValueChange = (key, value) => {
        onChange({ ...formData, ...value });
    };
    // const BaseInputTemplate = getTemplate(
    //     "BaseInputTemplate",options, registry
    //   )
    return (
        <>
            <header>{title || name}</header>
            &nbsp;
            <DynamicTextValueForm properties={properties} formData={formData} initialDataKey={name}
                onFormChange={handleValueChange} variables={{}} />
            {/* <BaseInputTemplate
                {...props}
                disabled={disabled || readonly}
                type='text'
                required={value ? false : required} 
                value=''
            /> */}
        </>
    );
}

export default CustomTextboxField;