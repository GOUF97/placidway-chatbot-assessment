# Short Write-up: Improvements & Limitations

## What I would improve with another week:
1. **Hybrid Search Implementation:** Combine semantic vector search with keyword-based BM25 retrieval (Ensemble Retriever) to ensure 100% precision when extracting exact numerical figures like package prices.
2. **Lead Capture Integration:** Add an automated prompt trigger when users ask about cost or treatment packages to seamlessly collect their name and email, saving the lead data to a secure database for PlacidWay's sales team.
3. **Automated Content Refresh Cron Job:** Implement a scheduled background scraper to re-index the 7 URLs weekly so pricing or clinic updates reflect automatically without manual re-crawling.

## Known Limitations:
- **Scraping Dependency:** The bot relies on clean extraction from HTML structures. Major layout shifts on the target pages might require updates to CSS selectors or text cleaning rules.
- **Token Limits on Long Contexts:** While chunking handles most documents effectively, complex multi-page comparative queries require precise retrieval chunks to avoid omitting nuanced pricing conditions.
