# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

"""DRIFT Search prompts."""

DRIFT_LOCAL_SYSTEM_PROMPT = """
---Role---
You are a helpful assistant responding to questions about data in the provided tables.

---Goal---
Your task is to summarize the input data tables to answer the user's question in the specified response length and format. Incorporate relevant general knowledge where appropriate.

- Support points with references from the data:
  "This is an example supported by data [Data: <dataset name> (record ids); <dataset name> (record ids)]."
- Include at most 5 record ids per reference. If there are more, append "+more."
  Example: "Data: Sources (1, 2, 3, 4, 5+more)."

If data is unavailable to answer the query, state: "Data not available to answer the query."

---Response Format---
1. Provide a response in markdown format: {response_type}.
2. Output a JSON with:
   - `response`: Markdown-formatted answer.
   - `score`: Integer (0-100) rating how well the response answers the research question `{global_query}`.
   - `follow_up_queries`: List of up to {num_followups} additional questions for further exploration.

---Data Tables---
{context_data}

---Instructions---
1. Focus on the most relevant data, especially from the Sources table.
2. Use all relevant information but avoid exceeding token limits.
3. Maintain JSON output formatting strictly.

"""


DRIFT_REDUCE_PROMPT = """
---Role---

You are a helpful assistant responding to questions about data in the reports provided.

---Goal---

Generate a response of the target length and format that responds to the user's question, summarizing all information in the input reports appropriate for the response length and format, and incorporating any relevant general knowledge while being as specific, accurate and concise as possible.

If you don't know the answer, just say so. Do not make anything up.

Points supported by data should list their data references as follows:

"This is an example sentence supported by multiple data references [Data: <dataset name> (record ids); <dataset name> (record ids)]."

Do not list more than 5 record ids in a single reference. Instead, list the top 5 most relevant record ids and add "+more" to indicate that there are more.

For example:

"Person X is the owner of Company Y and subject to many allegations of wrongdoing [Data: Sources (1, 5, 15)]."

Do not include information where the supporting evidence for it is not provided.

If you decide to use general knowledge, you should add a delimiter stating that the information is not supported by the data tables. For example:

"Person X is the owner of Company Y and subject to many allegations of wrongdoing. [Data: General Knowledge (href)]"

---Data Reports---

{context_data}

---Target response length and format---

Multiple paragraphs


---Goal---

Generate a response of the target length and format that responds to the user's question, summarizing all information in the input reports appropriate for the response length and format, and incorporating any relevant general knowledge while being as specific, accurate and concise as possible.

If you don't know the answer, just say so. Do not make anything up.

Points supported by data should list their data references as follows:

"This is an example sentence supported by multiple data references [Data: <dataset name> (record ids); <dataset name> (record ids)]."

Do not list more than 5 record ids in a single reference. Instead, list the top 5 most relevant record ids and add "+more" to indicate that there are more.

For example:

"Person X is the owner of Company Y and subject to many allegations of wrongdoing [Data: Sources (1, 5, 15)]."

Do not include information where the supporting evidence for it is not provided.

If you decide to use general knowledge, you should add a delimiter stating that the information is not supported by the data tables. For example:

"Person X is the owner of Company Y and subject to many allegations of wrongdoing. [Data: General Knowledge (href)]".

Add sections and commentary to the response as appropriate for the length and format. Style the response in markdown. Now answer the following query using the data above:

{query}

"""


DRIFT_PRIMER_PROMPT = """You are a helpful agent designed to reason over a knowledge graph in response to a user query. 
This is a unique knowledge graph where edges are freeform text rather than verb operators. You will begin your reasoning looking at a summary of the content of the most relevant communities and will provide:

1. score: How well the intermediate answer addresses the query. A score of 0 indicates a poor, unfocused answer, while a score of 100 indicates a highly focused, relevant answer that addresses the query in its entirety.

2. intermediate_answer: Follow below instructions strictly while generating the answer:
-Answer question only from the given CONTEXT.
-Generate the response in paragraph format using all available information from the input data tables. Do not limit your response to top entities only. Do not provide unnecessary information, answer the query as it is
-Do not generate or extrapolate numbers or dates.
-Do not generate any new number based on the CONTEXT.
-Generate response only if information required for user's query is present in CONTEXT.
-ONLY answer the query with data that you are completely sure is correct.
-If the data is not available to answer the query, respond with: "Data not available to answer the query."

3. follow_up_queries: A list of follow-up queries that could be asked to further explore the topic. These should be formatted as a list of strings. Generate at least {num_followups} good follow-up queries, only if data is available in the summaries. If no data is available in summaries, generate the follow ups to be the original query. You may rephrase the original query in this case.

Use only the data provided in the community summaries CONTEXT to generate the intermediate answer and follow-up queries.

If the data is not available in the provided summaries, respond with "Data not available to answer the query" for the intermediate answer, set the score to 0, and do not generate any follow-up queries.

For the query:

{query}

The top-ranked community summaries as CONTEXT:

{community_reports}      


While forming intermediate answers do not include information not present in CONTEXT of community summaries. Do not include any entity, company or person not mentioned in CONTEXT.
Provide the intermediate answer, and all scores in JSON format following:

{{'intermediate_answer': str,
'score': int,
'follow_up_queries': List[str]}}

Begin:
"""

DRIFT_DECOMPOSE_PROMPT_SYSTEM = """You are tasked with breaking down a complex multi-part query into independent sub-queries. Each sub-query must be rephrased as a complete, independent question that does not reference other sub-queries explicitly.
The answers from sub-queries will be assumed to be appended with answers of other sub-queries.

For each sub-query, return a dictionary where:
- Each key is the rephrased sub-query.
- Each value is a list of entity types applicable to the sub-query, indicating whether the current sub-query falls under those entity types.

Ensure the response follows the format where:
- Sub-queries are independent.
- Entity types must be selected from the ENTITY_TYPES list.
- Each sub-query should contain at least two relevant entity types.
- The sub-queries, when combined, must collectively cover all the entity types required in the user's original query.

"""
DRIFT_DECOMPOSE_PROMPT_ENTITY_TYPES = """
['ORGANIZATION', 'THEME', 'COMPANY STAGE', 'INVESTMENT STAGE', 'ROLE', 'GEO', 'PERSON', 'MARKET SEGMENT', 'FINANCIALS', 'GENDER', 'EDUCATIONAL INSTITUTION', 'TITLE']
"""

DRIFT_DECOMPOSE_PROMPT_USER = """Break down the following query into independent sub-queries and output the result as a dictionary. Each dictionary key should be the sub-query, and the corresponding value should be a list of up to two entity types relevant to the sub-query. Ensure:
- Each sub-query contains a maximum of two entity types.
- All the entity types mentioned in the original query are distributed across the sub-queries.
- The sub-queries are rephrased as independent, complete questions.

Query:
"""