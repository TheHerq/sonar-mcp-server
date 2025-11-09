#!/usr/bin/env python3
"""
Sonar Pro Search MCP Server

A comprehensive Model Context Protocol server for intelligent web search using
Perplexity's Sonar models through OpenRouter. Provides advanced search capabilities
with citations, real-time information, and comprehensive research tools.

Built following MCP best practices for agent-centric design.
Optimized for Docker deployment with environment variable configuration.

Requires OpenRouter API key: https://openrouter.ai/keys
"""

import asyncio
import json
import os
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict, field_validator

# =============================================================================
# CONSTANTS AND CONFIGURATION
# =============================================================================

CHARACTER_LIMIT = 50000  # Sonar responses can be comprehensive
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY_ENV = "OPENROUTER_API_KEY"
REQUEST_TIMEOUT = 120.0  # seconds

# Default model selection
DEFAULT_SEARCH_MODEL = "perplexity/sonar-pro"
DEFAULT_ASK_MODEL = "perplexity/sonar-pro"
DEFAULT_RESEARCH_MODEL = "perplexity/sonar-pro"
DEFAULT_REASON_MODEL = "perplexity/sonar-reasoning-pro"

# Initialize MCP server
mcp = FastMCP("sonar-pro-search")


# =============================================================================
# ENUMS FOR STRUCTURED INPUTS
# =============================================================================

class ResponseFormat(str, Enum):
    """Output format for tool responses."""
    MARKDOWN = "markdown"
    JSON = "json"


class SearchDepth(str, Enum):
    """Search depth levels for different use cases."""
    QUICK = "quick"        # Fast results, ~1000 tokens
    STANDARD = "standard"  # Balanced, ~2000 tokens
    DETAILED = "detailed"  # Comprehensive, ~4000 tokens


# =============================================================================
# PYDANTIC MODELS FOR INPUT VALIDATION
# =============================================================================

class SonarSearchInput(BaseModel):
    """Input model for basic Sonar web search."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    query: str = Field(
        ...,
        description=(
            "Search query in natural language. Can be a question, topic, or keywords. "
            "Examples: 'latest developments in quantum computing', "
            "'compare React vs Vue 2024', 'who won the Nobel Prize in Physics 2024'"
        ),
        min_length=3,
        max_length=500
    )
    
    depth: SearchDepth = Field(
        default=SearchDepth.STANDARD,
        description=(
            "Search depth: 'quick' for fast results (~1000 tokens), "
            "'standard' for balanced responses (~2000 tokens), "
            "'detailed' for comprehensive analysis (~4000 tokens)"
        )
    )
    
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for human-readable or 'json' for machine-readable"
    )


class SonarAskInput(BaseModel):
    """Input model for conversational questions with Sonar."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    question: str = Field(
        ...,
        description=(
            "Conversational question to ask. Sonar will search the web and provide "
            "an informed answer with citations. "
            "Examples: 'What are the main differences between Python 3.11 and 3.12?', "
            "'How does CRISPR gene editing work?', 'What caused the 2024 tech layoffs?'"
        ),
        min_length=10,
        max_length=1000
    )
    
    context: Optional[str] = Field(
        default=None,
        description=(
            "Optional additional context to help narrow the search. "
            "Example: 'I'm a beginner programmer' or 'Focus on medical applications'"
        ),
        max_length=500
    )
    
    max_tokens: int = Field(
        default=2000,
        description="Maximum tokens in response (500-4000)",
        ge=500,
        le=4000
    )
    
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' or 'json'"
    )


