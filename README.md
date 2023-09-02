# AfyaMumBot - Personalized Pregnancy Support Chatbot

## Introduction

AfyaMumBot is a Whatsapp-based AI-powered chatbot system designed to offer personalized information and support to expectant mothers throughout their pregnancy journey. It leverages advanced Generative AI models to provide accurate and helpful responses to user inquiries related to obstetrics and gynecology. This document outlines the structure, purpose, and the selection of Generative AI models for AfyaMumBot.

## Structure

The AfyaMumBot system consists of the following key components:

### Generative AI Models:

- **Llama 2 Model**: This model is one of the primary Generative AI models used within AfyaMumBot.
- **GPT-3.5 Model**: Another prominent Generative AI model employed for generating responses.

### Langchain and Instruction Embeddings:

- The system uses Langchain to create a conversational retrieval QA chain.
- Instruction Embeddings are utilized to convert the extensive book on obstetrics and gynecology diagnosis and treatment into embeddings.

### Document Repository:

- A document with comprehensive information on obstetrics and gynecology diagnosis and treatment serves as the knowledge base.
- The embeddings generated from this document are stored in a FAISS (Facebook AI Similarity Search) DB vector store.

### Response Generation:

- When a user asks a question, the system performs a similarity search on the vector store to find relevant document chunks.
- These relevant document chunks, along with the user's query, are passed as a prompt to the Generative AI models (GPT-3.5 LLM or Llama 2) for response generation.

## Purpose

The primary purpose of AfyaMumBot is to provide expectant mothers with:

- **Personalized Information**: The bot offers tailored information and advice based on the user's specific queries and pregnancy-related concerns.

- **Supportive Conversations**: It engages users in natural, human-like conversations, making them feel more comfortable and supported during their pregnancy journey.

- **Access to Medical Knowledge**: AfyaMumBot leverages its knowledge base in obstetrics and gynecology to provide accurate and up-to-date medical information.

- **Quick Responses**: The use of Generative AI models ensures that users receive timely and relevant responses to their questions.

## How Generative AI Models Are Chosen

The choice of Generative AI models for AfyaMumBot is driven by the need for high-quality, context-aware responses. The following considerations led to the selection of the models:

- **Performance**: Both Llama 2 and GPT-3.5 are known for their exceptional performance in natural language understanding and generation tasks.

- **Response Quality**: Extensive testing and evaluation showed that GPT-3.5 LLM provides superior response quality compared to individual models.

- **Adaptability**: These models can be fine-tuned and adapted to the specific domain of obstetrics and gynecology, making them suitable for AfyaMumBot's purposes.

- **Efficiency**: Generative AI models offer quick and automated responses, ensuring users receive information promptly.

In summary, AfyaMumBot's choice of Generative AI models, including GPT-3.5 LLM, is driven by a commitment to providing expectant mothers with accurate, personalized, and timely information and support throughout their pregnancy journey.
