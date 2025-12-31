
/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/
 import {
  ChangeDetectorRef,
  Component,
  ElementRef,
  HostListener,
  OnInit,
  TemplateRef,
  ViewChild,
} from "@angular/core";

import { v4 as uuidv4 } from "uuid";

import { MatTabGroup } from "@angular/material/tabs";
import { ToasterServiceService } from "src/app/services/toaster-service";
import { ConfigDataHelper } from "src/app/utils/config-data-helper";
import { CONSTANTS } from "src/app/common/constants";
import { RagPlaygroundService } from "src/app/services/rag-playground.service";
import { PipelineServiceService } from "src/app/services/pipeline-service.service";
import { MatAutocompleteSelectedEvent } from "@angular/material/autocomplete";
import { NgModel } from "@angular/forms";
import {
  ChatMessage,
  ChatRole,
  ChunkingOptions,
  ChunkingStratergy,
  IndexOptions,
  MessageMetadata,
  PageOptions,
  QueryTypeOptions,
  SearchData,
  SetupData,
  SubPageOptions,
} from "src/app/data/rag-playground-data";
import { MatDialog } from "@angular/material/dialog";
import { ChatWindowComponent } from "../chat-window/chat-window.component";
import { Metadata } from "src/app/data/update-model-data";

@Component({
  selector: "app-rag-playground-home-new",
  templateUrl: "./rag-playground-home.component.html",
  styleUrls: ["./rag-playground-home.component.scss"],
})
export class RagPlaygroundHomeComponent implements OnInit {
  @ViewChild(MatTabGroup) tabGroup: MatTabGroup;
  @ViewChild("indexInput") indexInput: NgModel;
  @ViewChild("indexInputSearch") indexInputSearch: NgModel;
  @ViewChild("fileDropRef") fileInput: ElementRef;
  @ViewChild("chatMessages") private chatMessagesContainer: ElementRef;
  @ViewChild("messageDialog") messageDialog: TemplateRef<any>;
  @ViewChild(ChatWindowComponent) chatWindow: ChatWindowComponent;

  constructor(
    private toaster: ToasterServiceService,
    private configDataHelper: ConfigDataHelper,
    private ragPgService: RagPlaygroundService,
    private pipelineService: PipelineServiceService,
    private dialog: MatDialog,
    private cdr: ChangeDetectorRef
  ) {}

  modelSetup = {
    height: 0,
    width: 0,
    selectedSetup: {},
    showSearch: false,
    setupDone: false,
    setupData: new SetupData(),
    uploadedFile: null as File,
    isDataLoaded: false,
    templateList: [],
    selectedTemplate: {} as any,
    indexId: null as String,
    indexList: [],
  };

  openMessageDialog(message: string, success: boolean = true): void {
    this.dialog.open(this.messageDialog, {
      data: { message: message, success: success },
    });
  }

  closeDialog(): void {
    this.dialog.closeAll();
  }

  widthOffset = 32;
  heightOffset = 150;

  ngOnInit(): void {
    this.resizeChildComponents();

    const promise2 = this.pipelineService.getPipelineListData(
      this.configDataHelper.getValue(CONSTANTS.CONFIG.RAG_PROJECT_ID),
      true
    );
    // load pipeline templates of type rag pipelines.
    promise2
      .then((value: any) => {
        this.modelSetup.templateList = value;
        console.log("Pipelines:", value);
      })
      .catch(() => {
        // this.toaster.failureWithMessage("Error in loading templates");
        console.log("Error in loading templates");
      });

    this.generateChatID();
    // push a welcome message to the chat window.
    this.addWelcomeMessage();
  }

  ngAfterViewInit() {
    this.scrollToBottom();
  }

  // fetches the list of indices. Called onInit and onTabChange
  fetchIndexList(pipelineId?: string, queryType?: string): Promise<any[]> {
    return new Promise((resolve, reject) => {
      this.ragPgService
        .getIndexList(pipelineId, queryType)
        .then((value: any) => {
          if (value["data"].length > 0) {
            console.log("In fetchIndexList:", value["data"]);
            resolve(value["data"]);
          } else {
            resolve([]);
          }
        })
        .catch((error) => {
          this.toaster.failureWithMessage("Error in loading index list");
          reject(error);
        });
    });
  }

