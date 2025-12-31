/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import React from "react";
import TextField from "@material-ui/core/TextField";
import {
  ariaDescribedByIds,
  examplesId,
  getInputProps,
  labelValue,
} from "@rjsf/utils";
import { Box, Grid } from "@material-ui/core";

const TYPES_THAT_SHRINK_LABEL = ["date", "datetime-local", "file", "time"];

/** The `BaseInputTemplate` is the template to use to render the basic `<input>` component for the `core` theme.
 * It is used as the template for rendering many of the <input> based widgets that differ by `type` and callbacks only.
 * It can be customized/overridden for other themes or individual implementations as needed.
 *
 * @param props - The `WidgetProps` for this template
 */
export default function BaseInputTemplate(props) {
  const {
    id,
    name, // remove this from textFieldProps
    placeholder,
    required,
    readonly,
    disabled,
    type,
    label,
    hideLabel,
    value,
    onChange,
    onChangeOverride,
    onBlur,
    onFocus,
    autofocus,
    options,
    schema,
    uiSchema,
    rawErrors = [],
    formContext,
    registry,
    InputLabelProps,
    ...textFieldProps
  } = props;
  const inputProps = getInputProps(schema, type, options);
  // Now we need to pull out the step, min, max into an inner `inputProps` for material-ui
  const { step, min, max, ...rest } = inputProps;
  const otherProps = {
    inputProps: {
      step,
      min,
      max,
      ...(schema.examples ? { list: examplesId(id) } : undefined),
    },
    ...rest,
  };
  const _onChange = ({ target: { value } }) => onChange(value);
  // onChange(value === "" ? options.emptyValue : value)
  const _onBlur = ({ target: { value } }) => onBlur(id, value);
  const _onFocus = ({ target: { value } }) => onFocus(id, value);
  const DisplayInputLabelProps = TYPES_THAT_SHRINK_LABEL.includes(type)
    ? {
        ...InputLabelProps,
        shrink: true,
      }
    : InputLabelProps;

  const labelVal = labelValue(label || undefined, hideLabel, false);

  return (
    <Grid
      xs={11}
      container
      style={{
        marginLeft: "5px",
        width: "90%",
        // border: "MAGENTA 2px SOLID",
        alignItems: "flex-end",
      }}
    >
      {labelVal && (
        <Grid xs={3} item={true}>
          <Box
            pt={1}
            style={
              {
                // border: "GOLD 2px SOLID",
              }
            }
          >
            {labelVal}
            {required && (
              <sup>
                <span
                  className="required-cls"
                  style={{ fontSize: "small", color: "red" }}
                >
                  *
                </span>
              </sup>
            )}
          </Box>
        </Grid>
      )}
      <Grid xs item={true}>
        <TextField
          style={{
            width: "100%",
            // border: "RED 2px SOLID"
          }}
          id={id}
          name={id}
          placeholder={placeholder}
          // label={labelValue(label || undefined, hideLabel, false)}
          autoFocus={autofocus}
          required={required}
          disabled={disabled || readonly}
          {...otherProps}
          value={(value || value === 0) && value != "New Value" ? value : ""}
          error={rawErrors.length > 0}
          onChange={onChangeOverride || _onChange}
          onBlur={_onBlur}
          onFocus={_onFocus}
          InputLabelProps={DisplayInputLabelProps}
          {...textFieldProps}
          aria-describedby={ariaDescribedByIds(id, !!schema.examples)}
        />
        {schema.examples && (
          <datalist id={examplesId(id)}>
            {schema.examples.map((example, i) => (
              <option key={i} value={example} />
            ))}
          </datalist>
        )}
      </Grid>
    </Grid>
  );
}
