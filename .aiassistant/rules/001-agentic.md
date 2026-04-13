<!-- PyCharm AI Project Rule -->
<!-- Source: .ai/rules/001-agentic.mdc -->
<!-- Synced: Mon Apr 13 09:03:15 MSK 2026 -->
<!-- Rule type: Always (apply to all files) -->

---
description: Rules for building AI Agents with LLM integrations (OpenAI, Anthropic, LangChain, LangGraph).
globs: ["**/agents/**/*.py", "**/skills/**/*.py", "**/tools/**/*.py"]
alwaysApply: false
---

# AGENTIC SYSTEMS

## Agent Architecture
- Always use `BaseAgent` abstract class from `app/agents/base.py`
- Each agent: single responsibility, `run(input: AgentInput) -> AgentOutput`
- Skills are pure functions: `async def skill_name(ctx: Context, **kwargs) -> Result`
- Tools are Pydantic models with `async def execute(self) -> ToolResult`

## LLM Client Rules
- Abstract LLM calls behind `app/core/llm.py` — never import OpenAI/Anthropic directly in agents
- Always set `max_tokens`, `temperature` explicitly — no defaults
- Use streaming for responses > 500 tokens
- Retry logic: `tenacity` with exponential backoff, max 3 retries

## Token Optimization
- System prompts: store in `app/prompts/` as `.md` files, load once at startup
- Use prompt caching (Anthropic) or prefix caching where available
- Trim conversation history: keep last N turns + summary
- Structured outputs via `response_format={"type": "json_schema"}` to avoid parsing overhead

## Memory & State
- Short-term: `ConversationBufferWindowMemory` (last 10 msgs)
- Long-term: vector store (Qdrant/Chroma) with namespace per user
- State machine for multi-step agents: `LangGraph` StateGraph

## Example Pattern
```python
from app.agents.base import BaseAgent
from app.core.llm import LLMClient

class ResearchAgent(BaseAgent):
    def __init__(self, llm: LLMClient):
        super().__init__(name="research", llm=llm)

    async def run(self, input: AgentInput) -> AgentOutput:
        result = await self.llm.complete(
            system=self.load_prompt("research_system"),
            messages=input.messages,
            max_tokens=1024,
            temperature=0.2,
        )
        return AgentOutput(content=result.text, usage=result.usage)
```
