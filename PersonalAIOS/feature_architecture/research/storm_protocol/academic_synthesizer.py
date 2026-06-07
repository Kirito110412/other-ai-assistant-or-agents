import logging
import asyncio
import aiohttp
from typing import List, Dict

logger = logging.getLogger(__name__)

class AcademicSynthesizer:
    """
    Implements the STORM Protocol for deep, multi-stage academic research.
    Workflow: Topic Outline -> Fetch URLs -> Draft Sections -> Self-Correct -> Compile PDF.
    """
    def __init__(self, hybrid_switch):
        self.max_urls = 50
        self.hybrid_switch = hybrid_switch # Dependency injection for LLM routing

    async def run_research_pipeline(self, topic: str):
        logger.info(f"Initiating STORM Protocol for topic: {topic}")

        # Phase 1: Generate Outline
        outline = await self._generate_outline(topic)
        logger.info(f"Generated Outline: {outline}")

        # Phase 2: Fetch Sources
        urls = await self._fetch_sources(topic)
        logger.info(f"Fetched {len(urls)} URLs")

        # Fetch actual content asynchronously
        source_texts = await self._scrape_sources(urls)

        # Phase 3: Draft Sections
        draft = await self._draft_sections(outline, source_texts)

        # Phase 4: Self-Correction
        revised_draft = await self._self_correct(draft)

        # Phase 5: Compile PDF
        pdf_path = await self._compile_pdf(revised_draft, topic)

        logger.info(f"STORM Protocol complete. Output saved to {pdf_path}")
        return pdf_path

    async def _generate_outline(self, topic: str) -> List[str]:
        prompt = f"Act as an academic researcher. Generate a strict, comprehensive outline for a paper on: '{topic}'. Return only the section headers as a JSON list of strings."
        response = await self.hybrid_switch.execute_query([{"role": "user", "content": prompt}], complexity=0.8)

        try:
            import json
            outline = json.loads(response)
            if isinstance(outline, list):
                return outline
        except Exception as e:
            logger.warning(f"Failed to parse LLM outline JSON. Defaulting. Error: {e}")

        return ["Introduction", "Literature Review", "Methodology", "Discussion", "Conclusion"]

    async def _fetch_sources(self, topic: str) -> List[str]:
        # In a full implementation, this would use a Search API (SerpAPI/DuckDuckGo).
        # We mock this for now to represent the URL gathering phase of STORM.
        logger.info(f"Simulating web search for {self.max_urls} sources on: {topic}")
        await asyncio.sleep(1)
        return [f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"] * 5 # Fallback to wiki

    async def _scrape_sources(self, urls: List[str]) -> Dict[str, str]:
        results = {}
        async with aiohttp.ClientSession() as session:
            for url in set(urls): # Deduplicate
                try:
                    async with session.get(url, timeout=5) as response:
                        if response.status == 200:
                            text = await response.text()
                            # Strip HTML (rudimentary for now)
                            results[url] = text[:2000] # Cap length per source
                except Exception as e:
                    logger.warning(f"Failed to fetch {url}: {e}")
        return results

    async def _draft_sections(self, outline: List[str], source_texts: Dict[str, str]) -> str:
        full_draft = f"# Draft Research Document\n\n"

        # Synthesize knowledge from sources
        context = " ".join([text[:500] for text in source_texts.values()])

        for section in outline:
            prompt = f"Draft the '{section}' section for an academic paper. Base it on this context: {context}. Include inline citations [1], [2], etc."
            section_content = await self.hybrid_switch.execute_query([{"role": "user", "content": prompt}], complexity=0.9)
            full_draft += f"## {section}\n{section_content}\n\n"

        return full_draft

    async def _self_correct(self, draft: str) -> str:
        prompt = f"Review the following academic draft. Fix any hallucinations, improve the flow, ensure a formal tone, and verify citations are logical. Draft:\n\n{draft}"
        revised = await self.hybrid_switch.execute_query([{"role": "user", "content": prompt}], complexity=0.95)
        return revised

    async def _compile_pdf(self, final_text: str, topic: str) -> str:
        # We use a markdown file as a proxy for the final document if reportlab/pdfkit isn't available
        filename = f"/tmp/{topic.replace(' ', '_')}_STORM_report.md"
        with open(filename, 'w') as f:
            f.write(final_text)
        return filename
