![](https://img.shields.io/github/license/Infosys/Infosys-Transformer-Foundry)
![](https://img.shields.io/github/issues/Infosys/Infosys-Transformer-Foundry)
![](https://img.shields.io/github/issues-closed/Infosys/Infosys-Transformer-Foundry)
![](https://img.shields.io/badge/Angular-12-blue)
![](https://img.shields.io/badge/Python-3.9-purple)
![](https://img.shields.io/github/forks/Infosys/Infosys-Transformer-Foundry)
![](https://img.shields.io/github/stars/Infosys/Infosys-Transformer-Foundry)
![](https://img.shields.io/github/last-commit/Infosys/Infosys-Transformer-Foundry)

# Infosys Transformer Foundry

## Overview

Infosys Transformer Foundry solution provides buildings blocks for managing LLM Ops and model life cycle management such as model selection, finetuning, benchmarking, deployment at scale along with data pipelines.

![Features offered](docs/images/features.png)

## Features v1.1

- [Model Zoo](docs/model_zoo.md): Curated list of open source models along with their metadata, lifecycle status and model tagging.
- [Leaderboard](docs/leaderboard.md): LLM leaderboard for customer data (text, embedding and code) on public/private models for efficient selection of models.
- [Benchmark tool](docs/benchmark.md): Allows benchmarking of fine-tuned or open source models.
- [Data Pipelines](docs/data_pipelines.md): Allow users to create custom data processing workflows for their models. 
- [Fine Tuning](docs/fine_tuning.md): User can fine tune a model against custom datasets for tailored results.
- [Model Deployment](docs/model_deployment.md): Facilitate deployment of curated or fine-tuned models and create access points.
- [Model Playground](docs/model_playground.md): Allows users to test the performance of different models available in the model zoo.
- [RAG Playground](docs/rag_playground.md): User can ingest documents in real time and leverage RAG for inferencing from them.
- Dataset Registration: Users have the ability to save datasets, they can then use them during finetuning or benchmarking jobs.

## Hardware & Software Requirements

Find the hardware and software requirements [here](docs/requirements.md)

## Installation

### Docker

<b>a. Clone the GitHub repository</b>

```
git clone -b < branch and Repo url>
```

<b>b. Build docker container for each component</b>

Navigate to each component folder within the repository and build the corresponding Docker image using the following command:

```dos
cd <component_folder>
docker build -t ${DOCKER_REPO}/<image_name>
```

<b>c. Run the Docker Container</b>

```dos
docker-compose -f docker-compose.yaml up
```

## Usage and Examples

[Benchmark Evaluation](docs/benchmark_evaluation.md)

## Reporting problems, asking questions

We appreciate your feedbacks, questions or bug reporting regarding this project. When posting issues in GitHub, ensure the posted examples follow the guidelines below:

<b>Minimal</b>: Provide the smallest possible code snippet that still reproduces the problem.

<b>Complete</b>: Include all necessary information (code, configuration, etc.) for someone else to replicate the issue.

<b>Reproducible</b>: Test your provided code to confirm it consistently reproduces the problem.
