import json
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "chunks.json"
VECTORSTORE_PATH = PROJECT_ROOT / "vectorstore"
INDEX_PATH = VECTORSTORE_PATH / "mahabharatham.index"
METADATA_PATH = VECTORSTORE_PATH / "metadata.json"
MODEL_NAME = "all-MiniLM-L6-v2"
BATCH_SIZE = 64


def create_embeddings() -> None:
	if not INPUT_PATH.exists():
		raise FileNotFoundError(
			f"Input file not found: {INPUT_PATH}. Run ingestion\\chunk.py first."
		)

	chunks = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
	if not chunks:
		raise ValueError(f"No chunks found in {INPUT_PATH}")

	texts = [chunk["text"] for chunk in chunks]
	print(f"loading embedding model: {MODEL_NAME}")
	model = SentenceTransformer(MODEL_NAME)
	vectors = model.encode(
		texts,
		batch_size=BATCH_SIZE,
		show_progress_bar=True,
		convert_to_numpy=True,
		normalize_embeddings=True,
	).astype("float32")

	index = faiss.IndexFlatIP(vectors.shape[1])
	index.add(vectors)
	VECTORSTORE_PATH.mkdir(parents=True, exist_ok=True)
	faiss.write_index(index, str(INDEX_PATH))
	METADATA_PATH.write_text(
		json.dumps(chunks, ensure_ascii=False, indent=2), encoding="utf-8"
	)
	print(f"created {index.ntotal} vectors at {INDEX_PATH}")


if __name__ == "__main__":
	create_embeddings()
        