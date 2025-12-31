/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import React from "react";
import { Box, Typography, Divider } from "@material-ui/core";
export default function TitleFieldTemplate(props) {
  const { id, required, title } = props;
  console.log("TitleFieldTemplate", title, props);
  // <Box id={id}>
  //   <Typography>{title}</Typography>
  // </Box>
  return (
    <>
      <Box id={id}>
        <header id={id}>
          {title}
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
        </header>
        <Divider light={true} />
      </Box>
    </>
  );
}
