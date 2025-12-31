/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import React, { useState } from "react";
import Box from "@material-ui/core/Box";
import Grid from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";
import { getTemplate, getUiOptions } from "@rjsf/utils";

import ArrayItemTableTemplate from "./ArrayItemTableTemplate";
/** The `ArrayFieldTemplate` component is the template used to render all items in an array.
 *
 * @param props - The `ArrayFieldTemplateItemType` props for the component
 */
export default function ArrayFieldTemplate(props) {
  const {
    canAdd,
    disabled,
    idSchema,
    uiSchema,
    items,
    onAddClick,
    readonly,
    registry,
    required,
    schema,
    title,
  } = props;

  const uiOptions = getUiOptions(uiSchema);
  const ArrayFieldDescriptionTemplate = getTemplate(
    "ArrayFieldDescriptionTemplate",
    registry,
    uiOptions
  );
  const ArrayFieldItemTemplate = getTemplate(
    "ArrayFieldItemTemplate",
    registry,
    uiOptions
  );
  const ArrayFieldTitleTemplate = getTemplate(
    "ArrayFieldTitleTemplate",
    registry,
    uiOptions
  );

  const CustomArrayTableTemplate = (key, itemProps) => {
    const tableHeader = [];
    Object.keys(itemProps.schema.properties).forEach((key) => {
      const value = itemProps.schema.properties[key];
      tableHeader.push(value["title"] || key);
    });
    return (
      <Box pl={2.5}>
        <table>
          {setHeader && (
            <thead>
              <tr>
                {tableHeader.map((val, index) => (
                  <td key={index}>{val}</td>
                ))}
                {(setHeader = false)}
                <td></td>
              </tr>
            </thead>
          )}
          <ArrayItemTableTemplate key={key} {...itemProps} />
        </table>
      </Box>
    );
  };
  // Button templates are not overridden in the uiSchema
  let setHeader = true;
  const {
    ButtonTemplates: { AddButton },
  } = registry.templates;
  return (
    <>
      <Box
        pl={1}
        pt={0.5}
        style={{
          marginRight: "50px",
          width: "97%",
          //  border: "PINK 2px SOLID"
        }}
      >
        {/* <Box pt={0.5}> */}
        <ArrayFieldTitleTemplate
          idSchema={idSchema}
          title={uiOptions.title || title}
          schema={schema}
          uiSchema={uiSchema}
          required={required}
          registry={registry}
        />
        <ArrayFieldDescriptionTemplate
          idSchema={idSchema}
          description={uiOptions.description || schema.description}
          schema={schema}
          uiSchema={uiSchema}
          registry={registry}
        />
        <Grid container={true} key={`array-item-list-${idSchema.$id}`}>
          {items &&
            items.map(({ key, ...itemProps }) => {
              if (itemProps.schema.type === "string") {
                return (
                  <Grid container item xs={11} key={key}>
                    <ArrayFieldItemTemplate {...itemProps} />
                  </Grid>
                );
              } else if (itemProps.schema.type === "object") {
                return (
                  <Grid container item xs={11}>
                    <Box pt={0.5}>
                      <ArrayFieldItemTemplate key={key} {...itemProps} />
                    </Box>
                  </Grid>
                );
                // return (CustomArrayTableTemplate(key, itemProps))
              }
            })}
          {canAdd && (
            <Grid
              container
              item
              // xs={items.length === 0 ? 12 : 1}
              style={
                items.length > 0
                  ? { marginTop: "-65px" }
                  : { marginTop: "-5px" }
              }
              justifyContent="flex-end"
              alignItems="flex-start"
              // style={items.length === 0 ? { position: "relative" } : {}}
            >
              {/* <Grid xs item={true} style={{ marginLeft: "5px" }}> */}
              <AddButton
                className="array-item-add"
                onClick={onAddClick}
                disabled={disabled || readonly}
                uiSchema={uiSchema}
                registry={registry}
              />
              {/* </Grid> */}
            </Grid>
          )}
        </Grid>
      </Box>
    </>
  );
}
