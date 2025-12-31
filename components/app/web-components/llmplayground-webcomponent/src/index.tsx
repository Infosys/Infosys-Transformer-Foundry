/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import React, { useState, useEffect } from "react";
import { createRoot } from "react-dom/client";
import App from "./app";

import PromptLibrary from "./pages/promtlibrary";

class ReactApp extends HTMLElement {
  constructor() {
    super();
    const container = this;
    const root = createRoot(container);
    console.log('[React] ReactApp custom element initialized');
    root.render(<AppWrapper />);
  }
}

const AppWrapper = () => {
  const [userID, setUserID] = useState('');

  useEffect(() => {
    const handleUserIdEvent = (event: Event) => {
      const customEvent = event as CustomEvent;
      console.log('Received userId:', customEvent.detail);
      setUserID(customEvent.detail);
      console.log('Updated userID state:', customEvent.detail); // Log state update
    };

    window.addEventListener('sendUserId', handleUserIdEvent);


    return () => {
      window.removeEventListener('sendUserId', handleUserIdEvent);
      console.log('Event listener removed for sendUserId');
    };
  }, []);

  console.log('AppWrapper component rendered with userID:', userID);

 

    return (<App userID={userID} />);

 

};


window.customElements.define('react-app', ReactApp);
