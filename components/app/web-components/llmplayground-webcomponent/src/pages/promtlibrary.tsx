/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

// Grouping with domain Name and name in table column,styling for prompt with tooltip,usecase
import React, { useEffect, useRef, useState } from "react";
import NavBar from "../components/navbar";

interface Payload {
  name: string;
  domain: string[]; // Now an array
  mode: string;
  conversationContent: string;
  conversationRole: string;
  modelName: string;
  modelId: string;
  version: string;
  usecase: string;
  parameters: {
    max_new_tokens: number;
    temperature: number;
    top_p: number;
    frequency_penalty: number;
    presence_penalty: number;
  };
}

const PromptLibrary = () => {
  const [payloads, setPayloads] = useState<Payload[]>([]);
  const [expandedGroups, setExpandedGroups] = useState<{ [key: string]: boolean }>({});
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const groupsPerPage = 5;
  const groupRefs = useRef<{ [key: string]: HTMLDivElement | null }>({});
  const [hoveredPrompt, setHoveredPrompt] = useState<string | null>(null);
  const [tooltipPosition, setTooltipPosition] = useState<{ x: number; y: number } | null>(null);

  // Fetch and flatten payloads by domain
  const fetchPayloads = async () => {
    try {
      setLoading(true);
      const response = await fetch("http://localhost:5432/api/v1/library/prompt", {
        method: "GET",
        headers: {
          accept: "application/json",
          userId: "admin@xyz.com",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      console.log("Fetched data:", result);

      if (result && result.data && Array.isArray(result.data["Prompt List"])) {
        // Transform parameters as before
        const transformedPayloads = result.data["Prompt List"].map((payload: any) => {
          if (Array.isArray(payload.parameters)) {
            const parametersObject = payload.parameters.reduce(
              (acc: { [key: string]: any }, param: { key: string; value: any }) => {
                if (param.key === "max_tokens" || param.key === "max_new_tokens") {
                  acc["max_new_tokens"] = param.value || "";
                } else {
                  acc[param.key] = param.value || "";
                }
                return acc;
              },
              {
                max_new_tokens: "",
                temperature: "",
                top_p: "",
                frequency_penalty: "",
                presence_penalty: "",
              }
            );
            return { ...payload, parameters: parametersObject };
          }
          return {
            ...payload,
            parameters: {
              max_new_tokens: "",
              temperature: "",
              top_p: "",
              frequency_penalty: "",
              presence_penalty: "",
            },
          };
        });

        // Flatten by domain
        const flattenedPayloads: Payload[] = [];
        transformedPayloads.forEach((payload: Payload) => {
          if (Array.isArray(payload.domain)) {
            payload.domain.forEach((domain: string) => {
              flattenedPayloads.push({ ...payload, domain: [domain] });
            });
          } else if (payload.domain) {
            flattenedPayloads.push({ ...payload, domain: [payload.domain] });
          }
        });

        setPayloads(flattenedPayloads);
      } else {
        setPayloads([]);
      }

      setError(null);
    } catch (err) {
      console.error("Error fetching payloads:", err);
      setError("Failed to fetch data. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPayloads();
  }, []);

  // Group by domain (domain[0] since each is now a single-item array)
  const groupedPayloads = payloads.reduce((groups: { [key: string]: Payload[] }, payload) => {
    const groupName = payload.domain[0] || "Unnamed Domain";
    if (!groups[groupName]) {
      groups[groupName] = [];
    }
    groups[groupName].push(payload);
    return groups;
  }, {});

  const groupNames = Object.keys(groupedPayloads);
  const totalGroups = groupNames.length;

  const paginatedGroupNames = groupNames.slice(
    (currentPage - 1) * groupsPerPage,
    currentPage * groupsPerPage
  );

  const toggleGroup = (groupName: string) => {
    setExpandedGroups((prev) => {
      const isExpanded = !prev[groupName];
      if (isExpanded && groupRefs.current[groupName]) {
        groupRefs.current[groupName]?.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
      return {
        ...prev,
        [groupName]: isExpanded,
      };
    });
  };

  return (
    <div
      style={{
        backgroundColor: "white",
        height: "70vh",
        padding: "20px",
        overflowY: "scroll",
        scrollBehavior: "smooth",
      }}
    >
      <NavBar tab="promptlibrary" />
      <div style={{ marginTop: "20px" }}>
        {loading ? (
          <p>Loading...</p>
        ) : error ? (
          <p style={{ color: "black" }}>{error}</p>
        ) : (
          paginatedGroupNames.map((groupName, groupIndex) => (
            <div
              key={groupIndex}
              ref={(el) => (groupRefs.current[groupName] = el)}
              style={{
                marginBottom: "16px",
                borderRadius: "8px",
                padding: "15px",
                border: "1px solid lightgrey",
              }}
            >
              {/* Expand/Collapse Header */}
              <div
                onClick={() => toggleGroup(groupName)}
                style={{
                  cursor: "pointer",
                  fontWeight: "bold",
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  fontFamily: "Roboto, Arial, sans-serif",
                  color: "#42619d",
                }}
              >
                <span>{groupName}</span>
                <span>{expandedGroups[groupName] ? "▼" : "▶"}</span>
              </div>

              {/* Table Content */}
              {expandedGroups[groupName] && (
                <div
                  style={{
                    marginTop: "10px",
                    border: "1px solid black",
                    borderRadius: "8px",
                    padding: "10px",
                    maxHeight: "300px",
                    overflowY: "auto",
                    scrollBehavior: "smooth",
                  }}
                >
                  <table
                    style={{
                      width: "100%",
                      borderCollapse: "collapse",
                      backgroundColor: "white",
                      color: "black",
                    }}
                  >
                    <thead>
                      <tr>
                        <th style={{ fontSize: "13px", fontWeight: "bold", padding: "8px", textAlign: "left", borderBottom: "1px solid lightgrey" }}>Name</th>
                        <th style={{ fontSize: "13px", fontWeight: "bold", padding: "8px", textAlign: "left", borderBottom: "1px solid lightgrey", width: "14%" }}>Prompt</th>
                        <th style={{ fontSize: "13px", fontWeight: "bold", padding: "8px", textAlign: "left", borderBottom: "1px solid lightgrey" }}>Model</th>
                        <th style={{ fontSize: "13px", fontWeight: "bold", padding: "8px", textAlign: "left", borderBottom: "1px solid lightgrey" }}>Mode</th>
                        <th style={{ fontSize: "13px", fontWeight: "bold", padding: "8px", textAlign: "left", borderBottom: "1px solid lightgrey" }}>Version</th>
                        <th style={{ fontSize: "13px", fontWeight: "bold", padding: "8px", textAlign: "left", borderBottom: "1px solid lightgrey" }}>Conversation Role</th>
                        <th style={{ fontSize: "13px", fontWeight: "bold", padding: "8px", textAlign: "left", borderBottom: "1px solid lightgrey" }}>Usecase</th>
                        <th style={{ fontSize: "13px", fontWeight: "bold", padding: "8px", textAlign: "left", borderBottom: "1px solid lightgrey" }}>Max New Tokens</th>
                        <th style={{ fontSize: "13px", fontWeight: "bold", padding: "8px", textAlign: "left", borderBottom: "1px solid lightgrey" }}>Temperature</th>
                        <th style={{ fontSize: "13px", fontWeight: "bold", padding: "8px", textAlign: "left", borderBottom: "1px solid lightgrey" }}>Top P</th>
                        <th style={{ fontSize: "13px", fontWeight: "bold", padding: "8px", textAlign: "left", borderBottom: "1px solid lightgrey" }}>Frequency Penalty</th>
                        <th style={{ fontSize: "13px", fontWeight: "bold", padding: "8px", textAlign: "left", borderBottom: "1px solid lightgrey" }}>Presence Penalty</th>
                      </tr>
                    </thead>
                    <tbody>
                      {groupedPayloads[groupName].map((payload, index) => (
                        
                        <tr key={index}>
                          <td style={{ fontSize: "13px", padding: "8px",verticalAlign:"top" }}>{payload.name}</td>
                          {/* <td
                            style={{
                              fontSize: "13px",
                              padding: "8px",
                              width: "14%",
                              maxWidth: "14%",
                              display: "-webkit-box",
                              WebkitLineClamp: 3,
                              WebkitBoxOrient: "vertical",
                              overflow: "hidden",
                              textOverflow: "ellipsis",
                              cursor: "pointer",
                            }}
                            title={payload.conversationContent}
                          >
                            {payload.conversationContent}
                          </td> */}
  <td
  style={{
    fontSize: "13px",
    padding: "8px",
    width: "250px",         // or any width 
    maxWidth: "250px",
    whiteSpace: "nowrap",
    overflow: "hidden",
    textOverflow: "ellipsis",
    cursor: "pointer",
    verticalAlign: "top",
    position: "relative",
  }}
  onMouseEnter={e => {
    setHoveredPrompt(payload.conversationContent);
    setTooltipPosition({ x: e.clientX, y: e.clientY });
  }}
  onMouseLeave={() => setHoveredPrompt(null)}
>
  {payload.conversationContent}
  {hoveredPrompt === payload.conversationContent && tooltipPosition && (
    <div
      style={{
        position: "fixed",
        // top: tooltipPosition.y + 10,
        // top: tooltipPosition.y - 120, // Show above the mouse
        top: tooltipPosition.y - (payload.conversationContent.length > 100 ? 200 : 40),
        left: tooltipPosition.x + 40,
        background: "white",
        color: "black",
        border: "1px solid #ccc",
        borderRadius: "6px",
        padding: "12px",
        zIndex: 9999,
        maxWidth: "400px",
        maxHeight: "300px",
        overflowY: "auto",
        overflowX: "auto",
        boxShadow: "0 2px 8px rgba(0,0,0,0.15)",
        whiteSpace: "pre-wrap",
        fontSize: "13px",
        verticalAlign: "top", 
      }}
    >
      {payload.conversationContent}
      
    </div>
    
  )}
</td>
                          <td style={{ fontSize: "13px", padding: "8px",verticalAlign: "top"  }}>{payload.modelName}</td>
                          <td style={{ fontSize: "13px", padding: "8px",verticalAlign: "top"  }}>{payload.mode}</td>
                          <td style={{ fontSize: "13px", padding: "8px",verticalAlign: "top" }}>{payload.version}</td>
                          <td style={{ fontSize: "13px", padding: "8px",verticalAlign: "top"  }}>{payload.conversationRole}</td>
                          <td style={{ fontSize: "13px", padding: "8px",verticalAlign: "top" }}>{payload.usecase}</td>
                          <td style={{ fontSize: "13px", padding: "8px" ,verticalAlign: "top" }}>{payload.parameters?.max_new_tokens}</td>
                          <td style={{ fontSize: "13px", padding: "8px" ,verticalAlign: "top" }}>{payload.parameters?.temperature}</td>
                          <td style={{ fontSize: "13px", padding: "8px",verticalAlign: "top"  }}>{payload.parameters?.top_p}</td>
                          <td style={{ fontSize: "13px", padding: "8px",verticalAlign: "top"  }}>{payload.parameters?.frequency_penalty}</td>
                          <td style={{ fontSize: "13px", padding: "8px" ,verticalAlign: "top" }}>{payload.parameters?.presence_penalty}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          ))
        )}
      </div>
      {/* Group-Level Pagination */}
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          position: "fixed",
          bottom: "20px",
          left: "50%",
          transform: "translateX(-50%)",
          color: "#42619d",
        }}
      >
        <button
          onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
          disabled={currentPage === 1}
          style={{
            padding: "5px 10px",
            marginRight: "10px",
            backgroundColor: "transparent",
            color: "#42619d",
            border: "none",
            cursor: "pointer",
          }}
        >
          &lt;
        </button>
        <span>
          {currentPage} of {Math.ceil(totalGroups / groupsPerPage)}
        </span>
        <button
          onClick={() =>
            setCurrentPage((prev) =>
              Math.min(prev + 1, Math.ceil(totalGroups / groupsPerPage))
            )
          }
          disabled={currentPage === Math.ceil(totalGroups / groupsPerPage)}
          style={{
            padding: "5px 10px",
            marginLeft: "10px",
            backgroundColor: "transparent",
            color: "#42619d",
            border: "none",
            cursor: "pointer",
          }}
        >
          &gt;
        </button>
      </div>
    </div>
  );
};

export default PromptLibrary;