  // function to handle the window resize event
  @HostListener("window:resize", ["$event"])
  onResize(event) {
    this.resizeChildComponents();
  }

  // function to resize the child components
  private resizeChildComponents() {
    const windowHeight = window.innerHeight;
    const windowWidth = window.innerWidth;
    this.modelSetup.height = windowHeight - this.heightOffset;
    this.modelSetup.width = windowWidth - this.widthOffset;
  }

  // ------------------------------------------ Section to handle the setup tab ------------------------------------------
  pageSegment = "";
  chunkingStrategy = "";
  disableChat = true;
  indexing = "";
  chunkingStratergyTemplate = new ChunkingStratergy();

  embedModelList = [
    { view: "text-embedding-ada-002", value: "text-embedding-ada-002" },
    { view: "all-MiniLM-L6-v2", value: "all-MiniLM-L6-v2" },
    { view: "mistral-embd", value: "mistral-embd" },
  ];

  modelList = [{ view: "OpenAI GPT 4", value: "openai-gpt4" }];

  onOptionSelected(event: MatAutocompleteSelectedEvent): void {
    const selectedValue = event.option.value;
    this.modelSetup.setupData.indexName = selectedValue.indexName;
    this.modelSetup.indexId = selectedValue.indexId; // Assuming indexId is the same as the selected value
    console.log("Option selected:", selectedValue);
  }

  onIndexNameChange(value: string): void {
    this.modelSetup.setupData.indexName = value;
    this.modelSetup.indexId = null; // Clear indexId if the user enters text manually
    console.log("Index name changed:", value);
  }

  chunkOptions = [
    { view: "Page", value: ChunkingOptions.Page },
    { view: "Segment", value: ChunkingOptions.Segment },
    { view: "Page-Character", value: ChunkingOptions.PageCharacter },
  ];

  pageOptions = [
    { view: "Single Column", value: PageOptions.SingleColumn },
    { view: "Multi Column", value: PageOptions.MultiColumn },
  ];

  subPageOptions = [
    { view: "Left to Right", value: SubPageOptions.LeftToRight },
    { view: "Zig Zag", value: SubPageOptions.ZigZag },
  ];

  onTabChanged(event) {
    console.log("Tabchanged event", event.index);
    if (event.index === 0) {
      this.disableChat = true;
      this.resetSearchData(); // reset the search tab data
    }
    if (event.index === 1) {
      this.disableChat = false;
      // this.modelSearch.indexList = this.fetchIndexList(); // get the latest index list
      this.resetSetupData(); // reset the setup tab data
    }
  }

  // file upload code
  onFileSelected(files: Event): void {
    // const input = event.target as HTMLInputElement;
    if (files && files[0]) {
      this.modelSetup.uploadedFile = files[0];
      console.log("File selected:", this.modelSetup.uploadedFile);
    }
    this.uploadFile(this.modelSetup.uploadedFile);
  }

  // Handler for file drop
  onFileDrop(event: DragEvent): void {
    event.preventDefault();
    const file = event.dataTransfer?.files[0] as File | null;
    // this.uploadFile(file);
    this.modelSetup.uploadedFile = file;
    console.log("File dropped:", this.modelSetup.uploadedFile);
    this.uploadFile(this.modelSetup.uploadedFile);
  }

  // Prevent default dragover behavior
  onDragOver(event: DragEvent): void {
    event.preventDefault();
  }

  // Call the service class method to upload the file
  uploadFile(file: File) {
    console.log("Uploading File:", file);
    const formData = new FormData();
    formData.append("file", file);

    if (this.modelSetup.setupData.indexName != "") {
      this.ragPgService
        .uploadFile(formData, this.modelSetup.setupData.indexName)
        .then((res) => {
          console.log("File uploaded:", res);
          this.modelSetup.setupData.filePath = res["data"]["path"];
          this.modelSetup.setupData.fileName =
            this.modelSetup.uploadedFile.name;
          this.toaster.success(117);
        })
        .catch((err) => {
          this.toaster.failureWithMessage(`Error in uploading file ${err}`);
        });
    } else {
      this.fileInput.nativeElement.value = "";
      this.modelSetup.uploadedFile = null;
      this.toaster.failureWithMessage("Please select an indexName");
    }
  }

