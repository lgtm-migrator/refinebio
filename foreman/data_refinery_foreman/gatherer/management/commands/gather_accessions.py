"""MicroArray (ArrayExpress, GEO) and RNA-Seq accession gathering automation.
Data sources:
  - https://www.ebi.ac.uk/biostudies/help (MicroArray ArrayExpress).
  - local SQLite meta DB from https://www.bioconductor.org/packages/release/bioc/html/GEOmetadb.html
    (MicroArray GEO).
  - https://www.ebi.ac.uk/ena/portal/api/ (RNA-Seq).
"""

import argparse
import logging
import re

from django.core.management.base import BaseCommand

from data_refinery_common.logging import get_and_configure_logger
from data_refinery_common.models.gathered_accession import GatheredAccession
from data_refinery_foreman.gatherer.agents.microarray_ae import MicroArrayExpressAccessionAgent
from data_refinery_foreman.gatherer.agents.microarray_geo import MicroArrayGEOAccessionAgent
from data_refinery_foreman.gatherer.agents.rna_seq import RNASeqAccessionAgent

logger = get_and_configure_logger(__name__)


class Command(BaseCommand):
    """Creates agents and runs actual accession gathering."""

    DATA_SOURCE_MA_AE = "microarray-ae"
    DATA_SOURCE_MA_GEO = "microarray-geo"
    DATA_SOURCE_RNA_SEQ = "rna-seq"
    DATA_SOURCES = (DATA_SOURCE_MA_AE, DATA_SOURCE_MA_GEO, DATA_SOURCE_RNA_SEQ)

    RE_ACCESSION = re.compile(r"(\D+)(\d+)")
    RE_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")

    # TODO(ark): remove after upgrade to python3.8 where parser argument
    # "extend" action is directly available.
    # https://docs.python.org/3.8/library/argparse.html#action
    class ExtendAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            items = getattr(namespace, self.dest) or []
            items.extend(values)
            setattr(namespace, self.dest, items)

    def add_arguments(self, parser) -> None:
        parser.register("action", "extend", Command.ExtendAction)

        parser.add_argument(
            "--ae-id",
            action="extend",
            nargs="+",
            type=str,
            help="ArrayExpress ID(s) to use for filtering.",
        )
        parser.add_argument(
            "--ae-ids-file",
            type=str,
            help="Path to a file containing ArrayExpress ID(s) to use for filtering.",
        )
        parser.add_argument("-c", "--count", type=int, help="Number of accessions to collect.")
        parser.add_argument(
            "-d",
            "--dry-run",
            action="store_true",
            default=False,
            help="Do not write the result to the database.",
        )
        parser.add_argument(
            "-e",
            "--exclude-previous",
            action="store_true",
            default=True,
            help="Exclude previously gathered or surveyed accessions.",
        )
        parser.add_argument(
            "--gpl-id",
            action="extend",
            nargs="+",
            type=str,
            help="GEO platform ID(s) to use for filtering.",
        )
        parser.add_argument(
            "--gpl-ids-file",
            type=str,
            help="Path to a file containing GEO platform ID(s) to use for filtering.",
        )
        parser.add_argument(
            "-k",
            "--keyword",
            type=str,
            help="Keyword to use for filtering.",
        )
        parser.add_argument(
            "-lv",
            "--log-verbose",
            action="store_true",
            default=False,
            help="Enable verbose log output.",
        )
        parser.add_argument(
            "-ne",
            "--no-exclude-previous",
            action="store_false",
            default=False,
            dest="exclude_previous",
            help="Do not exclude previously gathered or surveyed accessions.",
        )
        parser.add_argument(
            "-o", "--organism", type=str, help="Organism name to use for filtering."
        )
        parser.add_argument(
            "-s",
            "--since",
            type=str,
            required=True,
            help="Collect accessions made public on or after this date.",
        )
        parser.add_argument(
            "-src",
            "--source",
            type=str,
            action="extend",
            nargs="+",
            help="Gather accessions from selected sources.",
        )
        parser.add_argument(
            "--taxon-id",
            action="extend",
            nargs="+",
            type=int,
            help="Taxon ID(s) to use for filtering.",
        )
        parser.add_argument(
            "--taxon-ids-file",
            type=str,
            help="Path to a file containing taxon ID(s) to use for filtering.",
        )
        parser.add_argument(
            "-u",
            "--until",
            type=str,
            help="Collect accessions made public before or on this date.",
        )

    def set_verbosity_level(self, options) -> None:
        """Configures log verbosity level."""
        if options["log_verbose"]:
            logger.addHandler(logging.StreamHandler())
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.ERROR)

    def validate_args(self, options) -> None:
        """Validates arguments."""
        errors = list()

        since = options["since"]
        until = options["until"]
        if not self.RE_DATE.match(since):
            errors.append('The -s, --since value must match "YYYY-MM-DD" format.')
        if until and not self.RE_DATE.match(until):
            errors.append('The -u, --until value must match "YYYY-MM-DD" format.')
        if since and until and since > until:
            errors.append("The -s, --since date must be earlier than -u, --until date.")

        keyword = options["keyword"]
        organism = options["organism"]
        sources = options["source"] or self.DATA_SOURCES

        for source in sources:
            if source in self.DATA_SOURCES:
                continue
            errors.append(
                f"Unknown source: {source}. Supported sources: {', '.join(self.DATA_SOURCES)}"
            )

        if self.DATA_SOURCE_MA_AE in sources:
            ids = options["ae_id"] or options["ae_ids_file"]
            if not (ids or keyword or organism):
                errors.append(
                    (
                        "Exactly one of the keyword [-k, --keyword], organism [-o, --organism] or "
                        "ArrayExpress ID(s) [--ae-id, --ae-ids-file] must be specified for "
                        f"'{self.DATA_SOURCE_MA_AE}' source."
                    )
                )
        if self.DATA_SOURCE_MA_GEO in sources:
            ids = options["gpl_id"] or options["gpl_ids_file"]
            if not (ids or keyword or organism):
                errors.append(
                    (
                        "Exactly one of the keyword [-k, --keyword], organism [-o, --organism] or "
                        "GEO platform ID(s) [--gpl-id, --gpl-ids-file] must be specified for "
                        f"'{self.DATA_SOURCE_MA_GEO}' source."
                    )
                )
        if self.DATA_SOURCE_RNA_SEQ in sources:
            ids = options["taxon_id"] or options["taxon_ids_file"]
            if not (ids or keyword or organism):
                errors.append(
                    (
                        "Exactly one of the keyword [-k, --keyword], organism [-o, --organism] "
                        "or taxon ID(s) [--taxon-id, --taxon-ids-file] must be specified for "
                        f"'{self.DATA_SOURCE_RNA_SEQ}' source."
                    )
                )

        if errors:
            exit("\n".join(errors))

    def handle(self, *args, **options):
        """Creates agents and runs the accession gathering process."""
        self.validate_args(options)
        self.set_verbosity_level(options)

        agents = list()
        sources = options["source"] or self.DATA_SOURCES

        if self.DATA_SOURCE_RNA_SEQ in sources:
            agents.append(RNASeqAccessionAgent(options))

        if self.DATA_SOURCE_MA_AE in sources:
            agents.append(MicroArrayExpressAccessionAgent(options))

        if self.DATA_SOURCE_MA_GEO in sources:
            agents.append(MicroArrayGEOAccessionAgent(options))

        entries = set()
        for agent in agents:
            entries.update(agent.collect_data())

        entries = sorted(  # Sort the resulting list.
            (entry for entry in entries if self.RE_ACCESSION.match(entry.code)),
            key=lambda entry: (
                self.RE_ACCESSION.match(entry.code).group(1),
                int(self.RE_ACCESSION.match(entry.code).group(2)),
            ),
        )
        # Limit the number of output entries.
        entries = entries[: options["count"]] if options["count"] else entries

        if options["dry_run"]:
            if entries:
                output = "\n".join((str(entry) for entry in entries))
            else:
                output = "No accessions found."
            print(output)
        else:
            GatheredAccession.objects.bulk_create(entries)
