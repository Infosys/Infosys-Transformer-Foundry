/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders, HttpParams } from "@angular/common/http";
import { ConfigDataHelper } from "../utils/config-data-helper";
import { CONSTANTS } from "../common/constants";
import { MessageMetadata } from "../data/rag-playground-data";

@Injectable({
  providedIn: "root",
})
export class RagPlaygroundService {
  constructor(
    private httpClient: HttpClient,
    public configDataHelper: ConfigDataHelper
  ) {}

  // This func handles file upload for the playground
  uploadFile(formData: FormData, index: string): Promise<any> {
    console.log("uploadFile entry");
    const parent = this;
    const url =
      this.configDataHelper.getValue(
        CONSTANTS.CONFIG.PL_MGMT_SERVICE_BASER_URL_V1
      ) + CONSTANTS.APIS.RAG_PLAYGROUND_SERVICE.UPLOAD_FILE;

    // const formData = new FormData();
    // formData.append("file", file);
    const params = new HttpParams().set("indexName", index);

    console.log("uploadFile half before return", url, formData, params);

    return new Promise(function (fulfilled, rejected) {
      parent.httpClient.post(url, formData, { params }).subscribe(
        (response) => {
          if (response["code"] == 200) {
            console.log("uploadFile success");
            fulfilled(response);
          } else {
            console.log("uploadFile failure");
            rejected(response);
          }
        },
        (error) => {
          console.log("uploadFile error", error);
          rejected(error);
        }
      );
    });
  }

  // This func creates a new setup to trigger the indexing pipeline
  createSetup(data: any): Promise<any> {
    console.log("createSetup entry");
    const parent = this;
    const url =
      this.configDataHelper.getValue(
        CONSTANTS.CONFIG.PL_MGMT_SERVICE_BASER_URL_V1
      ) + CONSTANTS.APIS.RAG_PLAYGROUND_SERVICE.CREATE_SETUP;

    const headerDict = {
      userId: this.configDataHelper.getValue(CONSTANTS.CONFIG.GUSER_ID),
    };
    const requestOptions = {
      headers: new HttpHeaders(headerDict),
    };

    return new Promise((fulfilled, rejected) => {
      parent.httpClient.post(url, data, requestOptions).subscribe(
        (res) => {
          if (res["code"] == 200) {
            console.log("createSetup success", res);
            fulfilled(res);
          } else {
            console.log("createSetup failure");
            rejected(res);
          }
        },
        (error) => {
          console.log("createSetup error", error);
          rejected(error);
        }
      );
    });
  }

  // This func gets list of existing indexes
  getIndexList(pipelineId?: string, queryType?: string): Promise<any> {
    return new Promise((fulfilled, rejected) => {
      let url =
        this.configDataHelper.getValue(
          CONSTANTS.CONFIG.PL_MGMT_SERVICE_BASER_URL_V1
        ) +
        CONSTANTS.APIS.RAG_PLAYGROUND_SERVICE.GET_INDEX_LIST +
        "?projectId=" +
        this.configDataHelper.getValue(CONSTANTS.CONFIG.RAG_PROJECT_ID);

      if (pipelineId) url += `&pipelineId=${pipelineId}`;

      if (queryType) url += `&queryType=${queryType}`;

      const headerDict = {
        // userId: this.configDataHelper.getValue(CONSTANTS.CONFIG.GUSER_ID),
      };
      const requestOptions = {
        headers: new HttpHeaders(headerDict),
      };

      this.httpClient.get(url, requestOptions).subscribe((res) => {
        if (res["code"] == 200) {
          console.log("getIndexList success", res);
          fulfilled(res);
        } else {
          console.log("getIndexList failure");
          rejected(res);
        }
      });
    });
  }

