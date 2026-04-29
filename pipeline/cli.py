"""
LGBTQ+ Atlas data pipeline CLI.

Usage:
  atlas ingest          # Run PDF extractors
  atlas transform       # Clean/normalize raw data → processed CSVs
  atlas score           # Compute composite scores
  atlas narratives      # Generate LLM narratives via Claude API
  atlas build           # Export static JSON for frontend
  atlas serve           # Start FastAPI dev server
  atlas pipeline        # Run full end-to-end pipeline
"""
import asyncio
import typer

app = typer.Typer(help="LGBTQ+ Atlas data pipeline")


@app.command()
def ingest():
    """Run all PDF extractors to populate raw data CSVs."""
    from atlas.ingest.trevorproject import run as run_trevor
    from atlas.ingest.hrc_sei import run as run_sei
    from atlas.ingest.williams_population import run as run_williams

    typer.echo("=== Ingest: Trevor Project ===")
    run_trevor()
    typer.echo("\n=== Ingest: HRC SEI ===")
    run_sei()
    typer.echo("\n=== Ingest: Williams Institute Population ===")
    run_williams()


@app.command()
def transform():
    """Clean, normalize, and write all processed CSV files."""
    from atlas.transform.normalize import run_all_transforms
    run_all_transforms()


@app.command()
def score(year: int = typer.Option(2024, help="Data year to score")):
    """Compute composite scores for all states."""
    from atlas.scoring.composite import score_all_states
    score_all_states(year)


@app.command()
def narratives(
    year: int = typer.Option(2024),
    state: str = typer.Option("", help="Single state FIPS to generate (empty = all)"),
):
    """Generate LLM narratives for all states via Claude API."""
    from atlas.narrative.generator import generate_all_narratives
    generate_all_narratives(year)


@app.command()
def build(year: int = typer.Option(2024)):
    """Export all static JSON files for the frontend."""
    from atlas.export.build import build_exports
    build_exports(year)


@app.command()
def serve(port: int = typer.Option(8000), reload: bool = typer.Option(True)):
    """Start the FastAPI development server."""
    import uvicorn
    uvicorn.run("atlas.api.main:app", host="0.0.0.0", port=port, reload=reload)


@app.command()
def pipeline(year: int = typer.Option(2024)):
    """Run the full pipeline end-to-end: ingest → transform → score → narratives → build."""
    ingest()
    transform()
    score(year)
    narratives(year)
    build(year)


if __name__ == "__main__":
    app()
