import json
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "mahabharatham_raw.txt"
OUTPUT_PATH = PROJECT_ROOT / "data" / "chunks.json"
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200
PAGE_MARKER = re.compile(r"--- PAGE (\d+) ---")


def split_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
	if size <= 0:
		raise ValueError("size must be greater than zero")
	if overlap < 0 or overlap >= size:
		raise ValueError("overlap must be non-negative and smaller than size")

	chunks = []
	start = 0
	while start < len(text):
		end = min(start + size, len(text))
		chunk = text[start:end].strip()
		if chunk:
			chunks.append(chunk)
		if end == len(text):
			break
		start = end - overlap
	return chunks


def create_chunks() -> list[dict[str, object]]:
	if not INPUT_PATH.exists():
		raise FileNotFoundError(
			f"Input file not found: {INPUT_PATH}. Run ingestion\\extract.py first."
		)

	raw_text = INPUT_PATH.read_text(encoding="utf-8")
	page_sections = PAGE_MARKER.split(raw_text)
	chunks = []

	for index in range(1, len(page_sections), 2):
		page_number = int(page_sections[index])
		page_text = page_sections[index + 1]
		for chunk_number, text in enumerate(split_text(page_text), start=1):
			chunks.append(
				{
					"id": f"page-{page_number}-chunk-{chunk_number}",
					"page": page_number,
					"text": text,
				}
			)

	OUTPUT_PATH.write_text(json.dumps(chunks, ensure_ascii=False, indent=2), encoding="utf-8")
	return chunks


if __name__ == "__main__":
	chunks = create_chunks()
	print(f"created {len(chunks)} chunks at {OUTPUT_PATH}")
