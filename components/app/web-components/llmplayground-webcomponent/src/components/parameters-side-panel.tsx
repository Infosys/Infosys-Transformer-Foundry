/** ================================================================================================================# *
 * # ===============================================================================================================# *
 * # Copyright 2025 Infosys Ltd.                                                                                    # *
 * # Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # *
 * # http://www.apache.org/licenses/                                                                                # *
 * # ===============================================================================================================# *
 **/
import React, { useContext, useEffect, useState } from "react"
import { Checkbox } from "./ui/checkbox"
import { useBreakpoint } from "../hooks/use-breakpoint"
import ParameterSlider from "./parameter-slider"
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "./ui/select"
import MultiSelect from "./multi-select"
import { uuid } from "uuidv4"
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "./ui/tooltip"
import { ParametersContext, ModelsContext, ModelsStateContext } from "../app"
import { BarChart2, Copy, Trash2, Filter } from "lucide-react"
import {handleSelectModel} from "../lib/utils"

const modelProviders = {
  forefront: "Forefront",
  "huggingface-local": "Hugging Face (Local)",
  huggingface: "Hugging Face",
  "aleph-alpha": "Aleph Alpha",
  anthropic: "Anthropic",
  cohere: "co:here",
  openai: "OpenAI",
  aicloud: "AI Cloud",
  azure: "Azure",
}

const modelTypes = {
  "Text": ['Mistral-7b', 'mixtral8x7b', 'sgpt-model', 'Llama2-7b','gpt4_new','gpt-4-32k_2','gpt-35-turbo-new'],
  "Embedding": [ "mistral-embed"],
  "Code": ['starcoder2-3b', 'starcoderbase', 'codegen', 'sql-coder-34b', 'code-llama'],
  "Image": ['stablediffusion', "StableDiffusion-XL"],
  // "Audio": ["whisper-m"],
}

