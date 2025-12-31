/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import React, { createContext, useState, useEffect } from "react";
const FormDataContext = createContext();

const FormDataProvider = ({ children }) => {
  const [formData, setFormData] = useState({});

  const setNewFormData = (data) => {
    setFormData(data);
  };

  const addFormData = (key, value) => {
    console.log("before Addfome", formData);
    const newData = { ...formData, [key]: value };
    setFormData(newData);
    console.log("after Addfome", formData);
  };

  const clearFormData = (node) => {
    const updatedFormData = { ...formData };
    if (node.id in updatedFormData) {
      delete updatedFormData[node.id];
    } else if (node.data.label in updatedFormData) {
      delete updatedFormData[node.data.label];
    }
    setFormData(updatedFormData);
  };

  return (
    <FormDataContext.Provider
      value={{
        formData,
        addFormData,
        clearFormData,
        setNewFormData,
      }}
    >
      {children}
    </FormDataContext.Provider>
  );
};

export { FormDataContext, FormDataProvider };
