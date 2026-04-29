"""
Orchestrator: run all transform modules in dependency order.
Usage: uv run python -m atlas.transform.normalize
       or atlas transform (via CLI)
"""


def run_all_transforms() -> None:
    from atlas.transform import geo, population, legal, city_mei, safety
    from atlas.transform import health, economic, socioeconomic, community, youth

    print("=== Transform: geo (reference + GeoJSON) ===")
    geo.run()

    print("\n=== Transform: population ===")
    population.run()

    print("\n=== Transform: legal (state policy scores) ===")
    legal.run()

    print("\n=== Transform: city MEI ===")
    city_mei.run()

    print("\n=== Transform: safety (hate crimes) ===")
    safety.run()

    print("\n=== Transform: health ===")
    health.run()

    print("\n=== Transform: economic ===")
    economic.run()

    print("\n=== Transform: socioeconomic ===")
    socioeconomic.run()

    print("\n=== Transform: community ===")
    community.run()

    print("\n=== Transform: youth ===")
    youth.run()

    print("\n=== Transform: cities GeoJSON ===")
    from atlas.transform import cities
    cities.run()

    print("\nAll transforms complete.")


if __name__ == "__main__":
    run_all_transforms()
