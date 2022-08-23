import os
from datetime import datetime
from pathlib import Path

import pdfkit
from jinja2 import Environment, FileSystemLoader


# TODO GLE A lot more thought needs to be added to the report/notfication.
class ReportGenerator:
    def __init__(self, working_dir, template: str, evaluation: dict, date_ranges: dict):
        self.template = template

        filename_base = (
            evaluation["profile"].metric_name
            + (
                "_" + evaluation["profile"].app_name
                if evaluation["profile"].app_name is not None
                else ""
            )
            + "_"
            + date_ranges.get("recent_period").get("end_date").strftime("%Y-%m-%d")
        )
        self.output_html = os.path.join(working_dir, filename_base + ".html")
        self.output_pdf = os.path.join(working_dir, filename_base + ".pdf")
        self.evaluation = evaluation
        self.date_ranges = date_ranges

    def build_html_report(self):
        self.evaluation["creation_time"] = str(datetime.now())
        p = Path(__file__).parent / "templates"
        env = Environment(loader=FileSystemLoader(p))
        template = env.get_template(self.template)

        with open(self.output_html, "w") as fh:
            fh.write(
                template.render(
                    evaluation=self.evaluation,
                    date_ranges=self.date_ranges,
                )
            )

    # requires the html file to be created, will create if not available
    # returns relative path of pdf file.
    def build_pdf_report(self) -> str:
        self.build_html_report()
        options = {"enable-local-file-access": None}
        pdfkit.from_file(
            self.output_html,
            self.output_pdf,
            options=options,
            css="./analysis/reports/templates/4.3.1.bootstrap.min.css",
            verbose=True,
        )
        return self.output_pdf