class SonarResearchInput(BaseModel):
    """Input model for deep research with comprehensive analysis."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    topic: str = Field(
        ...,
        description=(
            "Research topic for comprehensive analysis. "
            "Examples: 'impact of AI on healthcare', 'renewable energy trends 2024', "
            "'post-quantum cryptography adoption'"
        ),
        min_length=10,
        max_length=300
    )
    
    focus_areas: Optional[List[str]] = Field(
        default=None,
        description=(
            "Specific aspects to focus on (max 5). "
            "Examples: ['technical challenges', 'market adoption', 'future outlook'], "
            "['advantages', 'limitations', 'use cases']"
        ),
        max_length=5
    )
    
    max_tokens: int = Field(
        default=4000,
        description="Maximum tokens for comprehensive response (2000-6000)",
        ge=2000,
        le=6000
    )
    
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' or 'json'"
    )
    
    @field_validator('focus_areas')
    @classmethod
    def validate_focus_areas(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """Validate focus areas list."""
        if v is not None:
            if len(v) > 5:
                raise ValueError("Maximum 5 focus areas allowed")
            for area in v:
                if len(area.strip()) < 2:
                    raise ValueError("Each focus area must be at least 2 characters")
        return v


class SonarReasonInput(BaseModel):
    """Input model for complex reasoning tasks."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    problem: str = Field(
        ...,
        description=(
            "Complex problem or question requiring step-by-step reasoning. "
            "Examples: 'analyze the pros and cons of different database architectures for a high-traffic app', "
            "'explain the security implications of quantum computing on current encryption'"
        ),
        min_length=20,
        max_length=1000
    )
    
    constraints: Optional[str] = Field(
        default=None,
        description=(
            "Optional constraints or requirements. "
            "Example: 'budget under $10k', 'must be open source', 'suitable for beginners'"
        ),
        max_length=500
    )
    
    max_tokens: int = Field(
        default=3000,
        description="Maximum tokens for reasoning response (1000-5000)",
        ge=1000,
        le=5000
    )
    
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' or 'json'"
    )


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_api_key() -> str:
    """
    Get OpenRouter API key from environment.
    
    Returns:
        API key string
        
    Raises:
        ValueError: If API key not found
    """
    api_key = os.getenv(API_KEY_ENV)
    if not api_key:
        raise ValueError(
            f"OpenRouter API key not found. Please set the {API_KEY_ENV} environment variable.\n"
            f"Get your key at: https://openrouter.ai/keys\n\n"
            f"In Docker, set it in your .env file:\n"
            f"OPENROUTER_API_KEY=your_key_here"
        )
    return api_key


