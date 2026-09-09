# SIH26003 - Dedicated Multilingual Support Engine (5 Languages)

This directory contains the complete **Multilingual Localization System** built specifically for **SIH Problem Statement SIH26003** (*Ministry of Development of North Eastern Region - MDoNER*) for elderly dementia patients across North Eastern India.

---

## 🌐 Supported Languages

1. **English (`en`)**: Primary global language & clinical standard.
2. **Hindi (`hi`)**: हिन्दी - Primary regional fallback language.
3. **Assamese (`as`)**: অসমীয়া - Native language of Assam & NER Brahmaputra valley.
4. **Mizo (`lus`)**: Mizo ṭawng - Native language of Mizoram.
5. **Khasi (`kha`)**: Ka Ktien Khasi - Native language of Meghalaya (Khasi & Jaintia Hills).

---

## 📁 Directory Structure

```
multilingual_support/
├── README.md                           # Documentation & Language Specs
├── multilingual_engine.py              # Standalone Python localization & voice synthesis engine
├── l10n_arb/                           # Flutter ARB Internationalization Files
│   ├── app_en.arb                      # English ARB
│   ├── app_hi.arb                      # Hindi ARB
│   ├── app_as.arb                      # Assamese ARB
│   ├── app_lus.arb                     # Mizo ARB
│   └── app_kha.arb                     # Khasi ARB
└── json_language_packs/                # Standalone JSON Dictionaries for REST APIs & Web Demo
    ├── master_multilingual_dictionary.json
    ├── english.json
    ├── hindi.json
    ├── assamese.json
    ├── mizo.json
    └── khasi.json
```

---

## 🚀 Quick Execution Test

To test multilingual text & voice prompt output across all 5 languages in terminal:

```bash
python multilingual_support/multilingual_engine.py
```
