# Follow-Up Mechanism (CRITICAL)

When interacting with NotebookLM via the `notebooklm_query` tool, NotebookLM behaves differently than a typical conversational AI. Because it strictly grounds its answers **only** in the provided documents, it may occasionally provide an incomplete answer or require iterative refinements to extract all relevant details from large source files.

## Required Claude Behavior

To ensure the user receives the highest quality answer when you use `notebooklm_query`, you must:

1. **STOP & ANALYZE**
   Do not immediately parrot NotebookLM's first response back to the user. Instead, read the response and compare it to the user's *original intent*.

2. **IDENTIFY GAPS**
   Determine if the retrieved response fully answers the user's question, or if there is clearly more information available in the documents that wasn't included in the initial summary.

3. **ASK FOLLOW-UP QUESTIONS**
   If the answer seems incomplete or if NotebookLM indicates there's more information (e.g., stopping abruptly or summarizing broadly), proactively ask follow-up questions using `notebooklm_query` again. 
   
   Example follow up queries:
   - "Please elaborate on [Specific Topic from first answer]."
   - "Are there any other sections mentioning [User's Keyword]?"

4. **REPEAT**
   Continue querying different angles of the question until you are confident you've extracted all necessary context from NotebookLM. (Keep this to a reasonable limit, around 2-3 queries maximum, to avoid endless loops).

5. **SYNTHESIZE**
   Finally, combine all the information you gathered across your multiple `notebooklm_query` tool calls into a single, comprehensive, properly formatted response for the user.

## Exception Handling
- If NotebookLM explicitly states that the documents **do not contain** the answer, inform the user immediately rather than blindly retrying.
- If NotebookLM throws an authentication or internal error, gracefully report this to the user and suggest they run `nlm login` if necessary.
