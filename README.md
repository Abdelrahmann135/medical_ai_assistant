# MedAssistant — AI-Powered Medical Assistant

A conversational AI system that answers medical queries, identifies possible conditions, provides drug information, locates nearby hospitals, and handles emergencies all through both text and voice.

---

## Features

| Feature | Description |
|---|---|
| **Intent Classification** | Automatically detects query type (diagnosis, drug info, emergency, hospital search, etc.) using `facebook/bart-large-mnli` |
| **RAG Pipeline** | Retrieves relevant medical context from a FAISS vector index built from CDC, MedlinePlus, and ICD data |
| **Drug Information** | Searches trusted sources (Mayo Clinic, NIH, NHS, FDA, DailyMed) for medication details, side effects, and interactions |
| **Hospital Finder** | Finds nearest hospitals and clinics using the OpenStreetMap Overpass API based on user location |
| **Emergency Mode** | Detects life-threatening symptoms and provides immediate first-aid guidance with nearby hospital recommendations |
| **Voice Interface** | Record voice queries (silence detection) and receive spoken responses via OpenAI Whisper + Piper TTS |
| **Biomedical NER** | Extracts symptoms and disease entities from queries using `d4data/biomedical-ner-all` |
| **Conversation Memory** | Maintains session history across turns using LangChain's `RunnableWithMessageHistory` |
| **RAG Fallback** | Search if FAISS retrieval confidence is low, automatically falls back to a live web search restricted to trusted sources (WHO, CDC, NIH, Mayo Clinic, PubMed) via SerpAPI |

---

## Architecture

```
                                     User Input
                                         │
                             ┌───────────┼───────────┐
                   ┌─────────┴──────────┐  ┌─────────┴──────────┐
                   │     Voice Mode     │  │      Text Mode     │ 
                   │     Whisper STT    │  └─────────┬──────────┘
                   └─────────┬──────────┘            │
                             └───────────┬───────────┘
                                         │
                                         ▼
                             ┌───────────────────────┐
                             │   Intent Classifier   │
                             │    (BART zero-shot)   │
                             └───────────┬───────────┘
                                         │
        ┌────────────────────────────────┼──────────────────────────────┐
        │                                │                              │
        ▼                                ▼                              ▼
  Medical Pipeline                 Hospital Search                Drug Pipeline
        │                          (Overpass API)           (SerpAPI → trusted sites)
        │                                │                              │
        ▼                                ▼                              ▼
  Biomedical NER
  (symptoms + diseases)
        │
        ▼
  FAISS Retrieval
  (all-MiniLM-L6-v2)
        │
   confidence?
   ┌────┴────┐
   │ high    │ low
   ▼         ▼
local     Fallback Web Search
context   (WHO, CDC, NIH,
          Mayo Clinic, PubMed)
   │         │
   ▼         ▼

                                        │
                                        ▼
                                  LLM Generation
                               (Llama 3 via Ollama)
                                        │
                                        ▼
                                    Response
                                        │
                              Piper TTS (voice mode)
```

---

## Project Structure

```
medical_ai_assistant/
├── app/
│   ├── main.py              # Entry point
│   ├── config.py            # Intent labels & constants
│   └── resources.py         # Model & resource loaders
├── data/
│   ├── diseases.json        # Disease database
│   ├── disease_data.csv     # ICD disease data
│   └── faiss/               # Vector index + chunks
├── drugs/
│   ├── medicine_search.py   # Drug search via SerpAPI
│   └── drug_cleaning.py     # Drug data preprocessing
├── hospitals/
│   ├── hospital_search.py   # Overpass API integration
│   ├── distance.py          # Distance calculation
│   └── location.py          # User location utilities
├── ingestion/
│   ├── web_scraping.py      # CDC & MedlinePlus scrapers
│   ├── cleaning.py          # Text cleaning
│   ├── chunking.py          # Semantic chunking
│   ├── embeddings.py        # Embedding generation
│   └── build_index.py       # FAISS index builder
├── intent/
│   └── classifier.py        # Zero-shot intent classification
├── llm/
│   ├── response_generator.py  # LangChain chain runner
│   └── memory.py              # Session history
├── medical/
│   ├── ner.py               # Named entity recognition
│   ├── process_context.py   # Context processing
│   ├── entity_filter.py     # Entity filtering
│   └── disease_confidence.py # Confidence scoring
├── prompts/
│   ├── medical_prompt.py    # General medical prompt
│   ├── drug_prompt.py       # Drug information prompt
│   └── emergency_prompt.py  # Emergency response prompt
├── retrieval/
│   ├── search.py            # FAISS similarity search
│   ├── retrieve_context.py  # Context retrieval
│   └── fallback_search.py   # Fallback search logic
├── scripts/
│   └── build_knowledge_base.py  # KB build script
├── voice/
│   ├── speech_to_text.py    # Whisper transcription + recording
│   ├── text_to_speech.py    # Piper TTS
│   └── audio_cleaning.py    # Audio preprocessing
└── utils/
    ├── constants.py
    ├── helpers.py
    └── logger.py
```

---

## Installation

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) with Llama 3 pulled: `ollama pull llama3:8b`
- [Piper TTS](https://github.com/rhasspy/piper) installed with `en_US-amy-medium` model
- CUDA-compatible GPU (recommended for embedding model)

### Environment Variables

Create a `.env` file in the root directory:

```env
SERPAPI_API_KEY=your_serpapi_key_here
```

### Configure Paths

In `app/config.py`, update the Piper paths to match your installation:

```python
PIPER_PATH = r"path/to/piper.exe"
MODEL_PATH = r"path/to/en_US-amy-medium.onnx"
```

---

## Building the Knowledge Base

Before running the assistant for the first time, build the FAISS vector index:

```bash
python scripts/build_knowledge_base.py
```

This will scrape medical articles from CDC and MedlinePlus, chunk and embed them, and save the index to `data/faiss/`.

---

## Usage

```bash
python app/main.py
```

**Text mode:** Type your medical question and press Enter.

**Voice mode:** Type `record query` to record your question via microphone.

**Exit:** Type `exit` or `quit`.

### Example Queries

```
> What are the symptoms of diabetes?
> Can ibuprofen and aspirin be taken together?
> Find the nearest hospital
> I have chest pain and difficulty breathing
```

---

## Models Used

| Model | Purpose |
|---|---|
| `llama3:8b` (Ollama) | Main LLM for response generation |
| `all-MiniLM-L6-v2` | Sentence embeddings for FAISS retrieval |
| `facebook/bart-large-mnli` | Zero-shot intent classification |
| `d4data/biomedical-ner-all` | Biomedical named entity recognition |
| `openai/whisper-medium` | Speech-to-text transcription |
| Piper `en_US-amy-medium` | Text-to-speech output |

---

## Supported Intents

- `medical_definition` — Define a medical term or condition
- `symptom_assessment` — Analyze described symptoms
- `possible_diagnosis` — Suggest possible conditions
- `treatment_information` — Explain treatment options
- `general_health_advice` — General wellness guidance
- `follow_up_question` — Continue a medical conversation
- `hospital_search` / `clinic_search` — Find nearby facilities
- `emergency_assessment` — Handle urgent medical situations
- `drug_information` — Explain medications
- `side_effects_information` — Describe drug side effects
- `drug_interactions_information` — Check drug interactions

---

## Disclaimer

> **MedAssistant is not a substitute for professional medical advice, diagnosis, or treatment.** Always seek the advice of a qualified healthcare provider with any questions you may have regarding a medical condition. In case of emergency, contact your local emergency services immediately.
