/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import React from "react";
import { Grid, Box } from "@material-ui/core";
import {
  canExpand,
  descriptionId,
  getTemplate,
  getUiOptions,
  titleId,
} from "@rjsf/utils";

/** The `ObjectFieldTemplate` is the template to use to render all the inner properties of an object along with the
 * title and description if available. If the object is expandable, then an `AddButton` is also rendered after all
 * the properties.
 *
 * @param props - The `ObjectFieldTemplateProps` for this component
 */
export default function ObjectFieldTemplate(props) {
  const {
    description,
    title,
    properties,
    required,
    disabled,
    readonly,
    uiSchema,
    idSchema,
    schema,
    formData,
    onAddClick,
    registry,
  } = props;
  const uiOptions = getUiOptions(uiSchema);
  const TitleFieldTemplate = getTemplate(
    "TitleFieldTemplate",
    registry,
    uiOptions
  );
  const DescriptionFieldTemplate = getTemplate(
    "DescriptionFieldTemplate",
    registry,
    uiOptions
  );
  // Button templates are not overridden in the uiSchema
  const {
    ButtonTemplates: { AddButton },
  } = registry.templates;
  return (
    <Box
      pt={0.5}
      pl={0.5}
      pr={0.5}
      style={
        {
          // width: "95%",
          // border: "GREEN 2px SOLID",
          // borderRight: "RED 2px SOLID",
        }
      }
    >
      {title && (
        <TitleFieldTemplate
          id={titleId(idSchema)}
          title={title}
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
      <Grid
        // xs={12}
        container={true}
        style={{
          paddingTop: "6px",
          // width: "50%",
          // border: "BLACK 2px DASHED",
        }}
        // style={{ width: "100%", border: "RED 2px DOTTED" }}
      >
        {properties.map((element, index) =>
          // Remove the <Grid> if the inner element is hidden as the <Grid>
          // itself would otherwise still take up space.
          element.hidden ? (
            element.content
          ) : (
            <Grid
              item={true}
              xs={12}
              key={index}
              // style={{
              //   paddingTop: "6px",
              //   width: "100%",
              //   border: "BLACK 1px DASHED",
              // }}
            >
              
              <div className="kvDiv">{element.content}</div>
            </Grid>
          )
        )}
        {canExpand(schema, uiSchema, formData) && (
          <Grid
            container
            item
            style={
              properties.length > 0
                ? { marginTop: "-30px" }
                : { margin: "-5px" }
            }
            // xs={properties.length === 0 ? 12 : 1}
            justifyContent="flex-end"
            alignItems="flex-start"
          >
            <AddButton
              className="object-property-expand"
              onClick={onAddClick(schema)}
              disabled={disabled || readonly}
              uiSchema={uiSchema}
              registry={registry}
              style={properties.length === 0 ? {} : { position: "relative" }}
            />
          </Grid>
        )}
      </Grid>
    </Box>
  );
}
