# TravelOps AI Architecture

TravelOps AI is a production-quality multi-agent travel planning system built using Python, LangGraph, and LangChain. It transforms a natural language travel request into a structured, validated, and budget-compliant itinerary through a collaborative agentic workflow.

## Why Multi-Agent?

A travel plan is too complex for a single prompt. It requires different types of reasoning:
- **Search & Comparison**: Finding the best flight or hotel among many options.
- **Synthesis**: Combining disparate data into a cohesive daily schedule.
- **Arithmetic**: Precise budget calculation.
- **Critical Analysis**: Identifying logical flaws (e.g., scheduling a museum on a day it's closed).

By splitting these into specialist agents, we ensure higher quality, easier debugging, and the ability to rerun only the failing components.

## Why LangGraph?

We use LangGraph instead of a simple chain because travel planning is **iterative**.

- **State Management**: A strongly typed `TravelState` acts as the single source of truth, passed between agents.
- **Parallel Execution**: Specialist agents (Flight, Hotel, Activities) run concurrently to reduce latency.
- **Conditional Routing**: The `Critic Agent` decides if a plan is "Approved" or needs "Rework".
- **Loops**: The system can route back to the `Supervisor` for corrections, iterating up to a defined maximum (default: 3) to refine the plan.
- **Traceability**: Every action is recorded in an `execution_trace`, allowing us to audit the AI's decision-making process.

## Agent Communication

Agents do not communicate via unstructured chat. They exchange **Structured Artifacts** (Pydantic models):

- **AgentResult**: Standard wrapper for any agent's output.
- **FlightOption / HotelOption / ActivityOption**: Domain-specific recommendations.
- **Critique**: A list of identified issues with severity and recommended corrective actions.

## Shared State

The `TravelState` is the central nervous system of the graph. Key components include:
- `trip_request`: The original structured requirements.
- `agent_results`: A list of all findings from specialists.
- `itinerary`: The synthesized daily plan.
- `budget_analysis`: The final cost breakdown.
- `rework_requests`: Instructions for agents to revisit their work.

## Tool Boundaries

To prevent "model confusion" and ensure specialization, agents are restricted to specific tools:
- **Flight Agent** $\rightarrow$ `FlightRepository` tools.
- **Hotel Agent** $\rightarrow$ `HotelRepository` tools.
- **Activities Agent** $\rightarrow$ `ActivityRepository` tools.
- **Itinerary Agent** $\rightarrow$ Geography and travel time tools.
- **Budget/Critic Agents** $\rightarrow$ No external search tools; they operate on the shared state.

## Critic/Rework Loop

1. **Plan Generation**: Specialist $\rightarrow$ Itinerary $\rightarrow$ Budget.
2. **Critique**: The Critic Agent independently analyzes the plan for conflicts, budget overages, or illogical pacing.
3. **Decision**:
   - If `approved == True` $\rightarrow$ Finalize.
   - If `approved == False` $\rightarrow$ Route to Supervisor.
4. **Targeted Rework**: The Supervisor interprets the critique and delegates rework ONLY to the agents responsible for the issue (e.g., if the hotel is too expensive, only the Hotel Agent is rerun).

## LLM Abstraction

The system uses a `LLMFactory` to decouple the agent logic from the provider. It supports:
- **Ollama Cloud**: For production-grade performance using `gemma4:31b-cloud`.
- **Local Ollama**: For privacy and local development.
- **Mock LLM**: A deterministic provider that returns synthetic data, allowing full system testing without API keys or internet access.
