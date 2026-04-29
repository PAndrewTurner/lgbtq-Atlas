"""
In-memory flat file loader. Instantiated once at app startup.
All routes query these Polars DataFrames — no I/O per request.
"""
import polars as pl
from pathlib import Path
from atlas.config import settings


class DataStore:
    def __init__(self):
        p = settings.data_processed_dir

        self.population  = self._load_csv(p / "population" / "state_population.csv")
        self.policy      = self._load_csv(p / "legal" / "state_policy_scores.csv")
        self.mei         = self._load_csv(p / "legal" / "city_mei_scores.csv")
        self.hate_crimes = self._load_csv(p / "safety" / "state_hate_crimes.csv")
        self.health      = self._load_csv(p / "health" / "state_health_outcomes.csv")
        self.economic    = self._load_csv(p / "economic" / "state_economic_profile.csv")
        self.income_edu  = self._load_csv(p / "socioeconomic" / "state_income_education.csv")
        self.marriage    = self._load_csv(p / "socioeconomic" / "state_marriage_households.csv")
        self.community   = self._load_csv(p / "community" / "state_community.csv")
        self.youth       = self._load_csv(p / "youth" / "state_youth.csv")
        self.scores      = self._load_csv(p / "scores" / "state_scores.csv")
        self.fips_ref    = self._load_csv(p / "reference" / "state_fips.csv")

        # city_scores may not exist yet — MEI scores only
        city_scores_path = p / "scores" / "city_scores.csv"
        self.city_scores = self._load_csv(city_scores_path) if city_scores_path.exists() else pl.DataFrame()

        self.narratives = self._load_narratives(p / "narratives")

        print(
            f"[DataStore] loaded — states: {len(self.fips_ref)}, "
            f"scores: {len(self.scores)}, cities: {len(self.mei)}"
        )

    def _load_csv(self, path: Path) -> pl.DataFrame:
        if not path.exists():
            print(f"[DataStore] WARNING: {path.name} not found — empty DataFrame")
            return pl.DataFrame()
        return pl.read_csv(path, infer_schema_length=1000)

    def _load_narratives(self, path: Path) -> dict[str, str]:
        if not path.exists():
            return {}
        return {f.stem: f.read_text() for f in path.glob("*.txt")}

    def state_scores_for_year(self, year: int) -> pl.DataFrame:
        if self.scores.is_empty():
            return pl.DataFrame()
        return self.scores.filter(pl.col("year") == year)

    def state_profile_data(self, fips: str, year: int) -> dict:
        def row(df: pl.DataFrame) -> dict:
            if df.is_empty() or "state_fips" not in df.columns:
                return {}
            col = pl.col("state_fips")
            # FIPS may be stored as int or string
            try:
                fips_val = int(fips)
                filtered = df.filter(col == fips_val)
            except ValueError:
                filtered = df.filter(col == fips)
            if len(filtered) == 0:
                return {}
            # If year column exists, filter by year
            if "year" in filtered.columns:
                yr = filtered.filter(pl.col("year") == year)
                if len(yr) > 0:
                    return yr.row(0, named=True)
                return filtered.sort("year", descending=True).row(0, named=True)
            return filtered.row(0, named=True)

        fips_row = self.fips_ref.filter(
            pl.col("state_fips").cast(pl.Utf8).str.zfill(2) == str(fips).zfill(2)
        )
        abbr = fips_row["state_abbr"][0] if len(fips_row) > 0 else None

        return {
            "population":  row(self.population),
            "policy":      row(self.policy),
            "hate_crimes": row(self.hate_crimes),
            "health":      row(self.health),
            "economic":    row(self.economic),
            "income_edu":  row(self.income_edu),
            "marriage":    row(self.marriage),
            "community":   row(self.community),
            "youth":       row(self.youth),
            "scores":      row(self.scores),
            "narrative":   self.narratives.get(str(fips).zfill(2), None),
        }


# Singleton — instantiated once at startup
store = DataStore()