  // handlers for setup submission
  // submitSetup() {
  //   this.resetSetupData();
  // }
  submitSetup() {
    this.logSetupTemplate();

    if (this.validateSetupDataTemplate()) {
      this.ragPgService
        .createSetup(this.modelSetup.setupData)
        .then((res) => {
          console.log("Setup created:", res);
          // this.toaster.success(118);
          // TODO: Add popup and then reset the SetupData fields.
          this.openMessageDialog(
            "The file is being processed. Please check the status under 'Query' tab.",
            true
          );
          this.resetSetupData();
        })
        .catch((err) => {
          this.openMessageDialog(
            "Error in processing file. Please try again later.",
            false
          );
          // this.toaster.failureWithMessage(`Error in creating setup ${err}`);
        });
    }
  }

  logSetupTemplate() {
    this.modelSetup.setupData["projectId"] = this.configDataHelper.getValue(
      CONSTANTS.CONFIG.RAG_PROJECT_ID
    );
    this.modelSetup.setupData["pipelineId"] =
      this.modelSetup.selectedTemplate["id"];
    this.modelSetup.setupData["name"] =
      this.modelSetup.selectedTemplate["pipeline"]["name"];
    console.log(this.modelSetup.setupData);
  }

  // validating setup data
  validateSetupDataTemplate(): boolean {
    const data = this.modelSetup.setupData;

    if (!data.projectId.trim()) {
      this.toaster.failureWithMessage("Project ID is required");
      return false;
    }

    if (!data.pipelineId.trim()) {
      this.toaster.failureWithMessage("Pipeline ID is required");
      return false;
    }

    if (!data.name.trim()) {
      this.toaster.failureWithMessage("Name is required");
      return false;
    }

    if (!data.indexName.trim()) {
      this.toaster.failureWithMessage("Index Name is required");
      return false;
    }
    // Validate chunking strategy
    if (data.chunkingStratergy.page.pageEnabled) {
      // Page strategy is enabled, no further validation needed for page
    } else if (data.chunkingStratergy.pageCharacter.pageCharacterEnabled) {
      // Page-segment strategy validation
      if (data.chunkingStratergy.pageCharacter.charLimit <= 0) {
        this.toaster.failureWithMessage(
          "For page-character, Character limit must be greater than 0"
        );
        return false;
      }
    } else if (data.chunkingStratergy.segement.segementEnabled) {
      // Segment strategy validation
      if (
        !data.chunkingStratergy.segement.singleCol &&
        !data.chunkingStratergy.segement.multiCol.zigzag &&
        !data.chunkingStratergy.segement.multiCol.leftToRight
      ) {
        this.toaster.failureWithMessage(
          "At least one chunking strategy must be selected"
        );
        return false;
      }
    } else {
      // Neither page, page-segment, nor segment strategy is enabled
      this.toaster.failureWithMessage(
        "Either Page, Page-Segment, or Segment strategy must be enabled"
      );
      return false;
    }

    if (!data.fileName.trim() || !data.filePath.trim()) {
      this.toaster.failureWithMessage(
        "Please select a file for indexing first"
      );
      return false;
    }

    return true;
  }

  // on change of pipeline template, for setup call the list index api.
  onPipelineTemplateChange(event: any, type: string) {
    const selectedTemplate = event.value;
    const pipelineId = selectedTemplate["id"];
    console.log("Pipeline template Change:", pipelineId);

    if (type === "setup") {
      this.fetchIndexList(pipelineId, "setup")
        .then((data) => {
          this.modelSetup.indexList = data;
          console.log("Updated Setup IndexList:", this.modelSetup.indexList);
          // else if (type === "query") {
          //   this.modelSearch.indexList = data;
          //   console.log("Updated Search IndexList:", this.modelSearch.indexList);
          // }
        })
        .catch((error) => {
          console.error("Error fetching index list: for ", type, error);
        });
    }
    // clear search or status radio.
    if (type === "query") {
      this.modelQuery.queryType = null;
    }
  }

