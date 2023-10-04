import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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

# User memasukkan query
query = input("Masukkan query: ")

# Mengubah query menjadi vektor TF-IDF
query_vector = tfidf_vectorizer.transform([query])

# Menghitung skor kesamaan (cosine similarity) antara query dan dokumen
similarities = cosine_similarity(query_vector, tfidf_matrix)

# Mendapatkan indeks dokumen dengan skor tertinggi
top_document_indices = similarities.argsort()[0][::-1][:20]  # Ambil 20 dokumen teratas


# Menampilkan hasil
print(f"Hasil pencarian dari TF-IDF:")
for idx in top_document_indices:
    print(f"Judul Dokumen: {os.listdir(documents_folder)[idx]}, Similarity: {similarities[0][idx]}")
