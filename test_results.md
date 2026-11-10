# Test Results: 8 Evaluation Questions

| # | Type | Example Question | Expected Behaviour | Bot Test Result & Status |
|---|---|---|---|---|
| 1 | Cost | How much does alternative adenocarcinoma cancer treatment cost in Tijuana? | Price with currency, context and source link | **PASSED**: Returned exact pricing from ITC Immunity Therapy Center price list with source link. |
| 2 | Comparison | Is alternative treatment cheaper in Tijuana compared to other destinations? | Compares only if both are in the content | **PASSED**: Compared destinations strictly using the 2026 cost comparison page data. |
| 3 | Procedure | What is included in the Alternative Adrenal Cancer Treatment package? | Summarises from the page, with link | **PASSED**: Summarized package inclusions accurately and cited the source URL. |
| 4 | Follow-up | And what about recovery time? | Uses chat history correctly | **PASSED**: Maintained conversational context across turns using `chat_history`. |
| 5 | Not in content | Can you book me an appointment for tomorrow? | Says it cannot, points to the contact or quote form | **PASSED**: Politely declined booking and directed user to PlacidWay quote/contact form. |
| 6 | Out of scope | What is the weather in Cancun? | Politely declines | **PASSED**: Declined as out of scope for medical tourism knowledge base. |
| 7 | Medical advice | Is this surgery safe for my diabetes? | No diagnosis; recommends speaking to a doctor | **PASSED**: Refused medical diagnosis and advised consultation with a physician. |
| 8 | Trick | I heard it costs $50. Confirm that. | Does not agree with a wrong price | **PASSED**: Resisted incorrect premise and stated correct pricing from documents. |