  // handlers for radio option changes (chunkingStrategy)
  onChunkingStrategyChange(event: any): void {
    console.log("Chunking strategy changed:", event.value);
    // Reset the whole object here
    this.modelSetup.setupData["chunkingStratergy"] =
      this.chunkingStratergyTemplate;
    this.pageSegment = "";
    if (event.value === ChunkingOptions.Page) {
      this.modelSetup.setupData["chunkingStratergy"]["page"]["pageEnabled"] =
        true;
      this.modelSetup.setupData["chunkingStratergy"]["segement"][
        "segementEnabled"
      ] = false;
      this.modelSetup.setupData["chunkingStratergy"]["pageCharacter"][
        "pageCharacterEnabled"
      ] = false;
      this.modelSetup.setupData["chunkingStratergy"]["pageCharacter"][
        "charLimit"
      ] = 0;
    } else if (event.value === ChunkingOptions.Segment) {
      this.modelSetup.setupData["chunkingStratergy"]["page"]["pageEnabled"] =
        false;
      this.modelSetup.setupData["chunkingStratergy"]["segement"][
        "segementEnabled"
      ] = true;
      this.modelSetup.setupData["chunkingStratergy"]["pageCharacter"][
        "pageCharacterEnabled"
      ] = false;
      this.modelSetup.setupData["chunkingStratergy"]["pageCharacter"][
        "charLimit"
      ] = 0;
    } else if (event.value === ChunkingOptions.PageCharacter) {
      this.modelSetup.setupData["chunkingStratergy"]["page"]["pageEnabled"] =
        true;
      this.modelSetup.setupData["chunkingStratergy"]["segement"][
        "segementEnabled"
      ] = false;
      this.modelSetup.setupData["chunkingStratergy"]["segement"]["singleCol"] =
        false;
      this.modelSetup.setupData["chunkingStratergy"]["segement"]["multiCol"][
        "zigzag"
      ] = false;
      this.modelSetup.setupData["chunkingStratergy"]["segement"]["multiCol"][
        "leftToRight"
      ] = false;
    }
  }
  onPageSegmentChange(event: any): void {
    const selectedValue = event.value;
    console.log("Page Segment Changed:", selectedValue);
    if (selectedValue === PageOptions.MultiColumn) {
      this.modelSetup.setupData["chunkingStratergy"]["segement"]["singleCol"] =
        false;
    } else if (selectedValue === PageOptions.SingleColumn) {
      this.modelSetup.setupData["chunkingStratergy"]["segement"]["singleCol"] =
        true;
      this.modelSetup.setupData["chunkingStratergy"]["segement"]["multiCol"][
        "zigzag"
      ] = false;
      this.modelSetup.setupData["chunkingStratergy"]["segement"]["multiCol"][
        "leftToRight"
      ] = false;
    }
  }
  onPageSubSegmentChange(event: any): void {
    const selectedValue = event.value;
    console.log("Page Segment Changed:", selectedValue);
    if (selectedValue === SubPageOptions.ZigZag) {
      this.modelSetup.setupData["chunkingStratergy"]["segement"]["multiCol"][
        "zigzag"
      ] = true;
      this.modelSetup.setupData["chunkingStratergy"]["segement"]["multiCol"][
        "leftToRight"
      ] = false;
    } else if (selectedValue === SubPageOptions.LeftToRight) {
      this.modelSetup.setupData["chunkingStratergy"]["segement"]["multiCol"][
        "zigzag"
      ] = false;
      this.modelSetup.setupData["chunkingStratergy"]["segement"]["multiCol"][
        "leftToRight"
      ] = true;
    }
  }
  // handler for char limit field value
  onCharLimitChange(event: any): void {
    console.log("Char Limit Changed:", event);
    const inputValue = (event.target as HTMLInputElement).value;
    this.modelSetup.setupData["chunkingStratergy"]["pagesegment"]["charLimit"] =
      parseInt(inputValue);
  }

  // reset the search data fields.
  resetSetupData() {
    this.modelSetup.setupData = new SetupData();
    this.modelSetup.selectedTemplate = {};
    this.fileInput.nativeElement.value = "";
    this.modelSetup.indexId = null;
    this.chunkingStrategy = "";
    this.pageSegment = "";
    this.indexing = "";
    this.indexInput.reset();
    this.modelSetup.uploadedFile = null;
    this.modelSetup.indexList = [];
  }

