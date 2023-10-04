from sklearn.feature_extraction.text import TfidfVectorizer
from rank_bm25 import BM25Okapi
from sklearn.metrics.pairwise import cosine_similarity
import os

# Mendefinisikan path ke direktori dokumen
documents_folder = r'D:/kuliah/Semester 5/Penelusuran Informasi/coba/output_folder'

# Inisialisasi list untuk menyimpan teks dari dokumen
documents = []

# Loop melalui semua file dalam direktori dan baca teksnya
for file_name in os.listdir(documents_folder):
    if file_name.endswith('.txt'):
        file_path = os.path.join(documents_folder, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            document_text = file.read()
            documents.append(document_text)

# Membuat vektor TF-IDF
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

# Membuat model BM25
corpus = [doc.split() for doc in documents]
bm25_model = BM25Okapi(corpus)


# # User memasukkan query
query = input("Masukkan query: ")

# Mengubah query menjadi vektor TF-IDF
query_vector = tfidf_vectorizer.transform([query])

# Menghitung skor kesamaan (cosine similarity) antara query dan dokumen menggunakan TF-IDF
tfidf_similarities = cosine_similarity(query_vector, tfidf_matrix)

# Menghitung skor BM25
query_tokens = query.split()
bm25_scores = bm25_model.get_scores(query_tokens)

# Kombinasi bobot untuk menggabungkan hasil TF-IDF dan BM25
alpha = 0.7  # Bobot untuk TF-IDF
beta = 0.3   # Bobot untuk BM25

combined_scores = alpha * tfidf_similarities + beta * bm25_scores

# Mendapatkan indeks dokumen dengan skor tertinggi
top_document_indices = combined_scores.argsort()[0][::-1][:20]  # Ambil 20 dokumen teratas

# Menampilkan hasil
print(f"Hasil pencarian dari TF-IDF dan BM25:")
for idx in top_document_indices:
    combined_similarity = combined_scores[0][idx]
    cosine_sim = tfidf_similarities[0][idx]
    bm25_score = bm25_scores[idx]
    if combined_similarity > 0 and cosine_sim > 0 and bm25_score > 0:
        file_name = os.listdir(documents_folder)[idx]
        print(f"Judul Dokumen: {file_name}")
        print(f"Combined Similarity: {combined_similarity}")
        print(f"cosine similarity: {cosine_sim}")
        print(f"BM25 Score: {bm25_score}")
        print()
