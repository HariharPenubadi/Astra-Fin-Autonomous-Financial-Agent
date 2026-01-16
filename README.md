# ASTRA: Autonomous Financial Intelligence Platform

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/yourusername/astra-fin/actions)
[![Tech Stack](https://img.shields.io/badge/stack-Python_|_React_|_Docker_|_Unsloth-blue)](https://fastapi.tiangolo.com/)
[![AI Engine](https://img.shields.io/badge/AI-Custom_Fine_Tuned_Llama_3-purple)](https://ollama.com/)
[![Architecture](https://img.shields.io/badge/architecture-Microservices-orange)](https://docs.docker.com/compose/)

> **A privacy-first, deterministic AI Financial Advisor agent orchestrated via a microservices architecture. Powered by a custom fine-tuned Llama-3 model ("astra-fin"), features real-time reasoning observability, self-correcting memory, and formally verified logic pipelines.**

---

##  The Engineering Challenge
Standard AI wrappers suffer from two critical failures: **Hallucination** and **Statelessness**. 

I engineered **ASTRA** to solve these by moving beyond simple RAG (Retrieval-Augmented Generation) to an **Agentic Workflow**:

**Domain Specialization:** Instead of a generic model, I fine-tuned Llama-3 8B on 10,000+ financial QA pairs to align its internal weights with fiduciary-style reasoning.

**Determinism:** Implementing a strict Planner/Executor architecture to enforce logic boundaries.

**Observability:** Building a reactive UI that exposes the agent's internal state changes (Intent/Memory) in real-time.

**CI/CD Reliability:** Decoupling logic tests from inference using unittest.mock, allowing the intelligence engine to be verified on non-GPU CI environments.

---

##  Model Engineering (FINE-TUNING PIPELINE)

Unlike generic assistants, ASTRA runs on "astra-fin-gguf", a model I explicitly trained for financial accuracy.
* **Base Model:** Llama-3 8B Instruct (Unsloth optimized)
* **Technique:** QLoRA (Quantized Low-Rank Adaptation)
* **Parameters:** Rank (r)=16, Alpha=16, 4-bit Quantization
* **Dataset:** virattt/financial-qa-10k (High-quality financial instruction pairs)
* **MLOps Workflow:**
    * Training: Optimized via Unsloth for 2x faster backpropagation.
    * Quantization: Converted to GGUF (q4_k_m) format to enable high-performance inference on consumer hardware (MacBook M-Series).
    * Registry: Adapters pushed to Hugging Face (Harihar-p/astra-fin-lora) for version control.

---
## Microservices Breakdown
**Frontend** - &ensp;React, Tailwind, Nginx ("Glass Box" interface visualizing the agent's reasoning steps.)

**Backend** - &ensp;Python, FastAPI, LangGraph (State management, routing logic, and tool execution.)

**Inference Engine Stack** - &ensp;Custom Fine-Tuned Model (Astra-Fin) (Domain-specific financial reasoning running locally via Ollama.)

**Memory** - &ensp;Qdrant (Vector DB) (Semantic persistence of user risk profiles and history.)

**Search** - &ensp;SearxNG (Private, self-hosted meta-search engine for real-time market data.)

---

## Key Features

* "Glass Box" Observability Unlike black-box chat interfaces, ASTRA visualizes its cognitive process. The frontend subscribes to the backend's reasoning stream to display:
    * Planner State: Shows real-time intent classification (e.g., INVESTMENT_SETUP, MARKET_ANALYSIS).
    * Live Memory: Visualizes updates to the user's Semantic Profile (Risk Tolerance, Budget, Horizon) as they happen.

* Formally Verified Intelligence The "Brain" is not just prompted; it is tested.
    * Unit Tests: Pytest suite verifies the Intent Router and Profile Extractor.
    * Mocking: CI pipeline uses unittest.mock to simulate LLM responses, ensuring logic validity without requiring GPUs in the build environment.

* Local-First Privacy
    * Runs 100% offline (after Docker build).
    * Financial data never leaves the user's infrastructure.
    * Uses the custom "astra-fin" GGUF model for low-latency, private inference.

---

## Installation & Setup

**Prerequisites**

* Docker Desktop
* Ollama (running locally)


    1. Start the LLM Ensure Ollama is running and accessible to Docker: Command: OLLAMA_HOST=0.0.0.0 ollama serve

    2. Clone & Launch Command: git clone https://github.com/HariharPenubadi/Astra-Fin-Agent.git Command: cd astra-fin-agent Command: docker-compose up --build

    3. Access the Platform 
    * Frontend UI: http://localhost:3000
    * Backend API Docs: http://localhost:8000/docs
    * Vector DB Dashboard: http://localhost:6333/dashboard

---

## Testing Strategy

ASTRA utilizes a bifurcated testing strategy to ensure reliability:

* **Unit Testing (Logic)** Verifies the Python logic without invoking the heavy LLM. Command: pytest tests/test_brain.py -v

* **Integration Testing (Flow)** Verifies the end-to-end conversation capability with the real local LLM. Command: pytest tests/test_flow.py -v

---

## Roadmap

**Phase 1:** Core Logic & Memory (LangGraph + Qdrant)

**Phase 2:** Model Fine-Tuning (Unsloth QLoRA) 

**Phase 3:** UI (React + FastAPI Streaming) 

**Phase 4:** Docker Containerization 

**Phase 5:** CI/CD with LLM Mocking 

---