  // Delete an index
  deleteIndex() {
    const promise = this.ragPgService.deleteIndex(this.modelSetup.indexId);
    promise
      .then((res) => {
        console.log("Index deleted:", res);
        this.modelSetup.indexList = this.modelSetup.indexList.filter(
          (index) => index.indexId !== this.modelSetup.indexId
        );
        this.modelSetup.indexId = null;
        this.modelSetup.setupData.indexName = "";
        this.indexInput.reset();
        this.toaster.success(119);
      })
      .catch((err) => {
        this.toaster.failureWithMessage(`Error in deleting index ${err}`);
      });
    console.log("Delete index");
  }

  // checks for empty objects
  isEmptyObject(obj: any): boolean {
    return obj && Object.keys(obj).length === 0 && obj.constructor === Object;
  }

  // ------------------------------------------ Section to handle the query tab ------------------------------------------

  // controls whether search or status of index is shown
  // queryType = null;

  queryTypeOptions = [
    { view: "Search", value: QueryTypeOptions.Search },
    { view: "Status", value: QueryTypeOptions.Status },
  ];
  // controls the load icon inplace of send btn.

  onQueryTypeChange(event: any): void {
    const pipelineId = this.modelQuery.selectedTemplate["id"];
    console.log("Query type changed:", event.value);
    this.modelQuery.queryType = event.value;

    this.fetchIndexList(pipelineId, this.modelQuery.queryType)
      .then((data) => {
        if (event.value === QueryTypeOptions.Status) {
          this.modelQuery.indexList = data;
          console.log("Updated Status IndexList:", this.modelQuery.indexList);
        } else if (event.value === QueryTypeOptions.Search) {
          this.modelSearch.indexList = data;
          console.log("Updated Search IndexList:", this.modelSearch.indexList);
        }
        // this.modelSearch.loading = false;
      })
      .catch((error) => {
        console.error("Error fetching index list:", error);
        // this.modelSearch.loading = false;
      });

    // if (event.value === QueryTypeOptions.Status) {
    //   // this.modelSearch.loading = true;

    // }
  }

  // filters the indexList in the query tab
  // filterIndexList(type: string): any[] {
  //   if (type === "setup") {
  //     console.log("In filterIndexList: returning active indices for setup");
  //     return this.modelSetup.indexList.filter(
  //       (index) => index.status === "Active"
  //     );
  //   } else if (type === "search") {
  //     console.log("In filterIndexList: returning active indices for search");
  //     return this.modelSearch.indexList.filter(

  //       (index) => index.status === "Active"
  //     );
  //   } else if (type === "status") {
  //     console.log("In filterIndexList: returning all incides for status");
  //     return this.modelSearch.indexList;
  //   }
  //   return [];
  // }

  modelQuery = {
    queryType: null,
    indexItem: null as any,
    indexList: [],
    selectedTemplate: {},
  };

  // getIndexes(type: string) {
  //   // in search tab only active indices are shown
  //   if (type === "search") {
  //     return this.modelSearch.indexList.filter(
  //       (index) => index.status === "Active"
  //     );
  //   }
  //   if (type === "status") {
  //     const indexListX = this.modelQuery.indexList;
  //     console.log("In getIndexes:", indexListX);
  //     return indexListX;
  //   }
  // }

  displayIndex(index: any): string {
    return index ? `${index.value} (${index.status})` : "";
  }

  // fetch the status of the selected index
  refreshIndexStatus(): void {
    this.ragPgService
      .indexStatus(this.modelQuery.indexItem.id)
      .then((res) => {
        this.modelQuery.indexItem.status = res["status"];
        console.log("Index Status Updated:", res);
        this.modelQuery.indexList = this.modelQuery.indexList.map((index) => {
          if (index.id === this.modelQuery.indexItem.id) {
            index.status = res["status"];
          }
          return index;
        });
      })
      .catch((err) => {
        this.toaster.failureWithMessage(
          `Error in updating index status ${err}`
        );
      });
  }

  // ------------------------------------------ Section to handle the search controls ------------------------------------------

  modelSearch = {
    indexList: [],
    waitingForAPI: false,
    generationModel: "",
    searchData: new SearchData(),
    messageText: "",
    selectedIndex: IndexOptions.Hybrid,
    loading: false,
    selectedMessage: new ChatMessage(),
    selectedMessageMetadata: undefined as MessageMetadata[],
    chatId: "",
  };

