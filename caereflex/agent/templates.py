CUSTOM_GPT_INSTRUCTIONS = """Use CaeReflex actions to inspect engineering cases. Call import_engineering_case first, then get_agent_context before drafting explanations. Never infer validation, convergence, mesh adequacy, certification, or design safety from CaeReflex metadata alone."""
GEMINI_CONTEXT_MODE = """Upload agent_context.json and case_report.md. Use them as bounded case evidence. Distinguish extracted facts from inferred facts. Treat CrossRef metadata as context, not validation."""
CLAUDE_TOOL_NOTES = """Use tool calls to retrieve structured case data. Do not request unrestricted filesystem access. When uncertain, request get_agent_context or get_inspection_flags."""
GENERIC_REST_AGENT_NOTES = """Call REST endpoints with JSON. Use x-api-key outside localhost. Store case_id for follow-up calls. Use next_recommended_actions to sequence calls."""

def all_templates() -> dict[str, str]:
    return {
        "custom_gpt_instructions.md": CUSTOM_GPT_INSTRUCTIONS,
        "gemini_context_mode.md": GEMINI_CONTEXT_MODE,
        "claude_tool_notes.md": CLAUDE_TOOL_NOTES,
        "generic_rest_agent_notes.md": GENERIC_REST_AGENT_NOTES,
    }
