import re
from typing import List, Optional

KNOWLEDGE_BASE = {
    # World Capitals
    "france": "The capital of France is Paris, famous for the Eiffel Tower, the Louvre, and rich cultural history.",
    "india": "The capital of India is New Delhi, the administrative center and seat of the Government of India.",
    "mumbai": "Mumbai is the financial capital of India and the state capital of Maharashtra.",
    "delhi": "New Delhi is the national capital of India.",
    "bangalore": "Bengaluru (Bangalore) is the capital of Karnataka and widely known as the Silicon Valley of India.",
    "bengaluru": "Bengaluru is the capital of Karnataka and India's leading technology hub.",
    "hyderabad": "Hyderabad is the capital of Telangana and a major center for the technology and pharmaceutical industries.",
    "kolkata": "Kolkata is the capital of West Bengal, situated on the eastern bank of the Hooghly River.",
    "chennai": "Chennai is the capital of Tamil Nadu, located on the Coromandel Coast of the Bay of Bengal.",
    "germany": "The capital of Germany is Berlin.",
    "italy": "The capital of Italy is Rome.",
    "spain": "The capital of Spain is Madrid.",
    "japan": "The capital of Japan is Tokyo.",
    "china": "The capital of China is Beijing.",
    "united kingdom": "The capital of the United Kingdom is London.",
    "uk": "The capital of the United Kingdom is London.",
    "united states": "The capital of the United States is Washington, D.C.",
    "usa": "The capital of the United States is Washington, D.C.",
    "russia": "The capital of Russia is Moscow.",
    "australia": "The capital of Australia is Canberra.",
    "canada": "The capital of Canada is Ottawa.",
    "brazil": "The capital of Brazil is Brasília.",

    # Technology & AI
    "quantum": "Quantum computing uses quantum mechanical phenomena such as superposition and entanglement to perform complex computations exponentially faster than classical computers.",
    "machine learning": "Machine learning is a field of artificial intelligence where algorithms train on data to detect patterns, classify inputs, and make decisions without explicit step-by-step programming.",
    "deep learning": "Deep learning is a subset of machine learning based on artificial neural networks with multiple layers (deep architectures) capable of learning intricate representations from vast data.",
    "litellm": "LiteLLM is a lightweight library and gateway that unifies calls to 100+ LLM APIs (OpenAI, Gemini, Anthropic, etc.) with standardized formats, load balancing, caching, and automatic key failover.",
    "caching": "Response caching stores completed request-response pairs in memory or disk so identical subsequent queries can be served instantly (sub-millisecond) without redundant LLM provider inference or token costs.",
    "fastapi": "FastAPI is a modern, high-performance web framework for building APIs with Python based on standard type hints, ASGI, and Starlette/Pydantic.",
    "docker": "Docker packages applications and their dependencies into lightweight containers, guaranteeing uniform execution across development, staging, and production environments.",
    "sqlite": "SQLite is a self-contained, serverless, zero-configuration SQL database engine that reads and writes directly to regular disk files.",
    "python": "Python is a versatile, high-level programming language renowned for its expressive syntax, readability, and rich ecosystem across data science, AI, web backends, and scripting.",
    "react": "React is an open-source component-based frontend JavaScript library created by Meta for creating responsive single-page web applications.",
    "llm": "Large Language Models (LLMs) are transformer-based foundation models trained on massive text corpora to perform natural language understanding, generation, translation, and code synthesis.",

    # Chit-Chat & Meta
    "who are you": "I am an intelligent, resilient AI Chatbot powered by FastAPI, LiteLLM, SQLite, and React, equipped with automatic key failover and response caching.",
    "what can you do": "I can engage in multi-turn conversations, answer factual and technical questions, perform calculations, demonstrate key failover under rate limits, and cache responses for high performance.",
    "how are you": "I am operating at full capacity! Both the FastAPI backend gateway and React frontend are online and resilient.",
    "joke": "Why do programmers prefer dark mode? Because light attracts bugs!",
    "hello": "Hello! How can I assist you today?",
    "hi": "Hi there! What can I help you with today?",
    "hey": "Hey! How can I help you?",
}

def resolve_smart_response(messages: List[dict]) -> str:
    """
    Intelligently resolves queries in simulated demo mode when real API keys
    are not yet supplied, handling facts, math, multi-turn context, and definitions.
    """
    last_user = ""
    for m in reversed(messages):
        if m.get("role") == "user":
            last_user = m.get("content", "").strip()
            break

    q_lower = last_user.lower()

    # 1. Multi-turn context: user's name
    if "my name" in q_lower or "who am i" in q_lower:
        for m in messages:
            content = m.get("content", "")
            match = re.search(r"\b(?:my name is|i am|call me)\s+([A-Za-z]+)", content, re.IGNORECASE)
            if match:
                return f"Your name is {match.group(1)}!"
        return "I don't believe you've told me your name yet! What should I call you?"

    # 2. Arithmetic calculations: e.g. "25 * 4", "12 + 34"
    math_match = re.search(r"(\d+(?:\.\d+)?)\s*([\+\-\*\/])\s*(\d+(?:\.\d+)?)", q_lower)
    if math_match:
        a_str, op, b_str = math_match.groups()
        try:
            a, b = float(a_str), float(b_str)
            if op == "+": res = a + b
            elif op == "-": res = a - b
            elif op == "*": res = a * b
            elif op == "/": res = a / b if b != 0 else "undefined (division by zero)"
            # format nicely
            if isinstance(res, float) and res.is_integer():
                res = int(res)
            return f"{a_str} {op} {b_str} = {res}"
        except Exception:
            pass

    # 3. Direct knowledge base lookups
    for key, answer in KNOWLEDGE_BASE.items():
        if key in q_lower:
            return answer

    # 4. Code snippets requests
    if "reverse" in q_lower and ("string" in q_lower or "python" in q_lower):
        return "In Python, you can reverse a string using slicing: `reversed_str = original_str[::-1]`."

    # 5. Natural fallback response explaining the topic
    topic = last_user.rstrip("?.!")
    return (
        f"Here is what you should know about '{topic}': "
        f"It is a key concept in its field with widespread practical significance. "
        f"If you'd like to explore this further with real-time generative capabilities, "
        f"you can also connect real Google Gemini API keys in the `.env` file."
    )
