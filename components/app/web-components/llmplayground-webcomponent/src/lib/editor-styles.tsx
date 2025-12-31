/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/
export const styleMap = {
    HIGHLIGHT: {
      backgroundColor: "#faed27",
    },
    NORMAL: {
      backgroundColor: "transparent",
    },
    BOLD: {
      fontWeight: "bold",
    },
  };
  
  export const styles = {
    openai: {
      transition: "background-color 0.2s ease-in-out",
      backgroundColor: "#b9eebc",
      padding: "2px 0",
    },
    aicloud: {
      transition: "background-color 0.2s ease-in-out",
      backgroundColor: "#f6b2b3",
      padding: "2px 0",
    },
    azure: {
      transition: "background-color 0.2s ease-in-out",
      backgroundColor: "#a198e6",
      padding: "2px 0",
    },
    huggingface_local: {
      transition: "background-color 0.2s ease-in-out",
      backgroundColor: "#f6b2b3",
      padding: "2px 0",
    },
    cohere: {
      transition: "background-color 0.2s ease-in-out",
      backgroundColor: "#a198e6",
      padding: "2px 0",
    },
    huggingface: {
      transition: "background-color 0.2s ease-in-out",
      backgroundColor: "#D7BCE8",
      padding: "2px 0",
    },
    forefront: {
      backgroundColor: "#BCCAE8",
      padding: "2px 0",
    },
    anthropic: {
      backgroundColor: "#cc785c80",
      padding: "2px 0",
    },
    aleph_alpha: {
      backgroundColor: "#e3ff00",
      padding: "2px 0",
    },
    default: {
      backgroundColor: "transparent",
      transition: "background-color 0.2s ease-in-out",
      padding: "2px 0",
    },
  };
  
  export function getDecoratedStyle(provider: string, showHighlights: boolean) {
    if (showHighlights === false) return styles.default;
    switch (provider) {
      case "openai":
        return styles.openai;
      case "aicloud":
        return styles.aicloud;
      case "azure":
        return styles.azure;
      case "huggingface-local":
        return styles.huggingface_local;
      case "cohere":
        return styles.cohere;
      case "huggingface":
        return styles.huggingface;
      case "forefront":
        return styles.forefront;
      case "anthropic":
        return styles.anthropic;
      case "aleph-alpha":
        return styles.aleph_alpha;
  
      default:
        return styles.default;
    }
  }
  