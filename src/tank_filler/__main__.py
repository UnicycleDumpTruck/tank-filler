"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Tank Filler."""


if __name__ == "__main__":
    main(prog_name="tank-filler")  # pragma: no cover
