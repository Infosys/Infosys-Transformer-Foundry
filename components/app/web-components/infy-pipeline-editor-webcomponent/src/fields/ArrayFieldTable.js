/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import React from 'react';

const ArrayFieldTable = (props) => {
    console.log("ArrayFieldTable", JSON.stringify(Object.keys(props)))
    console.log("ArrayFieldTable", props)
  const { idSchema, schema, uiSchema, formData, onAddClick, onDropIndexClick, onItemChange, registry } = props;
  const items = formData || [];

  const getItemSchema = () => {
    if (schema.items && schema.items.$ref) {
      const ref = schema.items.$ref;
      const definitionId = ref.split('/').pop();
      const definition = registry.rootSchema.definitions[definitionId];
      return definition;
    }
    return schema.items;
  };

  const itemSchema = getItemSchema();

  const handleItemChange = (index, key, value) => {
    const updatedItem = { ...items[index], [key]: value };
    const updatedItems = [...items];
    updatedItems[index] = updatedItem;
    onItemChange(updatedItems);
  };

  const handleAddClick = () => {
    const newItems = [...items, {}];
    onAddClick(newItems);
  };

  return (
    <table>
      <thead>
        <tr>
          {itemSchema &&
            itemSchema.properties &&
            Object.keys(itemSchema.properties).map((key) => (
              <th key={key}>{itemSchema.properties[key].title || key}</th>
            ))}
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {items.map((item, index) => (
          <tr key={index}>
            {itemSchema &&
              itemSchema.properties &&
              Object.keys(itemSchema.properties).map((key) => (
                <td key={key}>
                  <input
                    type="text"
                    value={item[key] || ''}
                    onChange={(e) => handleItemChange(index, key, e.target.value)}
                  />
                </td>
              ))}
            <td>
              <button type="button" onClick={() => onDropIndexClick(index)}>
                Remove
              </button>
            </td>
          </tr>
        ))}
      </tbody>
      <tfoot>
        <tr>
          <td colSpan={Object.keys(itemSchema.properties).length + 1}>
            <button type="button" onClick={handleAddClick}>
              Add
            </button>
          </td>
        </tr>
      </tfoot>
    </table>
  );
};

export default ArrayFieldTable;