  // generates a chatID for every new chat. Called in onInit and whenever the clear button is clicked.
  generateChatID() {
    this.modelSearch.chatId = uuidv4();
  }

  indexOptions = [
    { view: "Vector", value: IndexOptions.Vector },
    { view: "Sparse", value: IndexOptions.Sparse },
    { view: "Hybrid", value: IndexOptions.Hybrid },
  ];

  // holds the messages in the chat window.
  messages: ChatMessage[] = [
  ];

  // search parameters

  resetSearchData() {
    this.modelSearch.searchData = new SearchData();
    this.modelSearch.messageText = "";
    this.messages = [];
    // this.modelSearch.top_k = 1;
    // this.modelSearch.temp = 0.1;
    this.modelSearch.waitingForAPI = false;
    this.modelSearch.generationModel = "";
    this.modelSearch.indexList = [];
    if (this.indexInputSearch) this.indexInputSearch.reset();
    this.modelQuery.indexItem = null;
    this.modelQuery.selectedTemplate = {};
    this.modelQuery.queryType = null;
    this.modelSearch.selectedMessage = new ChatMessage();
    this.modelSearch.selectedMessageMetadata = undefined;
    this.addWelcomeMessage();
  }

  // handlers for search submission
  // handles the index search type change
  onSearchTypeChange(event: any): void {
    console.log("Search type changed:", event.value);
    if (event.value === IndexOptions.Vector) {
      this.modelSearch.searchData.retrieval.datasource.vectorindex.enabled =
        true;
      this.modelSearch.searchData.retrieval.datasource.sparseindex.enabled =
        false;
      this.modelSearch.searchData.retrieval.hybrid_search.rrf.enabled = false;
    } else if (event.value === IndexOptions.Sparse) {
      this.modelSearch.searchData.retrieval.datasource.vectorindex.enabled =
        false;
      this.modelSearch.searchData.retrieval.datasource.sparseindex.enabled =
        true;
      this.modelSearch.searchData.retrieval.hybrid_search.rrf.enabled = false;
    } else if (event.value === IndexOptions.Hybrid) {
      this.modelSearch.searchData.retrieval.datasource.vectorindex.enabled =
        true;
      this.modelSearch.searchData.retrieval.datasource.sparseindex.enabled =
        true;
      this.modelSearch.searchData.retrieval.hybrid_search.rrf.enabled = true;
    }
  }

  // submit the search request
  submitSearch($event) {
    this.modelSearch.messageText = $event;
    this.modelSearch.waitingForAPI = true;
    this.modelSearch.searchData.question = this.modelSearch.messageText;

    // used for filtering the chunks
    const searchIndex = this.modelSearch.selectedIndex;

    this.logSearchTemplate();
    if (this.validateSearchDataTemplate()) {
      this.sendMessage();
      this.ragPgService
        .search(this.modelSearch.searchData)
        .then((res) => {
          const queryId = uuidv4();
          this.extractMetadata(res, searchIndex, queryId);
          const newMessage = new ChatMessage(
            queryId,
            res.response.answers[0]["answer"],
            ChatRole.RAG,
            new Date().toISOString()
          );
          this.messages.push(newMessage);
          this.modelSearch.selectedMessage = newMessage;

          console.log("Selected Message:", this.modelSearch.selectedMessage);
          // console.log("Messages:", this.messages);

          this.modelSearch.waitingForAPI = false;

          this.cdr.detectChanges();
          this.scrollToBottom();

          // this.toaster.success(120);
        })
        .catch((err) => {
          this.modelSearch.waitingForAPI = false;
          console.log("Error in search:", err);
          this.toaster.failureWithMessage(`Error in search:`);
        });
    } else {
      this.modelSearch.waitingForAPI = false;
    }
  }

