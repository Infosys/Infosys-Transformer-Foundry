/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import React from "react";
import DynamicTableForm from "../forms/dynamic-table-form";
import { Grid, Box } from "@material-ui/core";
import resolveSchema from "../common/utils";
import TitleFieldTemplate from "../templates/TitleFieldTemplate";
import {
  canExpand,
  descriptionId,
  getTemplate,
  getUiOptions,
  titleId,
} from "@rjsf/utils";
const CustomArrayToTableField = (props) => {
  console.log("CustomArrayToTableField", props);
  const {
    name,
    schema,
    formData = {},
    onChange,
    registry,
    disabled,
    readonly,
    uiSchema,
    idSchema,
  } = props;
  const { title, required } = schema;
  const { description } = schema.items;
  const properties = resolveSchema(registry.rootSchema, schema).items
    .properties;
  const uiOptions = getUiOptions(uiSchema);
  const DescriptionFieldTemplate = getTemplate(
    "DescriptionFieldTemplate",
    registry,
    uiOptions
  );
  const handleValueChange = (key, value) => {
    onChange(value);
  };
  return (
    <Box pl={1.5} pt={0.5}>
      {title && (
        <TitleFieldTemplate
          id={titleId(idSchema)}
          title={title || name}
          required={required}
          schema={schema}
          uiSchema={uiSchema}
          registry={registry}
        />
      )}
      {description && (
        <DescriptionFieldTemplate
          id={descriptionId(idSchema)}
          description={description}
          schema={schema}
          uiSchema={uiSchema}
          registry={registry}
        />
      )}
      <Box
        pt={1}
        style={{
          // border: "SILVER 2px SOLID",
        }}
      >
        <DynamicTableForm
          properties={properties}
          formData={formData}
          initialDataKey={name}
          onFormChange={handleValueChange}
          pprops={props}
          disabled={disabled || readonly}
        />
      </Box>
    </Box>
  );
};

export default CustomArrayToTableField;