const ParametersSidePanel = ({ showModelDropdown, showModelList }) => {
  const { isLg } = useBreakpoint("lg")
  const { parametersContext, setParametersContext } = useContext(ParametersContext)
  const { modelsContext, setModelsContext } = useContext(ModelsContext)
  const { modelsStateContext, setModelsStateContext } = useContext(ModelsStateContext)

  const [modelSearchValue, setModelSearchValue] = React.useState<string>("")
  const [modelType, setModelType] = React.useState<string>("")
  const {modelList, setModelList} = React.useState<string[]>([])
 
  const [number_of_models_enabled, setSelectedModelsCount] = React.useState(
    modelsStateContext.filter(
      (modelState) => modelState.enabled
    ).length
  )

  const number_of_models_selected = modelsStateContext.filter(
    (modelState) => modelState.selected
  ).length


 const modelTypes = modelsStateContext.reduce((acc, modelState) => {
  const unwantedKeywords = ['image', 'speech', 'sound', 'embedding'];
  if (!unwantedKeywords.some(keyword => modelState.tasktype.includes(keyword))) {
    if (!acc[modelState.tasktype]) {
      acc[modelState.tasktype] = [];
    }
    acc[modelState.tasktype].push(modelState.name.split(":")[1]);
  }
  return acc;
}, {});

  
  const models_shared_keys = Object.keys(modelsContext).length === 0 ? {} : modelsStateContext
    .filter(
      (modelState) =>
        modelState.enabled &&
        (number_of_models_selected >= 1 ? modelState.selected : true)
    )
    .map((modelState) => (modelsContext[modelState.name].defaultParameters))
    .flatMap((parameter) =>
      Object.entries(parameter).map(([key, parameter]) => ({
        key,
        range: parameter["range"] || [],
      }))
    )
    .reduce((acc, { key, range }) => {
      acc[key] = acc[key] || { range: [] }
      acc[key].range = [...new Set([...acc[key].range, ...range])]
      return acc
    }, {})
  
    // in this useEffect calculate the model list to display based on the modelType (filter using modelsStateContext[tasktype])
    useEffect(()=>{
      // when modelType changes, update the  and disable models of different types.
      console.log("modelsContext", modelsContext)
      console.log("modelsStateContext", modelsStateContext)

      setModelsStateContext(
        modelsStateContext.map((modelState: any) => {
          modelState.selected = false
          if (!showModelDropdown)
            modelState.enabled = false
          return modelState
        })
      )

    },[modelType])

    const modelTypeFilter = (model: string) => {
      // console.log(model, modelType, modelTypes[modelType], selectedModel?.name); 

      const typeList = modelTypes[modelType];
      if (typeList?.includes(model)){
        return true;
      }
      return false;
    }

  const generate_parameters_sliders = () => {

    console.log("Rendering parameter sliders");
    
    return [
      {
        title: "Maximum Length",
        name: "max_new_tokens",
        type: "number",
        step: 1,
        tooltipContent: (
          <p>
            Maximum number of tokens to generate. <br /> Responses are not
            guaranted to fill up <br /> to the maximum desired length. <br />
          </p>
        ),
        normalizeFn: (value) => parseInt(value),
      },
      {
        title: "Maximum Length",
        name: "max_tokens",
        type: "number",
        step: 1,
        tooltipContent: (
          <p>
            Maximum number of tokens to generate. <br /> Responses are not
            guaranted to fill up <br /> to the maximum desired length. <br />
          </p>
        ),
        normalizeFn: (value) => parseInt(value),
      },
      {
        title: "Temperature",
        name: "temperature",
        type: "number",
        step: 0.01,
        tooltipContent: (
          <p>
            A non-negative float that tunes the degree <br /> of randomness in
            generation. Lower <br />
            temperatures mean less random generations.
            <br />
          </p>
        ),
        normalizeFn: (value) => parseFloat(value),
      },
      {
        title: "Top P",
        name: "top_P",
        type: "number",
        step: 0.01,
        tooltipContent: (
          <p>
            If set to float less than 1, only the smallest <br /> set of most
            probable tokens with probabilities <br /> that add up to top_p or
            higher are kept for
            <br /> generation. <br />
          </p>
        ),
        normalizeFn: (value) => parseFloat(value),
      },
      {
        title: "Top P",
        name: "top_p",
        type: "number",
        step: 0.01,
        tooltipContent: (
          <p>
            If set to float less than 1, only the smallest <br /> set of most
            probable tokens with probabilities <br /> that add up to top_p or
            higher are kept for
            <br /> generation. <br />
          </p>
        ),
        normalizeFn: (value) => parseFloat(value),
      },
      {
        title: "Top K",
        name: "top_K",
        type: "number",
        step: 1,
        tooltipContent: (
          <p>
            Can be used to reduce repetitiveness of <br />
            generated tokens. The higher the value,
            <br /> the stronger a penalty is applied to
            <br />
            previously present tokens, proportional
            <br /> to how many times they have already
            <br /> appeared in the prompt or prior generation. <br />
          </p>
        ),
        normalizeFn: (value) => parseInt(value),
      },
      {
        title: "Frequency Penalty",
        name: "frequency_penalty",
        type: "number",
        step: 0.01,
        tooltipContent: (
          <p>
            Can be used to reduce repetitiveness of <br />
            generated tokens. The higher the value,
            <br /> the stronger a penalty is applied to
            <br />
            previously present tokens, proportional
            <br /> to how many times they have already
            <br /> appeared in the prompt or prior generation.
          </p>
        ),
        normalizeFn: (value) => parseFloat(value),
      },
      {
        title: "Presence Penalty",
        name: "presence_penalty",
        type: "number",
        step: 0.01,
        tooltipContent: (
          <p>
            Can be used to reduce repetitiveness of <br />
            generated tokens. Similar to Frequency Penalty,
            <br /> except that this penalty is applied equally <br /> to all
            tokens that have already appeared,
            <br />
            regardless of their <br /> exact frequencies. <br />
          </p>
        ),
        normalizeFn: (value) => parseFloat(value),
      },
      {
        title: "Repetition Penalty",
        name: "repetition_Penalty",
        type: "number",
        step: 0.01,
        tooltipContent: (
          <p>
            Akin to presence penalty. The repetition penalty is meant <br /> to
            avoid sentences that repeat themselves without <br /> anything
            really interesting.{" "}
          </p>
        ),
        normalizeFn: (value) => parseFloat(value),
      },
    ]
      .filter((parameter) => parameter.name in models_shared_keys)
      .map((parameter) => ({
        ...parameter,
        value: parametersContext[parameter.name],
        min: models_shared_keys[parameter.name].range[0],
        max: models_shared_keys[parameter.name].range[1],
        disabled: 
        modelsStateContext.filter(
          (modelState) => modelState.enabled
        ).length === 0 ||
          models_shared_keys[parameter.name].range.length > 2,
        
      }))
      .map((parameter) => {

        return (
          <ParameterSlider
            key={parameter.name}
            title={parameter.title}
            type={parameter.type}
            defaultValue={parameter.value}
            disabled={parameter.disabled}
            onChangeValue={(value: number) => {
              setModelsStateContext(
                modelsStateContext.map((modelState: any) => {
                  if (
                    modelState.parameters[parameter.name] &&
                    (number_of_models_selected === 0 || modelState.selected)
                  ) {
                    modelState.parameters[parameter.name] = value
                  }

                  return modelState
                })
              )
              setParametersContext({
                ...parametersContext,
                [parameter.name]: value,
              })
            }}
            min={parameter.min}
            max={parameter.max}
            step={parameter.step}
            normalizeInputData={parameter.normalizeFn}
            tooltipContent={
              <>
                {parameter.tooltipContent}
                {number_of_models_enabled === 0 ? (
                  <p>
                    <b>Disabled:</b> no models have been enabled.
                  </p>
                ) : parameter.disabled ? (
                  <p>
                    <b>Disabled:</b> the range of values for this parameter
                    <br /> <b>is not</b> uniform across all models.
                    <br />
                    <b>Tip:</b> to edit similar models, tap the models on
                    <br /> the list or select them by clicking their name
                    <br /> above their respective editor.
                  </p>
                ) : null}
              </>
            }
          />
        )
      })
  }

  const generate_card = (modelState: any) => {
    return (
      <div
        key={`selected_${modelState.tag}`}
        className={`relative select-none my-2 flex justify-center items-center rounded-md border border-slate-200 font-mono text-sm dark:border-slate-700 overflow-hidden ${
          modelState.selected ? "bg-slate-200 dark:bg-slate-200" : ""
          } ${
          modelState.enabled
            ? "cursor-pointer hover:bg-slate-200 dark:hover:bg-slate-200"
            : ""
          }`}
      >
        <div
          className={`pl-4 py-3 flex-1 overflow-hidden ${
            !modelState.enabled ? "text-zinc-400" : ""
            }`}
          onClick={(event) => {
            if (modelState.enabled)
              handleSelectModel(
                modelState,
                modelsStateContext,
                setModelsStateContext,
                parametersContext,
                setParametersContext,
                event.ctrlKey || event.metaKey
              )
          }}
        >
          {modelState.name.split(":")[1]}
          <br />
          <span style={{ fontSize: "12px" }}>
            Provider: <i>{modelState.provider}</i>
          </span>
          <br />
        </div>

        {/* <Copy
          size={10}
          className="absolute top-2 right-2"
          onClick={() => {
            const index_of_model = modelsStateContext.findIndex(
              (m: any) => m.name === modelState.name
            )
            const name_fragments = modelState.name.split(":")
            setModelsStateContext([
              ...modelsStateContext.slice(0, index_of_model + 1),
              {
                ...modelState,
                is_clone: true,
                tag: `${name_fragments[0]}:${name_fragments[1]}:${uuid()}`,
              },
              ...modelsStateContext.slice(index_of_model + 1),
            ])
          }}
        /> */}

        <Checkbox
          className="mr-6"
          key={modelState.tag}
          checked={modelState.enabled}
          disabled={disableModelSelection(modelState)}
          onCheckedChange={(val: boolean) => {
            setModelsStateContext(
              modelsStateContext.map((m: any) => {
                if (m.tag === modelState.tag) {
                  console.log("Inside checkbox Model Card", m, val);
                  
                  return {
                    ...m,
                    enabled: val,
                    selected: false
                  }
                }
                return m
              })
            )
            console.log("Generate Model Card", modelsStateContext)
            setSelectedModelsCount(
              modelsStateContext.filter(
                (modelState) => modelState.enabled
              ).length
            )
            console.log("Generate Model Card", modelsStateContext, number_of_models_selected, number_of_models_enabled)
          }}
        />
        {modelState.is_clone && false ? (
          <Trash2
            size={10}
            className="absolute bottom-2 right-2"
            onClick={() => {
              setModelsStateContext(
                modelsStateContext.filter((m: any) => m.tag !== modelState.tag)
              )
            }}
          />
        ) : null}
      </div>
    )
  }

  const disableModelSelection = (modelState) => {
    console.log("Disable Model Selection", number_of_models_enabled)
    if (modelsStateContext.filter(
      (modelState) => modelState.enabled
    ).length === 3)
      return !modelState.enabled
    else
      return false
  }

  const generate_list = () => {
    if (!showModelList) return null

    return (
      <>
        <div style={{marginTop: '0.55rem'}}>
          <span className="flow-root inline-block align-middle"
          >
            <p className="text-sm font-medium float-left align-text-top" style={{marginBottom:'0px', fontWeight: 'normal'}}>
              Model Type
            </p>
            <Select
              value={modelType || ""}
              onValueChange={(value) => {
                setModelType(value)
              }}>
              <SelectTrigger
                className="w-full"
                onKeyDown={(e) => {
                  if (e.code === "Enter" && e.metaKey) {
                    e.preventDefault()
                  }
                }}
              >
                <SelectValue placeholder="Select the task type" />
                <SelectContent
                  onKeyDown={(e) => {
                    if (e.code === "Enter" && e.metaKey) {
                      e.preventDefault()
                    }
                  }}
                >
                  <SelectGroup>
                    {Object.entries(modelTypes).map(([type, tasks]) => {
                      return (
                        <div key={type}>
                          <SelectItem
                            value={type}
                            title={type}
                            onKeyDown={(e) => {
                              if (e.code === "Enter" && e.metaKey) {
                                e.preventDefault()
                              }
                            }}
                          >{type?.length > 22 ? `${type.slice(0, 22)}...` : type}</SelectItem>
                        </div>)
                    }
                    )
                    }

                  </SelectGroup>
                </SelectContent>
              </SelectTrigger>
            </Select>
          </span>
        </div>
        {/* Hide the enable All and search bar divs. */}
        {/* <div>
          <div className="my-2 flex cursor-default flex mb-1">
            <p className="flex-1 text-sm font-normal float-left align-text-top">
              Enable All
            </p>

            <Checkbox
              checked={parametersContext.selectAllModels}
              onCheckedChange={(val: boolean) => {
                setModelsStateContext(
                  modelsStateContext.map((modelState: any) => {
                    modelState.enabled = val
                    modelState.selected = false
                    return modelState
                  })
                )

                setParametersContext({
                  ...parametersContext,
                  selectAllModels: val,
                })
              }}
              className="float-right"
            />
          </div>
        </div> */}
        {/* <div className="my-2 flex flex-row border-slate-300 border p-2 rounded">
          <div className="flex items-center">
            <Filter size={18} />
          </div>

          <div className="ml-2 flex-1 mr-2">
            <input
              className="outline-0 w-[100%]"
              value={modelSearchValue}
              onChange={(event) => {
                setModelSearchValue(event.target.value)
              }}
              placeholder="Model Name"
            />
          </div>
        </div> */}
        <div>
          <ul>
            {modelsStateContext.filter((modelState: any) =>
                !modelState.tag? false : !modelTypeFilter(modelState.name.split(":")[1])? false: true )
              .map(generate_card)}
          </ul>
        </div>
      </>
    )
  }

  const generate_header = () => {
    if (!showModelDropdown)
      return (
        <div className="flex mb-2">
          <span className="cursor-default flex-1 flow-root inline-block align-middle">
            <p className="text-sm font-medium float-left align-text-top">
              Parameters
            </p>
          </span>
          <Tooltip delayDuration={300} skipDelayDuration={150}>
            <TooltipTrigger asChild>
              <div
                onClick={() => {
                  setParametersContext({
                    ...parametersContext,
                    showParametersTable: !parametersContext.showParametersTable,
                  })
                }}
                className={`mx-1 cursor-pointer flex justify-center items-center w-[24px] h-[24px] rounded-full border-[1px] border-slate-200 select-none ${
                parametersContext.showParametersTable
                  ? "text-white bg-slate-700"
                  : "hover:text-white hover:bg-slate-700 text-slate-600 bg-white"
                  }`}
              >
                <BarChart2 size={18} />
              </div>
            </TooltipTrigger>
            <TooltipContent side={"bottom"}>
              <p>Show Parameters for all models</p>
            </TooltipContent>
          </Tooltip>
        </div>
      )

    const selectedModel = modelsStateContext.find((modelState) => modelState.selected)
    
    console.log("modelsStateContext", modelsStateContext);
    
    const getDisplayName = (model_key) => {
      const modelkey = model_key.split(":")[1]
      
      switch (modelkey) {
        case "gpt4_new":
          return "GPT-4"
          break;
        case "gpt-35-turbo-new":
          return "GPT-35-turbo"
          break;
        case "gpt-4-32k_2":
          return "GPT-4-32k"
          break;
      
        default:
          return ""
          break;
      }
    }
    // Model type filters the type of model from the modelsStateContext.
    return (
      <div className="">
        <div className="mb-2" >
          <span className="flow-root inline-block align-middle" style={{marginBottom:'1rem'}}
          >
            <p className="text-sm font-medium float-left align-text-top" style={{marginBottom:'0px', fontWeight: 'normal'}}>
              Model Type
            </p>
            <Select
              value={modelType || ""}
              onValueChange={(value) => {
                setModelType(value)
              }}>
              <SelectTrigger
                className="w-full"
                onKeyDown={(e) => {
                  if (e.code === "Enter" && e.metaKey) {
                    e.preventDefault()
                  }
                }}
              >
                <SelectValue style={{ width: '200px'}} placeholder="Select the task type" value={modelType} />
                <SelectContent
                  onKeyDown={(e) => {
                    if (e.code === "Enter" && e.metaKey) {
                      e.preventDefault()
                    }
                  }}
                >
                  <SelectGroup>
                    {Object.entries(modelTypes).map(([type, tasks]) => {
                      return (
                        <div key={type}>
                          <SelectItem
                            value={type}
                            title={type}
                            onKeyDown={(e) => {
                              if (e.code === "Enter" && e.metaKey) {
                                e.preventDefault()
                              }
                            }}
                          >{type?.length > 22 ? `${type.slice(0, 22)}...` : type}</SelectItem>
                        </div>)
                    }
                    )
                    }

                  </SelectGroup>
                </SelectContent>
              </SelectTrigger>
            </Select>
          </span>

          <span className="flow-root inline-block align-middle">
            <p className="text-sm font-medium float-left align-text-top" style={{marginBottom:'0px', fontWeight: 'normal'}}>
              Model
            </p>
            {modelType!=""&&<Select 
            value={selectedModel?.name || null}
              disabled={false}
            onValueChange={(value) => {
              setModelsStateContext(
                  modelsStateContext.map((model) => ({ ...model, selected: (model.name === value) ? true : false }))
              )
              const modelParameters = modelsStateContext.find((model) => model.name === value).parameters

                setParametersContext({
                  temperature: modelParameters.temperature || parametersContext.temperature,
                  max_new_tokens: modelParameters.max_new_tokens || parametersContext.max_new_tokens,
                  topP: modelParameters.topP || parametersContext.topP,
                  topK: modelParameters.topK || parametersContext.topK,
                  frequencyPenalty: modelParameters.frequencyPenalty || parametersContext.frequencyPenalty,
                  presencePenalty: modelParameters.presencePenalty || parametersContext.presencePenalty,
                  repetitionPenalty: modelParameters.repetitionPenalty || parametersContext.repetitionPenalty,
                  stopSequences: modelParameters.stopSequences || parametersContext.stopSequences
                })
            }}
          >
            <SelectTrigger
              className="w-full"
              onKeyDown={(e) => {
                if (e.code === "Enter" && e.metaKey) {
                  e.preventDefault()
                }
              }}
            >
              <SelectValue placeholder="Select a Model" value={selectedModel?.name || null}/>
            </SelectTrigger>
            <SelectContent
              onKeyDown={(e) => {
                if (e.code === "Enter" && e.metaKey) {
                  e.preventDefault()
                }
              }}
            >
              {Object.entries(modelProviders).map(([provider, prettyName]) => (
                <SelectGroup key={provider}>
                  {Object.entries(modelsContext)
                      .filter(([key]) => key.split(":")[0] === provider && modelTypeFilter(key.split(":")[1]))
                    .map(([model_key, _], index) => {
                      if (modelsContext[model_key]) {
                        return (
                          <div key={model_key}>
                            <SelectLabel hidden={index != 0} style={{ fontWeight: 'bold', color: '#42619d' }}>
                              {prettyName}
                            </SelectLabel>
                            <SelectItem
                              value={model_key}
                              onKeyDown={(e) => {
                                if (e.code === "Enter" && e.metaKey) {
                                  e.preventDefault()
                                }
                              }}
                            >
                              {provider!=='openai'?model_key.split(":")[1]:`${model_key.split(":")[1]} (${getDisplayName(model_key)})`}
                            </SelectItem>
                          </div>
                        )
                      }
                    })}
                </SelectGroup>
              ))}
            </SelectContent>
            </Select>}
            {/* display a empty tag if modelType isn't selected */}
            {modelType == "" &&
              <Select value="Please select type" disabled={true}>
                <SelectTrigger className="w-full">
                <SelectValue placeholder="Select a Model" value={selectedModel?.name || null}/>
                </SelectTrigger>
          </Select>
            }
            
          </span>

        </div>
      </div>
    )
  }

  const generate_show_probabilities = () => {
    const selectedModel = modelsStateContext.find((modelState) => modelState.selected)
    if (!selectedModel || !selectedModel.capabilities || !selectedModel.capabilities.includes("logprobs"))
      return null

    return (
      <Tooltip delayDuration={300} skipDelayDuration={150}>
        <TooltipTrigger asChild>
          <div className="cursor-default flex justify-between align-middle inline-block align-middle mb-1">
            <p className="text-sm font-normal float-left align-text-top">
              Show Probabilities
            </p>
            <Checkbox
              name="show-probabilities"
              className="float-right self-center"
              checked={parametersContext.showProbabilities}
              onCheckedChange={(val: boolean) => {
                setParametersContext({
                  ...parametersContext,
                  showProbabilities: val,
                })
              }}
            />
          </div>
        </TooltipTrigger>
        <TooltipContent side={isLg ? "left" : "bottom"}>
          <p>
            When enabled hover over generated words <br /> to see how likely a
            token was to be generated,
            <br /> if the model supports it.
          </p>
        </TooltipContent>
      </Tooltip>
    )
  }

  return (
    <div className="flex flex-col max-h-[100%] pt-4 sm:pt-4 md:pt-[0px] lg:pt-[0px]">
      <div className="mb-2">
        {generate_header()}
      </div>
      <div className="flex flex-col gap-y-3">
        {generate_parameters_sliders()}

        {/* <MultiSelect
          onValueChange={(value: any) => {
            setModelsStateContext(
              modelsStateContext.map((modelState: any) => {
                if (
                  modelState.parameters.stopSequences &&
                  (number_of_models_selected === 0 || modelState.selected)
                )
                  modelState.parameters.stopSequences = value

                return modelState
              })
            )
            setParametersContext({
              ...parametersContext,
              ["stopSequences"]: value,
            })
          }}
          defaultOptions={parametersContext.stopSequences}
          tooltipContent={
            <>
              <p>
                Up to four sequences where the API will stop <br /> generating
                further tokens. The returned text <br />
                will not contain the stop sequence.
              </p>
            </>
          }
        /> */}

        {generate_show_probabilities()}

        {/* <Tooltip delayDuration={300} skipDelayDuration={150}>
          <TooltipTrigger asChild>
            <div className="cursor-default flex justify-between align-middle inline-block align-middle mb-1">
              <p className="text-sm font-normal float-left align-text-top">
                Highlight Models
              </p>
              <Checkbox
                name="highlight-models"
                className="float-right self-center"
                checked={parametersContext.highlightModels}
                onCheckedChange={(val: boolean) => {
                  setParametersContext({
                    ...parametersContext,
                    highlightModels: val,
                  })
                }}
              />
            </div>
          </TooltipTrigger>
          <TooltipContent side={isLg ? "left" : "bottom"}>
            <p>Disable model specific text highlights</p>
          </TooltipContent>
        </Tooltip> */}
      </div>

      {generate_list()}
    </div>
  )
}

export default ParametersSidePanel