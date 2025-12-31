/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import React from "react";
import Grid from "@material-ui/core/Grid";
import TextField from "@material-ui/core/TextField";
import { ADDITIONAL_PROPERTY_FLAG, TranslatableString } from "@rjsf/utils";

/** The `WrapIfAdditional` component is used by the `FieldTemplate` to rename, or remove properties that are
 * part of an `additionalProperties` part of a schema.
 *
 * @param props - The `WrapIfAdditionalProps` for this component
 */
export default function WrapIfAdditionalTemplate(props) {
  const {
    children,
    classNames,
    style,
    disabled,
    id,
    label,
    onDropPropertyClick,
    onKeyChange,
    readonly,
    required,
    schema,
    uiSchema,
    registry,
  } = props;
  const { templates, translateString } = registry;
  // Button templates are not overridden in the uiSchema
  const { RemoveButton } = templates.ButtonTemplates;
  const keyLabel = translateString(TranslatableString.KeyLabel, [label]);
  const additional = ADDITIONAL_PROPERTY_FLAG in schema;
  const btnStyle = {
    flex: 1,
    paddingLeft: 6,
    paddingRight: 6,
    marginBottom: "-10px",
    marginRight: "-10px",
    fontWeight: "bold",
  };

  if (!additional) {
    return (
      <div className={classNames} style={style}>
        {children}
      </div>
    );
  } else {
  }

  const handleBlur = ({ target }) => onKeyChange(target.value);
  const tempStyle = {
    ...style,
    ...{
      // width:'95%',
      // border: "BLACK 2px DASHED",
    },
  };

  return (
    <Grid
      container
      key={`${id}-key`}
      alignItems="center"
      spacing={0.2}
      className={classNames}
      style={tempStyle}
      direction="row"
      // xs={10}
      justifyContent="flex-start"
    >
      <Grid item xs={5}>
        <TextField
          fullWidth={true}
          required={required}
          // label={keyLabel}
          defaultValue={label && label.includes("newKey") < 1 ? label : ""}
          disabled={disabled || readonly}
          id={`${id}-key`}
          name={`${id}-key`}
          onBlur={!readonly ? handleBlur : undefined}
          type="text"
        />
      </Grid>
      <Grid item xs={5}>
        {children}
      </Grid>
      <Grid
        item={true}
        style={{
          marginRight: " 60px",
          marginTop: "-6px",
        }}
      >
        <RemoveButton
          iconType="default"
          style={btnStyle}
          disabled={disabled || readonly}
          onClick={onDropPropertyClick(label)}
          uiSchema={uiSchema}
          registry={registry}
        />
      </Grid>
    </Grid>
  );
}
