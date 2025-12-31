/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/

// -------------------RAG Playground Setup Tab Data-------------------
export class SetupData {
  constructor(
    public projectId: string = "",
    public pipelineId: string = "",
    public name: string = "",
    public indexName: string = "",
    public chunkingStratergy: ChunkingStratergy = new ChunkingStratergy(),
    public embeddingModelName: string = "",
    public fileName: string = "",
    public filePath: string = ""
  ) {}
}

export class ChunkingStratergy {
  constructor(
    public page: Page = new Page(),
    public segement: Segement = new Segement(),
    public pageCharacter: PageCharacter = new PageCharacter()
  ) {}
}

export class Page {
  constructor(public pageEnabled: boolean = false) {}
}

export class PageCharacter {
  constructor(
    public pageCharacterEnabled: boolean = false,
    public charLimit: number = 0
  ) {}
}

export class Segement {
  constructor(
    public segementEnabled: boolean = false,
    public singleCol: boolean = false,
    public multiCol: MultiCol = new MultiCol()
  ) {}
}

export class MultiCol {
  constructor(
    public zigzag: boolean = false,
    public leftToRight: boolean = false
  ) {}
}

export enum ChunkingOptions {
  Page = "page",
  Segment = "segment",
  PageCharacter = "page-segment",
}

export enum PageOptions {
  SingleColumn = "singleCol",
  MultiColumn = "multiCol",
}

export enum SubPageOptions {
  LeftToRight = "leftToRight",
  ZigZag = "zigzag",
}

export enum IndexOptions {
  Vector = "vector",
  Sparse = "sparse",
  Hybrid = "hybrid",
}

// -------------------RAG Playground Query (search) Tab Data-------------------

export class SearchData {
  constructor(
    public question: string = "",
    public retrieval: Retrieval = new Retrieval(),
    public generation: Generation = new Generation()
  ) {}
}

export class Generation {
  constructor(
    public enabled: boolean = true,
    public temperature: number = 0.05,
    public top_k_used: number = 20,
    public total_attempts: number = 1
  ) {}
}

export class Retrieval {
  constructor(
    public enabled: boolean = true,
    public index_id: string = "",
    public pre_filter_fetch_k: number = 10,
    public filter_metadata: FilterMetadata = new FilterMetadata(),
    public top_k: number = 50,
    public datasource: Datasource = new Datasource(),
    public hybrid_search: HybridSearch = new HybridSearch()
  ) {}
}

export class Datasource {
  constructor(
    public vectorindex: SearchIndex = new SearchIndex(),
    public sparseindex: SearchIndex = new SearchIndex()
  ) {}
}

export class SearchIndex {
  constructor(public enabled: boolean = true) {}
}

export class FilterMetadata {
  constructor() {}
}

export class HybridSearch {
  constructor(public rrf: SearchIndex = new SearchIndex()) {}
}

export enum QueryTypeOptions {
  Setup = "setup",
  Search = "search",
  Status = "status",
}

// -------------------RAG Playground Chat Messages-------------------

export class ChatMessage {
  constructor(
    public id: string = "",
    public content: string = "",
    public role: ChatRole = ChatRole.USER,
    public timestamp: string = "",
    // public messageMetadata: MessageMetadata[] | undefined = []
  ) {}
}
export enum ChatRole {
  RAG = "rag",
  USER = "user",
}

export class MessageMetadata {
  constructor(
    public chunkId: string = "",
    public pageNo: number = 0,
    public sequenceNo: number = 0,
    public docName: string = "",
    public documentId: string = "",
    public chunkingMethod: string = "",
    public charCount: string = "",
    public score: number = 0.0,
    public content: string = ""
  ) {}
}
