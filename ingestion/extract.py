from pathlib import Path
from typing import cast

import pymupdf


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = PROJECT_ROOT / "data" / "mahabharatham.pdf"
OUTPUT_PATH = PROJECT_ROOT / "data" / "mahabharatham_raw.txt"


def extract_text() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with pymupdf.open(PDF_PATH) as document, OUTPUT_PATH.open(
        "w", encoding="utf-8"
    ) as output_file:
        print("total pages:", len(document))

        for page_number in range(1, len(document) + 1):
            page = document[page_number - 1]
            output_file.write(f"\n\n--- PAGE {page_number} ---\n\n")
            output_file.write(cast(str, page.get_text("text")))

            if page_number % 100 == 0:
                print("processed:", page_number)

    print("done")


if __name__ == "__main__":
    extract_text()
# for i, page in enumerate(doc):

#     text = page.get_text()

