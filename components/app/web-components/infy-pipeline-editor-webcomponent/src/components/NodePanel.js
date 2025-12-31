/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import React, { useState, useEffect } from "react";
// TESTING DATA
const nodepanel = [
  {
    group: "Generic",
    nodes: [
      {
        label: "Node",
        propertyNamedRef: "custom-1",
      },
    ],
  },
  {
    group: "Info extraction",
    nodes: [
      {
        label: "Key Value Extraction",
        propertyNamedRef: "custom-1",
      },
      {
        label: "Table Detection",
        propertyNamedRef: "custom-1",
      },
      {
        label: "Table Extraction",
        propertyNamedRef: "custom-1",
      },
    ],
  },
  {
    group: "HayStack",
    nodes: [
      {
        label: "Document Classifier",
        propertyNamedRef: "custom-1",
      },
      {
        label: "Pre-Processor",
        propertyNamedRef: "custom-1",
      },
    ],
  },
];

const NodePanel = (props) => {
  const [panelData, setpanelData] = useState([]);

  const [openPanel, setopenPanel] = useState({});

  const togglePanel = (panel) => {
    setopenPanel((prevState) => ({ ...prevState, [panel]: !prevState[panel] }));
  };

  useEffect(() => {
    // setpanelData(nodepanel);
    setpanelData(props.nodePanelData.panelData);
  });

  const onDragStart = (event, name, nodeAttribute) => {
    // const onDragStart = (event, name, propertyNamedRef, nodeAttribute) => {
    event.dataTransfer.setData(
      "application/pipeline-editor",
      JSON.stringify({
        name: name,
        // propertyNamedRef: propertyNamedRef, now this will be inside nodeAttribute
        nodeAttribute: nodeAttribute,
      })
    );
    event.dataTransfer.effectAllowed = "move";
  };

  return (
    <aside>
      <div className="side-panel">
        {/*
        <div
          className="dndnode"
          onDragStart={(event) => onDragStart(event, "Generic Node")}
          draggable
        >
          Generic Node
        </div> */}
        {panelData &&
          Object.entries(panelData).map(([panelKey, panel]) => (
            <div key={panelKey} className="panel">
              <div
                className="panel-header"
                onClick={() => togglePanel(panelKey)}
              >
                {panel.group}
                <span className="arrow ">
                  {openPanel[panelKey] ? (
                    <span class="material-symbols-outlined">unfold_less</span>
                  ) : (
                    <span class="material-symbols-outlined">
                      expand_more
                    </span>
                  )}
                </span>
              </div>
              {/* <hr /> */}
              {openPanel[panelKey] && (
                <div
                  className="panel-content"
                  onClick={() => console.log(panel)}
                >
                  {panel.nodes.map((node) => {
                    if (node.enabled)
                      return (
                        <div
                          key={node.label}
                          className="dndnode"
                          style={{
                            backgroundColor:
                              node.nodeAttribute?.backgroundColor,
                          }}
                          onDragStart={
                            (event) =>
                              onDragStart(
                                event,
                                node.label,
                                // node.propertyNamedRef,
                                node.nodeAttribute
                              ) //passing node data to onDrag() to initiate the props form.
                          }
                          draggable
                        >
                          {node.label}
                        </div>
                      );
                  })}
                </div>
              )}
            </div>
          ))}
      </div>
    </aside>
  );
};

export default NodePanel;
