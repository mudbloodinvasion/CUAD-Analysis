# 📄 Contract Risk Analysis System

An AI-powered commercial contract analysis and risk assessment system built using the CUAD dataset, Sentence Transformers, FAISS, Gemini, and Streamlit.
The system extracts contract text, retrieves relevant clauses using semantic search, analyzes them using Gemini, assigns baseline risk levels, generates a contract-level risk report, and allows users to ask questions about the contract.

# 🚀 Project Overview

Commercial contracts are often lengthy and contain important clauses related to liability, termination, exclusivity, non-compete obligations, licensing, assignment, audit rights, and other legal commitments.
Manually reviewing these contracts can be time-consuming and difficult to scale.
This project aims to provide an AI-assisted workflow for:
- Extracting text from contracts
- Splitting contracts into manageable chunks
- Finding relevant clauses using semantic search
- Classifying clauses according to the CUAD taxonomy
- Extracting supporting evidence
- Generating clause-level explanations
- Assigning baseline risk levels
- Generating an overall contract risk report
- Answering natural-language questions about contracts

# System Architecture 

                 Commercial Contract
                         │
                         ▼
                  PDF / TXT Upload
                         │
                         ▼
              Document Text Extraction
                     (pypdf)
                         │
                         ▼
                   Text Chunking
                         │
                         ▼
              Sentence Transformer Embeddings
                         │
                         ▼
                   FAISS Index
                         │
                         ▼
                Semantic Retrieval
                         │
                         ▼
                    Gemini LLM
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
        Clause Analysis  Contract   Question
                         Report     Answering
              │          │          │
              └──────────┼──────────┘
                         ▼
                  Risk Analysis
                         │
                         ▼
                  Streamlit UI

# 📚 CUAD Dataset

This project uses the Contract Understanding Atticus Dataset (CUAD) as the foundation for contract clause classification.
CUAD contains:
- 510 commercial contracts
- More than 13,000 clause annotations
- 41 clause categories
Some of the categories include:
- Document Name
- Parties
- Agreement Date
- Effective Date
- Governing Law
- Non-Compete
- Exclusivity
- Uncapped Liability
- Liquidated Damages
- Anti-Assignment
- Change Of Control
- Termination For Convenience
- Minimum Commitment
- Volume Restriction
- Audit Rights
- Insurance
- Source Code Escrow
- Irrevocable Or Perpetual License
- Unlimited/All-You-Can-Eat-License
The CUAD taxonomy provides the clause categories used by the system for structured analysis.

# Working of System 
1. Document Upload through Streamlit interface
2. Document Extraction using pypdf. The system extracts text page-by-page and keeps information about:
- Total pages
- Pages containing text
- Pages without extractable text
- Character counts
- Extracted page content
This also helps identify contracts where text extraction may be problematic.
3. Text Chunking - chunk_size: 1200 , chunk_overlap: 150
4. Semantic Embeddings using sentence-transformers/all-MiniLM-L6-v2
5. FAISS Vector Search using FAISS IndexFlatIP
6. Clause Analysis with Gemini where it determines whether each requested category is present and returns:
- Clause category
- Presence
- Supporting evidence
- Summary
- Confidence score
7. Can ask questions

# Tech Stack
Python , Streamlit , FAISS , Transformers , Numpy , PYPDF

# Installation 
git clone <your-repository-url>
cd "CUAD ANALYSIS"

Install dependency 
pip install -r requirement.txt

# Challenges Overcomed 
1. An LLM could potentially make unsupported claims.
Solution
The system instructs Gemini to:
- Use only retrieved contract passages
- Provide supporting evidence
- Avoid inventing information
- Return a confidence score

2.Legal clauses can be written in many different ways.A keyword search may fail when the exact search term is not present.
Solution 
Sentence Transformer embeddings allow the system to perform semantic similarity search.

3.Commercial contracts can contain hundreds of pages, making it impractical to send the entire document directly to an LLM.
Solution 
The system uses: Chunking + Embedding + FAISS Retrieval. Only relevant passages are provided to Gemini.

# Limitation
1. OCR Is Not Currently Implemented
2. The current High/Medium/Low mapping is a project-defined baseline and should not be treated as professional legal risk scoring.
3. Semantic retrieval may occasionally miss relevant clauses in very long or complex contracts.

# Advantages 
1. The system searches by meaning rather than only matching keywords.
2. Detected clauses include supporting contract passages.
3. JSON-based responses make the results easier to process and display.
4. The system uses an established commercial contract clause taxonomy.
5. The application goes beyond individual clauses and produces an overall contract assessment.
6. Users can ask natural-language questions about the uploaded contract

# Disclaimer 
ONly for Educational Purposes .