  // This func deletes an existing index
  deleteIndex(indexId: String): Promise<any> {
    const parent = this;
    return new Promise((fulfilled, rejected) => {
      const url =
        this.configDataHelper.getValue(
          CONSTANTS.CONFIG.PL_MGMT_SERVICE_BASER_URL_V1
        ) +
        CONSTANTS.APIS.RAG_PLAYGROUND_SERVICE.DELETE_INDEX.replace(
          CONSTANTS.PLACEHOLDER.INDEXID,
          `${indexId}`
        );
      const headerDict = {
        userId: this.configDataHelper.getValue(CONSTANTS.CONFIG.GUSER_ID),
      };
      const requestOptions = {
        headers: new HttpHeaders(headerDict),
      };

      this.httpClient.delete(url, requestOptions).subscribe((res) => {
        if (res["code"] == 200) {
          console.log("deleteIndex success", res);
          fulfilled(res);
        } else {
          console.log("deleteIndex failure");
          rejected(res);
        }
      });
    });
  }

  // RAG search service call
  search(data: any): Promise<any> {
    return new Promise((fulfilled, rejected) => {
      const url =
        this.configDataHelper.getValue(CONSTANTS.CONFIG.RAG_SEARCH_BASE_URL) +
        CONSTANTS.APIS.RAG_PLAYGROUND_SERVICE.SEARCH_RAG;

      this.httpClient.post(url, data).subscribe(
        (res) => {
          if (res["responseCde"] == 200) {
            console.log("search success", res);
            fulfilled(res);
          } else {
            console.log("search failure");
            rejected(res);
          }
        },
        (error) => {
          console.log("Error in Search Service", error);
          rejected(error);
        }
      );
    });
  }

  // not used currently
  indexStatus(indexId: string): Promise<any> {
    return new Promise((fulfilled, rejected) => {
      const url =
        this.configDataHelper.getValue(
          CONSTANTS.CONFIG.PL_MGMT_SERVICE_BASER_URL_V1
        ) +
        CONSTANTS.APIS.RAG_PLAYGROUND_SERVICE.GET_INDEX_STATUS.replace(
          CONSTANTS.PLACEHOLDER.INDEXID,
          `${indexId}`
        );

      const headerDict = {
        userId: this.configDataHelper.getValue(CONSTANTS.CONFIG.GUSER_ID),
      };
      const requestOptions = {
        headers: new HttpHeaders(headerDict),
      };

      this.httpClient.get(url, requestOptions).subscribe((res) => {
        if (res["code"] == 200) {
          console.log("indexStatus success", res);
          fulfilled(res["data"]);
        } else {
          console.log("indexStatus failure");
          rejected(res["data"]);
        }
      });
    });
  }

  // post the messsage metadata to db; called on search api response.
  postMessageMetadata(
    data: MessageMetadata[],
    chatId: string,
    queryId: string
  ): Promise<any> {
    return new Promise((fulfilled, rejected) => {
      const url =
        this.configDataHelper.getValue(
          CONSTANTS.CONFIG.PL_MGMT_SERVICE_BASER_URL_V1
        ) + CONSTANTS.APIS.RAG_PLAYGROUND_SERVICE.POST_MESSAGE_METADATA;

      const requestOptions = {};

      const payload = {
        chatId: chatId,
        queryId: queryId,
        messageMetadata: data,
      };

      this.httpClient.post(url, payload, requestOptions).subscribe(
        (res) => {
          if (res["code"] == 200) {
            console.log("postMessageMetadata success", res);
            fulfilled(res);
          } else {
            console.log("postMessageMetadata failure");
            rejected(res);
          }
        },
        (error) => {
          console.log("postMessageMetadata error", error);
          rejected(error);
        }
      );
    });
  }

  // fetch the message metadata from db; called on message selection.
  getMessageMetadata(chatId: string, queryId: string): Promise<any> {
    return new Promise((fulfilled, rejected) => {
      const url =
        this.configDataHelper.getValue(
          CONSTANTS.CONFIG.PL_MGMT_SERVICE_BASER_URL_V1
        ) + CONSTANTS.APIS.RAG_PLAYGROUND_SERVICE.MESSAGE_METADATA;

      const requestOptions = {
        params: new HttpParams().set("queryId", queryId).set("chatId", chatId),
      };

      this.httpClient.get(url, requestOptions).subscribe(
        (res) => {
          if (res["code"] == 200) {
            console.log("getMessageMetadata success", res);
            fulfilled(res['data']);
          } else {
            console.log("getMessageMetadata failure");
            rejected(res);
          }
        },
        (error) => {
          console.log("getMessageMetadata error", error);
          rejected(error);
        }
      );
    });
  }
}
