/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import React from "react";
import MenuItem from "@material-ui/core/MenuItem"
import TextField from "@material-ui/core/TextField"
import {
    ariaDescribedByIds,
    enumOptionsIndexForValue,
    enumOptionsValueForIndex,
    labelValue
} from "@rjsf/utils"
import { Box, Grid } from "@material-ui/core";
/** The `SelectWidget` is a widget for rendering dropdowns.
 *  It is typically used with string properties constrained with enum options.
 *
 * @param props - The `WidgetProps` for this component
 */
export default function SelectWidget({
    schema,
    id,

    // remove this from textFieldProps
    name,

    options,
    label,
    hideLabel,
    required,
    disabled,
    readonly,
    placeholder,
    value,
    multiple,
    autofocus,
    onChange,
    onBlur,
    onFocus,
    rawErrors = [],
    registry,
    uiSchema,
    hideError,
    formContext,
    ...textFieldProps
}) {
    const { enumOptions, enumDisabled, emptyValue: optEmptyVal } = options

    multiple = typeof multiple === "undefined" ? false : !!multiple

    const emptyValue = multiple ? [] : ""
    const isEmpty =
        typeof value === "undefined" ||
        (multiple && value.length < 1) ||
        (!multiple && value === emptyValue)

    const _onChange = ({ target: { value } }) =>
        onChange(enumOptionsValueForIndex(value, enumOptions, optEmptyVal))
    const _onBlur = ({ target: { value } }) =>
        onBlur(id, enumOptionsValueForIndex(value, enumOptions, optEmptyVal))
    const _onFocus = ({ target: { value } }) =>
        onFocus(id, enumOptionsValueForIndex(value, enumOptions, optEmptyVal))
    const selectedIndexes = enumOptionsIndexForValue(value, enumOptions, multiple)
    const labelVal = labelValue(label || undefined, hideLabel, false)
    return (
        <>
            <Grid container>
                {labelVal && <Grid xs={3} item={true}>
                    <Box pt={0.5}>
                        {labelVal}{required && <sup><span className="required-cls" style={{ fontSize: "small", color: "red" }}>*</span></sup>}
                    </Box>
                </Grid>}
                <Grid xs item={true}>
                    <TextField
                        style={{ width: "100%" }}
                        id={id}
                        name={id}
                        // label={labelValue(label, hideLabel || !label, false)}
                        value={isEmpty ? emptyValue : selectedIndexes}
                        required={required}
                        disabled={disabled || readonly}
                        autoFocus={autofocus}
                        placeholder={placeholder}
                        error={rawErrors.length > 0}
                        onChange={_onChange}
                        onBlur={_onBlur}
                        onFocus={_onFocus}
                        {...textFieldProps}
                        // Apply this and the following props after the potential overrides defined in textFieldProps
                        select
                        InputLabelProps={{
                            ...textFieldProps.InputLabelProps,
                            shrink: !isEmpty
                        }}
                        SelectProps={{
                            ...textFieldProps.SelectProps,
                            multiple
                        }}
                        aria-describedby={ariaDescribedByIds(id)}
                    >
                        {Array.isArray(enumOptions) &&
                            enumOptions.map(({ value, label }, i) => {
                                const disabled =
                                    Array.isArray(enumDisabled) && enumDisabled.indexOf(value) !== -1
                                return (
                                    <MenuItem key={i} value={String(i)} disabled={disabled}>
                                        {label}
                                    </MenuItem>
                                )
                            })}
                    </TextField>
                </Grid>
            </Grid>
        </>
    )
}
