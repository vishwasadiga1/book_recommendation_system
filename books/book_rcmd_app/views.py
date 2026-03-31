import pickle
from django.shortcuts import render
import numpy as np

# load data
popular_df = pickle.load(open('popular.pkl', 'rb'))

def index(request):
    data = []

    for i in range(len(popular_df)):
        item = [
            popular_df.iloc[i]['Book-Title'],
            popular_df.iloc[i]['Book-Author'],
            popular_df.iloc[i]['Image-URL-M'],
            popular_df.iloc[i]['num_ratings'],
            round(popular_df.iloc[i]['avg_ratings'], 1)
        ]
        data.append(item)

    return render(request, 'index.html', {'popular_books': data})

pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))



def recommend_ui(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input').strip()

        # Case-insensitive exact match
        matches = [book for book in pt.index if book.lower() == user_input.lower()]

        # If no exact match → try partial match
        if not matches:
            matches = [book for book in pt.index if user_input.lower() in book.lower()]

        # If still nothing → show error
        if not matches:
            return render(request, 'recommend.html', {'error': "No similar books found"})

        # Use matched book
        book_name = matches[0]

        # Get index safely
        index = np.where(pt.index == book_name)[0][0]

        similar_items = sorted(
            list(enumerate(similarity_scores[index])),
            key=lambda x: x[1],
            reverse=True
        )[1:6]

        data = []
        for i in similar_items:
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]

            if temp_df.empty:
                continue  # to avoid crash

            temp_df = temp_df.drop_duplicates('Book-Title')

            item = [
                temp_df['Book-Title'].values[0],
                temp_df['Book-Author'].values[0],
                temp_df['Image-URL-M'].values[0]
            ]
            data.append(item)

        return render(request, 'recommend.html', {'data': data})

    return render(request, 'recommend.html')