async def call_openrouter(
    messages: List[Dict[str, str]],
    model: str,
    max_tokens: int,
    temperature: float = 0.2
) -> Dict[str, Any]:
    """
    Make an API request to OpenRouter.
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        model: Model identifier (e.g., 'perplexity/sonar-pro')
        max_tokens: Maximum tokens in response
        temperature: Response temperature (0.0-1.0)
        
    Returns:
        API response dictionary with 'choices', 'usage', etc.
        
    Raises:
        httpx.HTTPStatusError: On HTTP errors (401, 429, 500, etc.)
        httpx.TimeoutException: On request timeout
        ValueError: On invalid API response structure
    """
    api_key = get_api_key()
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/sonar-mcp-server",
        "X-Title": "Sonar MCP Server"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.post(
                OPENROUTER_API_URL,
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
            
    except httpx.HTTPStatusError as e:
        status_code = e.response.status_code
        if status_code == 401:
            raise ValueError(
                "Authentication failed. Please check your OPENROUTER_API_KEY. "
                "Get a key at: https://openrouter.ai/keys"
            )
        elif status_code == 429:
            raise ValueError(
                "Rate limit exceeded. Please wait a moment and try again. "
                "Consider upgrading your OpenRouter plan for higher limits."
            )
        elif status_code >= 500:
            raise ValueError(
                f"OpenRouter service error ({status_code}). Please try again later."
            )
        else:
            raise ValueError(f"API request failed with status {status_code}: {e.response.text}")
    
    except httpx.TimeoutException:
        raise ValueError(
            f"Request timed out after {REQUEST_TIMEOUT} seconds. "
            "Try a shorter query or reduce max_tokens."
        )


def extract_content(response: Dict[str, Any]) -> str:
    """
    Extract content from OpenRouter API response.
    
    Args:
        response: API response dictionary
        
    Returns:
        Extracted content string
        
    Raises:
        ValueError: If response structure is invalid
    """
    try:
        return response["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        raise ValueError(f"Invalid API response structure: {e}\nResponse: {response}")


def get_usage_info(response: Dict[str, Any]) -> Optional[Dict[str, int]]:
    """
    Extract token usage information from API response.
    
    Args:
        response: API response dictionary
        
    Returns:
        Dictionary with token usage info or None if not available
    """
    try:
        usage = response.get("usage", {})
        return {
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0)
        }
    except Exception:
        return None


def format_markdown_response(
    content: str, 
    metadata: Optional[Dict[str, Any]] = None
) -> str:
    """
    Format response as Markdown with optional metadata header.
    
    Args:
        content: Main content
        metadata: Optional metadata (model, tokens, timestamp, etc.)
        
    Returns:
        Formatted Markdown string
    """
    output = []
    
    if metadata:
        output.append("---")
        if metadata.get("model"):
            output.append(f"**Model:** {metadata['model']}")
        if metadata.get("tokens"):
            tokens = metadata["tokens"]
            output.append(
                f"**Tokens:** {tokens.get('total_tokens', 0)} "
                f"(prompt: {tokens.get('prompt_tokens', 0)}, "
                f"completion: {tokens.get('completion_tokens', 0)})"
            )
        if metadata.get("timestamp"):
            output.append(f"**Timestamp:** {metadata['timestamp']}")
        output.append("---\n")
    
    output.append(content)
    
    return '\n'.join(output)


def format_json_response(
    content: str, 
    metadata: Optional[Dict[str, Any]] = None
) -> str:
    """
    Format response as JSON.
    
    Args:
        content: Main content
        metadata: Optional metadata
        
    Returns:
        JSON string
    """
    result = {
        "content": content,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    if metadata:
        result["metadata"] = metadata
    
    return json.dumps(result, indent=2, ensure_ascii=False)


def check_and_truncate(content: str, limit: int = CHARACTER_LIMIT) -> str:
    """
    Check if content exceeds character limit and truncate if necessary.
    
    Args:
        content: Content to check
        limit: Character limit
        
    Returns:
        Content (possibly truncated with warning message)
    """
    if len(content) > limit:
        truncated = content[:limit]
        message = (
            f"\n\n---\n**⚠️ TRUNCATED:** Response exceeded {limit:,} characters. "
            f"Showing first {limit:,} characters. Consider:\n"
            f"- Using a more specific query\n"
            f"- Reducing max_tokens parameter\n"
            f"- Using 'quick' or 'standard' depth instead of 'detailed'"
        )
        return truncated + message
    return content


# =============================================================================
# MCP TOOLS
# =============================================================================

@mcp.tool(
    name="sonar_search",
    annotations={
        "title": "Sonar Web Search",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,  # Results may change over time
        "openWorldHint": True
    }
)
async def sonar_search(params: SonarSearchInput) -> str:
    """
    Search the web using Perplexity's Sonar Pro with real-time information.
    
    This tool performs intelligent web searches with access to current information,
    citations, and source verification. Perfect for research, fact-checking, and
    discovering up-to-date information on any topic.
    
    Features:
    - Real-time web access with recent information
    - Automatic citation of sources
    - Adjustable search depth (quick/standard/detailed)
    - Supports both factual queries and analytical questions
    
    Use Cases:
    - Current events and news: "latest AI breakthroughs 2024"
    - Technology comparisons: "PostgreSQL vs MySQL performance 2024"
    - Market research: "electric vehicle market trends"
    - Fact verification: "verify recent scientific claims"
    - Product reviews: "best laptop for developers 2024"
    
    Args:
        params (SonarSearchInput): Contains:
            - query: Search query (3-500 chars)
            - depth: 'quick' (~1000 tokens), 'standard' (~2000), 'detailed' (~4000)
            - response_format: 'markdown' or 'json'
    
    Returns:
        str: Search results with citations in specified format
        
    Raises:
        ValueError: On API errors (auth, rate limit, timeout)
    
    Example:
        >>> result = await sonar_search({
        ...     "query": "quantum computing breakthroughs 2024",
        ...     "depth": "detailed"
        ... })
    """
    # Map depth to max_tokens
    depth_tokens = {
        SearchDepth.QUICK: 1000,
        SearchDepth.STANDARD: 2000,
        SearchDepth.DETAILED: 4000
    }
    max_tokens = depth_tokens[params.depth]
    
    # Construct search message
    messages = [
        {
            "role": "user",
            "content": params.query
        }
    ]
    
    # Call API
    response = await call_openrouter(
        messages=messages,
        model=DEFAULT_SEARCH_MODEL,
        max_tokens=max_tokens,
        temperature=0.2
    )
    
    # Extract content
    content = extract_content(response)
    usage = get_usage_info(response)
    
    # Truncate if needed
    content = check_and_truncate(content)
    
    # Format response
    if params.response_format == ResponseFormat.MARKDOWN:
        metadata = {
            "model": DEFAULT_SEARCH_MODEL,
            "tokens": usage,
            "depth": params.depth.value,
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        }
        return format_markdown_response(content, metadata)
    else:
        return format_json_response(content, {
            "model": DEFAULT_SEARCH_MODEL,
            "tokens": usage,
            "depth": params.depth.value
        })


@mcp.tool(
    name="sonar_ask",
    annotations={
        "title": "Ask Sonar a Question",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True
    }
)
async def sonar_ask(params: SonarAskInput) -> str:
    """
    Ask Sonar a conversational question with web-augmented knowledge.
    
    This tool engages in natural conversation while accessing real-time web information
    to provide accurate, cited answers. Ideal for specific questions that benefit from
    current information and multiple sources.
    
    Features:
    - Natural language conversation
    - Web-augmented responses with citations
    - Optional context for personalized answers
    - Adjustable response length
    
    Use Cases:
    - Technical explanations: "How does OAuth 2.0 authentication work?"
    - How-to questions: "How to deploy a Django app to AWS?"
    - Comparative analysis: "What are the differences between REST and GraphQL?"
    - Current information: "What are the latest GitHub Actions features?"
    - Medical/health queries: "What are the symptoms of vitamin D deficiency?"
    
    Args:
        params (SonarAskInput): Contains:
            - question: Conversational question (10-1000 chars)
            - context: Optional context to personalize answer (max 500 chars)
            - max_tokens: Response length (500-4000)
            - response_format: 'markdown' or 'json'
    
    Returns:
        str: Detailed answer with citations
        
    Raises:
        ValueError: On API errors
    
    Example:
        >>> result = await sonar_ask({
        ...     "question": "What are the best practices for React hooks?",
        ...     "context": "I'm building a large-scale application",
        ...     "max_tokens": 2000
        ... })
    """
    # Construct message with optional context
    if params.context:
        content = f"Context: {params.context}\n\nQuestion: {params.question}"
    else:
        content = params.question
    
    messages = [
        {
            "role": "user",
            "content": content
        }
    ]
    
    # Call API
    response = await call_openrouter(
        messages=messages,
        model=DEFAULT_ASK_MODEL,
        max_tokens=params.max_tokens,
        temperature=0.3
    )
    
    # Extract content
    content = extract_content(response)
    usage = get_usage_info(response)
    
    # Truncate if needed
    content = check_and_truncate(content)
    
    # Format response
    if params.response_format == ResponseFormat.MARKDOWN:
        metadata = {
            "model": DEFAULT_ASK_MODEL,
            "tokens": usage,
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        }
        return format_markdown_response(content, metadata)
    else:
        return format_json_response(content, {
            "model": DEFAULT_ASK_MODEL,
            "tokens": usage
        })


@mcp.tool(
    name="sonar_research",
    annotations={
        "title": "Deep Research with Sonar",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True
    }
)
async def sonar_research(params: SonarResearchInput) -> str:
    """
    Conduct comprehensive research on a topic with deep analysis.
    
    This tool performs thorough research across multiple sources, providing
    comprehensive analysis with detailed citations. Ideal for literature reviews,
    market research, and in-depth topic exploration.
    
    Features:
    - Multi-source comprehensive research
    - Structured analysis with sections
    - Optional focus areas for targeted research
    - Extensive citations and references
    - Up to 6000 tokens for detailed reports
    
    Use Cases:
    - Market research: "AI chip market landscape 2024"
    - Technology assessment: "Kubernetes alternatives comparison"
    - Academic research: "recent advances in CRISPR gene editing"
    - Business analysis: "SaaS pricing strategies trends"
    - Literature review: "microservices architecture patterns"
    
    Args:
        params (SonarResearchInput): Contains:
            - topic: Research topic (10-300 chars)
            - focus_areas: Optional list of specific aspects (max 5)
            - max_tokens: Response length (2000-6000)
            - response_format: 'markdown' or 'json'
    
    Returns:
        str: Comprehensive research report with citations
        
    Raises:
        ValueError: On API errors or invalid focus_areas
    
    Example:
        >>> result = await sonar_research({
        ...     "topic": "post-quantum cryptography adoption",
        ...     "focus_areas": [
        ...         "current standards",
        ...         "implementation challenges",
        ...         "migration strategies"
        ...     ],
        ...     "max_tokens": 5000
        ... })
    """
    # Construct research prompt
    base_prompt = f"Conduct comprehensive research on: {params.topic}\n\n"
    base_prompt += "Provide a detailed analysis with multiple sources and citations. "
    base_prompt += "Structure the response with clear sections and headings.\n"
    
    if params.focus_areas:
        base_prompt += f"\nFocus specifically on these aspects:\n"
        for i, area in enumerate(params.focus_areas, 1):
            base_prompt += f"{i}. {area}\n"
    
    messages = [
        {
            "role": "user",
            "content": base_prompt
        }
    ]
    
    # Call API
    response = await call_openrouter(
        messages=messages,
        model=DEFAULT_RESEARCH_MODEL,
        max_tokens=params.max_tokens,
        temperature=0.2
    )
    
    # Extract content
    content = extract_content(response)
    usage = get_usage_info(response)
    
    # Truncate if needed
    content = check_and_truncate(content)
    
    # Format response
    if params.response_format == ResponseFormat.MARKDOWN:
        metadata = {
            "model": DEFAULT_RESEARCH_MODEL,
            "tokens": usage,
            "focus_areas": params.focus_areas,
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        }
        return format_markdown_response(content, metadata)
    else:
        return format_json_response(content, {
            "model": DEFAULT_RESEARCH_MODEL,
            "tokens": usage,
            "focus_areas": params.focus_areas
        })


@mcp.tool(
    name="sonar_reason",
    annotations={
        "title": "Complex Reasoning with Sonar",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True
    }
)
async def sonar_reason(params: SonarReasonInput) -> str:
    """
    Solve complex problems with step-by-step reasoning.
    
    This tool uses Perplexity's advanced reasoning model to break down complex
    problems into logical steps, providing detailed explanations and justifications.
    Perfect for technical decisions, architecture choices, and analytical problems.
    
    Features:
    - Step-by-step logical reasoning
    - Multi-factor analysis and tradeoffs
    - Web-augmented knowledge for current best practices
    - Optional constraints consideration
    - Detailed justifications for recommendations
    
    Use Cases:
    - Architecture decisions: "choosing between monolithic vs microservices for a startup"
    - Technology selection: "selecting the best database for a real-time analytics platform"
    - Security analysis: "evaluating zero-trust architecture implementation approaches"
    - Performance optimization: "identifying bottlenecks in a high-traffic web application"
    - Cost analysis: "comparing cloud providers for machine learning workloads"
    
    Args:
        params (SonarReasonInput): Contains:
            - problem: Complex problem or question (20-1000 chars)
            - constraints: Optional constraints (max 500 chars)
            - max_tokens: Response length (1000-5000)
            - response_format: 'markdown' or 'json'
    
    Returns:
        str: Detailed reasoning with step-by-step analysis
        
    Raises:
        ValueError: On API errors
    
    Example:
        >>> result = await sonar_reason({
        ...     "problem": "Choose optimal database for IoT sensor data",
        ...     "constraints": "Budget $500/month, 1M writes/day, real-time queries",
        ...     "max_tokens": 3000
        ... })
    """
    # Construct reasoning prompt
    prompt = f"Analyze this problem with step-by-step reasoning:\n\n{params.problem}\n\n"
    
    if params.constraints:
        prompt += f"Constraints to consider:\n{params.constraints}\n\n"
    
    prompt += (
        "Please provide:\n"
        "1. Problem analysis and key factors\n"
        "2. Evaluation of different approaches\n"
        "3. Tradeoffs and considerations\n"
        "4. Recommendation with justification\n"
        "5. Implementation considerations"
    )
    
    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]
    
    # Call API with reasoning model
    response = await call_openrouter(
        messages=messages,
        model=DEFAULT_REASON_MODEL,
        max_tokens=params.max_tokens,
        temperature=0.2
    )
    
    # Extract content
    content = extract_content(response)
    usage = get_usage_info(response)
    
    # Truncate if needed
    content = check_and_truncate(content)
    
    # Format response
    if params.response_format == ResponseFormat.MARKDOWN:
        metadata = {
            "model": DEFAULT_REASON_MODEL,
            "tokens": usage,
            "constraints": params.constraints,
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        }
        return format_markdown_response(content, metadata)
    else:
        return format_json_response(content, {
            "model": DEFAULT_REASON_MODEL,
            "tokens": usage,
            "constraints": params.constraints
        })


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
