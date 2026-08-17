# Summary: Grounding vs. Plain Prompting

**Project:** DocMind AI — RAG Mini-Project (Neurofive Solutions Internship, Week 3)

## What was tested

The document `Generative_AI_and_Prompt_Engineering_Notes.pdf` was uploaded and ingested into DocMind AI. Five questions requiring the model to read the actual document content were asked, covering specific facts, exact numbers, and terminology that only appear in the source material:

1. Why is RAG needed instead of just pasting the whole document into the prompt?
2. What happened when the enum field came back as null in the structured output test, and how was it fixed?
3. What are the four stages of a RAG pipeline?
4. In the internal few-shot vs. zero-shot test, how many out of 10 messages were classified correctly?
5. What is the Transformer architecture and when was it introduced?
6. What is this document about?

## Results with RAG grounding

Every answer matched the document exactly, with correct source page numbers cited:

- Correctly named the four RAG stages (chunking, embedding, retrieval, generation)
- Correctly reported the exact test numbers (zero-shot: 8/10, few-shot: 10/10)
- Correctly described the enum-null bug and its exact fix (the added rule about inferring `delivery_or_pickup` from context)
- Correctly cited the Transformer's 2017 paper ("Attention Is All You Need")

No hallucinated content was observed in any of the five+ answers — every claim traced back to a specific page in the source PDF.

## How grounding changed answer quality vs. a plain prompt

Without RAG, a plain prompt to the LLM would rely entirely on the model's training data and general knowledge. For general/public facts (like the Transformer paper), a plain prompt might still answer correctly by coincidence, since that's widely known information the model was trained on. But for anything specific to *this* document — the internal test's exact 8/10 vs. 10/10 numbers, the specific enum-null bug and its fix, or document-specific terminology — a plain prompt has no way to know these details and would either refuse, guess, or hallucinate a plausible-sounding but incorrect answer.

Grounding via RAG solved this by retrieving the exact relevant chunks from the document before generation, so the model's answer was constrained to only what was actually written — making the answers both **verifiable** (via cited source pages) and **accurate** for private/custom content that no general-purpose LLM could otherwise know.