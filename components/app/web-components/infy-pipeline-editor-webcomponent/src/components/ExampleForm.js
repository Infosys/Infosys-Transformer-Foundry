/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import React from "react";
import Form from "@rjsf/core";
import validator from "@rjsf/validator-ajv8";


const schema = {
  type: "object",
  properties: {
    fruit: {
      type: "string",
      enum: ["Apple", "Banana", "Orange", "Mango", "Grapes"],
    },
  },
};

const widgets = {
  SelectWidget: (props) => {
    const { id, options, value, onChange } = props;
    return (
      <select
        id={id}
        value={value}
        onChange={(event) => onChange(event.target.value)}
      >
        <option value="">Select an option</option>
        {options.enumOptions.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    );
  },
};

const ExampleForm = () => {
  return <Form schema={schema} widgets={widgets} validator={validator}/>;
};

export default ExampleForm;
