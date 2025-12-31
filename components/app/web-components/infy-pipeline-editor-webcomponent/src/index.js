/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import React from "react";
import { createRoot } from "react-dom/client";
import { FormDataProvider } from "./stores/form-datastore";
import { ToastContainer } from "react-toastify";
import ReactFlowWrapper from "./components/ReactFlowWrapper";

import "react-toastify/dist/ReactToastify.css";
import "./style.css";

class CustomReactComponent extends HTMLElement {
  constructor() {
    super();
    this.handleReceiveDataFromParent =
      this.handleReceiveDataFromParent.bind(this);
  }

  connectedCallback() {
    // Add event listener for custom event before rendering the component
    console.log("connectedCallback");
    window.addEventListener(
      "receiveDataFromParent",
      this.handleReceiveDataFromParent
    );
  }

  disconnectedCallback() {
    console.log("disconnectedCallback");
    // Remove event listener when the component is removed from the DOM
    window.removeEventListener(
      "receiveDataFromParent",
      this.handleReceiveDataFromParent
    );
  }

  handleReceiveDataFromParent(event) {
    // Handle the data received from Angular parent
    console.log("handleReceiveDataFromParent", event.detail);
    const { nodeData, pipeline, nodeSetting, isReadOnlyMode } = event.detail;

    // Render the component with the received data
    this.renderComponent(nodeData, pipeline, nodeSetting, isReadOnlyMode);
  }

  renderComponent(nodeData, pipeline, nodeSetting, isReadOnlyMode) {
    createRoot(this).render(
      <FormDataProvider>
        <ReactFlowWrapper
          nodeData={nodeData}
          pipeline={pipeline}
          nodeSetting={nodeSetting}
          isReadOnlyMode={isReadOnlyMode}
        />
        <ToastContainer autoClose={5000} />
      </FormDataProvider>
    );
  }
}

customElements.define("pipeline-editor", CustomReactComponent);
