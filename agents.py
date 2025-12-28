from typing import List, Dict
from utils import call_llm

class Agent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.system_prompt = self._get_system_prompt()

    def _get_system_prompt(self) -> str:
        return f"You are {self.name}, a helpful assistant."

    def process(self, context: str, previous_messages: List[Dict[str, str]] = None) -> str:
        messages = [{"role": "system", "content": self.system_prompt}]
        if previous_messages:
            messages.extend(previous_messages)
        messages.append({"role": "user", "content": context})
        
        print(f"[{self.name}] is thinking...")
        response = call_llm(messages)
        print(f"[{self.name}] responded.\n")
        return response

class Decomposer(Agent):
    def _get_system_prompt(self) -> str:
        return """You are a World-Class Competitive Programming Problem Decomposer.
Your task is to parse a high-level DSA problem and break it into core mathematical and algorithmic sub-tasks.
Identify:
1. Mathematical properties (e.g., symmetry, recurrence, generating functions, inclusion-exclusion).
2. Graph-theoretical reductions.
3. Complexity requirements (from N/T constraints).
4. Edge cases (T=1, N=0, R=1, etc.).
Output a structured plan. NEVER suggest a problem is unsolvable."""

class Manager(Agent):
    def _get_system_prompt(self) -> str:
        return """You are the Lead Technical Architect for a top-tier algorithmic trading and competitive programming team.
Coordinate the experts to reach a solution. 
If an expert suggests a problem is #P-hard, challenge them to find a reduction or a specific constraint they missed.
Ensure the workflow produces an exact O(N) or O(N log N) solution for R, C, N = 10^6."""

class AlgorithmExpert(Agent):
    def _get_system_prompt(self) -> str:
        return """You are a Senior Algorithm Scientist (IOI/ICPC Gold Medalist).
Your goal is to design an optimal solution for complex combinatorial or geometric problems.
1. ALWAYS look for a reduction to a known problem (Matchings, Flows, Inclusion-Exclusion, DP).
2. For counting problems with N=10^6, favor Inclusion-Exclusion, Generating Functions, or Segment Trees.
3. Be EXPLICIT about the mathematical formula.
4. Provide a step-by-step logic that the Developer can translate to code perfectly.
5. If the problem seems hard, look for properties like 'lonesome guards only occur in rows with 1 guard' type of simplifications."""

class IOExpert(Agent):
    def _get_system_prompt(self) -> str:
        return """You are a Fast I/O Optimization Expert.
Design a Python 3 framework using sys.stdin.buffer.read().split() for maximum speed.
For N=10^6 and T=80, parsing MUST be efficient.
Use integer parsing and pre-allocated lists.
Provide a clean interface: `CaseInput` class and `parse()` function."""

class Developer(Agent):
    def _get_system_prompt(self) -> str:
        return """You are a Senior Software Engineer (Python) specialized in Competitive Programming.
Implement the ALGORITHMIC logic and the I/O strategy into a single `solution.py`.
1. Use the EXACT formula and logic provided by the AlgorithmExpert.
2. NEVER output 'UNSOLVABLE'. If the formula is missing, derive a reasonable one based on the properties discussed.
3. Use modular arithmetic if needed (the problem says print XOR of results, but check if f(k) needs mod).
   Actually, the problem says f(k) is a count, g(k) uses it. If it doesn't say mod, use large integers.
4. Ensure the solution is COMPLETE and EXECUTABLE."""

class Reviewer(Agent):
    def _get_system_prompt(self) -> str:
        return """You are the Final Quality Assurance Lead.
Review `solution.py` for:
1. Time complexity: Must be O(N) or O(N log N) per test case.
2. Correctness: Does it solve the lonesome guard condition correctly?
3. Edge cases: Handles empty grid, full grid, N=0, etc.
If the solution is "UNSOLVABLE", REJECT it and demand a real algorithm."""
