"""
LLM-generated narrative summaries per state via Claude API.
Uses prompt caching on the system prompt (significant cost saving over 50 states).
"""
import anthropic
from pathlib import Path
from atlas.config import settings

SYSTEM_PROMPT = """You are a data journalist writing concise, compassionate,
and accurate profiles of LGBTQ+ life in U.S. states for a public interactive atlas.
Your audience is LGBTQ+ adults considering where to live, travel, or advocate.
Tone: warm, direct, factual. Never editorialize beyond what the data shows.
Never use alarmist language. Acknowledge uncertainty when data is sparse.

Write exactly 3 paragraphs with NO headers:
1. Population and community overview (who lives here, community infrastructure)
2. Legal and safety climate (laws, hate crime context, political trend)
3. Health and economic picture (outcomes, disparities, access to care)

Each paragraph: 2-4 sentences. Output plain text only."""


def generate_state_narrative(state_name: str, profile_data: dict) -> str:
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    user_content = f"""Write a profile for {state_name} using this data:

Population: {profile_data.get('population', {})}
Legal scores: {profile_data.get('legal', {})}
Safety data: {profile_data.get('safety', {})}
Health data: {profile_data.get('health', {})}
Economic data: {profile_data.get('economic', {})}
Community data: {profile_data.get('community', {})}
Overall score: {profile_data.get('overall_score')} / 100
Score trend: {profile_data.get('trend', [])}"""

    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=500,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": user_content}],
    )
    return message.content[0].text.strip()


def generate_all_narratives(year: int = 2024) -> None:
    from atlas.config import settings
    import polars as pl

    proc = settings.data_processed_dir
    narratives_dir = proc / "narratives"
    narratives_dir.mkdir(parents=True, exist_ok=True)

    fips_df = pl.read_csv(proc / "reference" / "state_fips.csv")
    scores_df = pl.read_csv(proc / "scores" / "state_scores.csv").filter(
        pl.col("year") == year
    )

    for row in fips_df.iter_rows(named=True):
        fips = row["state_fips"]
        state_name = row["state_name"]
        out_path = narratives_dir / f"{fips}.txt"
        if out_path.exists():
            print(f"  Skipping {state_name} (already generated)")
            continue

        score_row = scores_df.filter(pl.col("state_fips") == fips)
        overall = float(score_row["overall_score"][0]) if len(score_row) > 0 else None

        profile_data = {
            "population": {"lgbtq_pct": None},
            "legal": {},
            "safety": {},
            "health": {},
            "economic": {},
            "community": {},
            "overall_score": overall,
            "trend": [],
        }

        try:
            text = generate_state_narrative(state_name, profile_data)
            out_path.write_text(text)
            print(f"  Generated: {state_name}")
        except Exception as e:
            print(f"  ERROR {state_name}: {e}")