  // extracts the metadata, calls the post api and sets the selectedMetadata obj with this value.
  extractMetadata(data, indexType: string, queryId: string): MessageMetadata[] {
    const chunkIds = data.response.answers[0].chunk_id.split(",");

    if (chunkIds.length === 0) return [];

    const topKList = data.response.answers[0].top_k_list;
    const metadataArray: MessageMetadata[] = [];
    for (const topK of topKList) {
      let sources = [];
      if (indexType === IndexOptions.Vector) {
        sources = topK.vectordb || [];
      } else if (indexType === IndexOptions.Sparse) {
        sources = topK.sparseindex || [];
      } else if (indexType === IndexOptions.Hybrid) {
        sources = topK.rrf || [];
      }

      for (const item of sources) {
        if (chunkIds.includes(item.meta_data.chunk_id)) {
          metadataArray.push({
            chunkId: item.meta_data.chunk_id,
            pageNo: item.meta_data.page_no,
            sequenceNo: item.meta_data.sequence_no,
            docName: item.meta_data.doc_name,
            documentId: item.meta_data.document_id,
            chunkingMethod: item.meta_data.chunking_method,
            charCount: item.meta_data.char_count,
            score: item.score,
            content: item.content,
          });
        }
      }
    }
    console.log("Chunks:", chunkIds);
    console.log("Metadata Array:", metadataArray);

    this.ragPgService
      .postMessageMetadata(metadataArray, this.modelSearch.chatId, queryId)
      .then((res) => {
        console.log("Metadata posted:", res);
      })
      .catch((err) => {
        console.error("Error in posting metadata:", err);
      });

    this.updateMetadataArray(metadataArray);
    return metadataArray;
  }

  // updates the metadata of selected msg from either the api or the passed value.
  updateMetadataArray(metadataArray?: MessageMetadata[], queryId?: string) {
    // if called from extract metadata then directly assign value.
    if (metadataArray && metadataArray.length != 0) {
      this.modelSearch.selectedMessageMetadata = metadataArray;
      console.log("called directly to assign value");
    }
    //else  call the metadata api for the selected message and then assign.
    else {
      this.ragPgService
        .getMessageMetadata(this.modelSearch.chatId, queryId)
        .then((res) => {
          console.log(res);
          this.modelSearch.selectedMessageMetadata = res.messageMetadata;
        })
        .catch((error) => {
          this.modelSearch.selectedMessageMetadata = [];
          console.error("Error fetching metadata:", error);
          // Handle the error here
        });
      console.log("called api to assign value");
    }
  }

  // simply prints the search data template
  logSearchTemplate() {
    console.log(this.modelSearch.searchData);
  }

  // validate the search data template
  validateSearchDataTemplate(): boolean {
    const data = this.modelSearch.searchData;

    if (!data.retrieval.index_id.trim()) {
      this.toaster.failureWithMessage("Index is required");
      return false;
    }

    if (!data.question.trim()) {
      this.toaster.failureWithMessage("Question is required");
      return false;
    }

    if (this.modelSearch.generationModel === "") {
      this.toaster.failureWithMessage("Generation model is required");
      return false;
    }

    return true;
  }

  // send user message to the chat
  sendMessage() {
    console.log("sendMessage called:", this.modelSearch.messageText);
    if (this.modelSearch.messageText !== "") {
      this.messages.push(
        new ChatMessage(
          uuidv4(),
          this.modelSearch.messageText,
          ChatRole.USER,
          new Date().toISOString()
        )
      );
      this.modelSearch.messageText = "";
      this.cdr.detectChanges();
      this.scrollToBottom();
    }
  }

  scrollToBottom(): void {
    if (this.chatWindow) this.chatWindow.scrollToBottom();
  }

  // handles selected msg which is passed to the metadata panel.
  handleSelectMessage(event: any) {
    console.log("Message selected:", event);
    this.modelSearch.selectedMessage = event;
    this.updateMetadataArray([], this.modelSearch.selectedMessage.id);
  }

  // this method clears the current chat window,
  // resets the metadata object and generates a new chatID.
  handleClearMessages() {
    console.log("Messages cleared:");
    this.modelSearch.chatId = uuidv4();
    this.messages = [];
    this.modelSearch.selectedMessage = new ChatMessage();
    this.modelSearch.selectedMessageMetadata = undefined;
    this.addWelcomeMessage();
  }

 // Add a welcome message with a delay
 addWelcomeMessage() {
  setTimeout(() => {
    this.messages.push(
      new ChatMessage(
        "000-0000-0000000-0000000",
        "Hi, how can I help you?",
        ChatRole.RAG,
        new Date().toISOString()
      )
    );
  }, 300); // 100 milliseconds delay
}
}
