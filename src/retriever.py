import numpy as np
import faiss

from sentence_transformers import SentenceTransformer


class ContractRetriever:

    def __init__(self, model_name):

        self.model = SentenceTransformer(
            model_name
        )

        self.chunks = []
        self.index = None

    # --------------------------------------------------
    # CREATE DOCUMENT CHUNKS
    # --------------------------------------------------

    def create_chunks(
        self,
        text,
        chunk_size=1200,
        chunk_overlap=150
    ):

        words = text.split()

        chunks = []

        start = 0

        while start < len(words):

            end = start + chunk_size

            chunk = " ".join(
                words[start:end]
            )

            if chunk.strip():
                chunks.append(chunk)

            start = end - chunk_overlap

        self.chunks = chunks

        return chunks

    # --------------------------------------------------
    # BUILD FAISS INDEX
    # --------------------------------------------------

    def build_index(self):

        if not self.chunks:

            raise ValueError(
                "No document chunks available."
            )

        embeddings = self.model.encode(
            self.chunks,
            normalize_embeddings=True,
            show_progress_bar=False
        )

        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(
            dimension
        )

        self.index.add(
            embeddings
        )

    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------

    def search(
        self,
        query,
        top_k=5
    ):

        if self.index is None:

            raise ValueError(
                "FAISS index has not been created."
            )

        if not self.chunks:

            raise ValueError(
                "No document chunks available."
            )

        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True,
            show_progress_bar=False
        )

        query_embedding = np.asarray(
            query_embedding,
            dtype="float32"
        )

        # Don't request more results than chunks available
        top_k = min(
            top_k,
            len(self.chunks)
        )

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0]
        ):

            if index == -1:
                continue

            results.append(
                {
                    "text": self.chunks[index],
                    "score": float(score)
                }
            )

        return results

    # --------------------------------------------------
    # GET CONTEXT FOR GEMINI
    # --------------------------------------------------

    def get_context(
        self,
        query,
        top_k=5
    ):

        results = self.search(
            query,
            top_k
        )

        context_parts = []

        for i, result in enumerate(
            results,
            start=1
        ):

            context_parts.append(
                f"[PASSAGE {i}]\n"
                f"{result['text']}"
            )

        return "\n\n".join(
            context_parts
        )