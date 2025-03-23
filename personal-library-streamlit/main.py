import json
import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Personal Library Manager",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for colorful styling and footer
st.markdown("""
    <style>
    /* Sidebar background */
    .css-1d391kg { background-color: #f0f8ff; }
    /* Main background */
    .stApp { background-color: #f9f9f9; }
    /* Buttons */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    /* Headers */
    h1 { color: #2c3e50; }
    h2 { color: #e74c3c; }
    /* Text inputs */
    .stTextInput>div>input {
        border: 2px solid #3498db;
        border-radius: 5px;
    }
    /* Success, Error, Info messages */
    .stSuccess { background-color: #d4edda; color: #155724; }
    .stError { background-color: #f8d7da; color: #721c24; }
    .stInfo { background-color: #cce5ff; color: #004085; }
    /* Footer styling */
    .sidebar-footer {
        position: fixed;
        bottom: 10px;
        left: 10px;
        width: 320px;
        background-color: #3498db;
        color: white;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

class BookCollection:
    """A class to manage a collection of books."""
    def __init__(self):
        self.books_list = []
        self.storage_file = "books-data.json"
        self.read_from_storage()

    def read_from_storage(self):
        try:
            with open(self.storage_file, "r") as f:
                self.books_list = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.books_list = []

    def write_to_storage(self):
        with open(self.storage_file, "w") as f:
            json.dump(self.books_list, f, indent=4)

    def add_new_book(self):
        st.subheader("➕ Add a New Book 🌟")
        with st.form(key="add_book_form"):
            book_title = st.text_input("Title 🌈", placeholder="e.g., Next.js Guide")
            book_author = st.text_input("Author ✍️", placeholder="e.g., Muhammad Farooq")
            book_year = st.text_input("Year 📅", placeholder="e.g., 2025")
            book_genre = st.selectbox("Genre 🎨", ["Programming", "Fiction", "Non-Fiction", "Fantasy", "Biography", "Other"])
            is_book_read = st.radio("Have you read it? 📖", ["No", "Yes"], horizontal=True) == "Yes"
            submit_button = st.form_submit_button(label="Add Book 📚")

        if submit_button and book_title and book_author:
            new_book = {
                "title": book_title,
                "author": book_author,
                "year": book_year,
                "genre": book_genre,
                "read": is_book_read
            }
            self.books_list.append(new_book)
            self.write_to_storage()
            st.success(f"✅ Book '{book_title}' added successfully!")
        elif submit_button:
            st.error("⚠️ Title and Author are required!")

    def delete_book(self):
        st.subheader("🗑️ Delete a Book 🔥")
        book_title = st.text_input("Enter the book title to delete", key="delete_title")
        if st.button("Delete Book 🗑️"):
            for book in self.books_list[:]:
                if book["title"].lower() == book_title.lower():
                    self.books_list.remove(book)
                    self.write_to_storage()
                    st.success(f"✅ Book '{book_title}' deleted!")
                    return
            st.error("❌ Book not found!")

    def find_book(self):
        st.subheader("🔍 Find a Book 🌍")
        search_type = st.selectbox("Search by", ["Title", "Author"], key="search_type")
        search_term = st.text_input("Search term", key="search_term")
        if st.button("Search 🔎"):
            found_books = [
                book for book in self.books_list
                if search_term.lower() in book[search_type.lower()].lower()
            ]
            if found_books:
                st.write("📋 Found Books:")
                for i, book in enumerate(found_books, 1):
                    status = "✅ Read" if book["read"] else "⏳ Not Read"
                    st.markdown(f"{i}. **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {status}", unsafe_allow_html=True)
            else:
                st.info("ℹ️ No books found.")

    def update_book(self):
        st.subheader("✏️ Update a Book 🛠️")
        book_title = st.text_input("Enter the book title to update", key="update_title")

        if st.button("Find Book 🔍", key="find_update"):
            for book in self.books_list:
                if book["title"].lower() == book_title.lower():
                    # Store book in session state for editing
                    st.session_state['book_to_update'] = book
                    st.session_state['show_form'] = True
                    break
            else:
                st.error("❌ Book not found!")
                st.session_state['show_form'] = False

        if 'show_form' in st.session_state and st.session_state['show_form']:
            book = st.session_state['book_to_update']
            with st.form(key="update_book_form"):
                st.write(f"Editing '{book['title']}' - Leave fields unchanged if not modifying.")
                new_title = st.text_input("New Title 🌟", value=book["title"])
                new_author = st.text_input("New Author ✍️", value=book["author"])
                new_year = st.text_input("New Year 📅", value=book["year"])
                new_genre = st.selectbox("New Genre 🎨", ["Programming", "Fiction", "Non-Fiction", "Fantasy", "Biography", "Other"], 
                                       index=["Programming", "Fiction", "Non-Fiction", "Fantasy", "Biography", "Other"].index(book["genre"]))
                new_read = st.radio("Have you read it? 📖", ["No", "Yes"], index=1 if book["read"] else 0, horizontal=True) == "Yes"
                update_button = st.form_submit_button(label="Update Book ✏️")

                if update_button:
                    # Find and update book in self.books_list
                    for stored_book in self.books_list:
                        if stored_book["title"].lower() == book["title"].lower():
                            stored_book.update({
                                "title": new_title,
                                "author": new_author,
                                "year": new_year,
                                "genre": new_genre,
                                "read": new_read
                            })
                            break  # Exit loop after updating

                    self.write_to_storage()
                    st.success(f"✅ Book '{new_title}' updated successfully!")
                    # Reset form state
                    del st.session_state['book_to_update']
                    st.session_state['show_form'] = False

    def show_list_books(self):
        st.subheader("📖 Your Book List 📚")
        if not self.books_list:
            st.info("ℹ️ Your library is empty. Add some books!")
        else:
            for i, book in enumerate(self.books_list, 1):
                status = "✅ Read" if book["read"] else "⏳ Not Read"
                st.markdown(f"{i}. **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {status}", unsafe_allow_html=True)

    def show_reading_progress(self):
        st.subheader("📊 Reading Progress 🌈")
        total_books = len(self.books_list)
        read_books = sum(1 for book in self.books_list if book["read"])
        completion_percentage = (read_books / total_books) * 100 if total_books > 0 else 0
        st.write(f"📚 Total Books: **{total_books}**")
        st.write(f"✅ Books Read: **{read_books}**")
        st.progress(completion_percentage / 100)
        st.markdown(f"🎯 Reading Progress: **{completion_percentage:.2f}%**", unsafe_allow_html=True)

def main():
    book_collection = BookCollection()

    # Colorful header
    st.title("📚 Personal Library Manager")
    st.markdown("<h3 style='color: #3498db;'>Organize your books with style! 🌟</h3>", unsafe_allow_html=True)

    # Sidebar with menu and footer
    st.sidebar.markdown("### Menu 📋")
    menu = st.sidebar.radio(
        "Select an option",
        [
            "➕ Add a New Book",
            "🗑️ Delete a Book",
            "🔍 Find a Book",
            "✏️ Update a Book",
            "📖 Show Book List",
            "📊 Show Reading Progress"
        ],
        label_visibility="hidden",
        format_func=lambda x: f"{x}"
    )

    # Add footer in sidebar with colorful GitHub link
    st.sidebar.markdown(
        """
        <div class="sidebar-footer">
            Made with ❤️ by Muhammad Farooq | © 2025<br>
            <a href="https://github.com/Muhammad-Farooq" target="_blank" style="color: #ffeb3b; text-decoration: none;">
                GitHub 🌐
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Execute selected option
    if menu == "➕ Add a New Book":
        book_collection.add_new_book()
    elif menu == "🗑️ Delete a Book":
        book_collection.delete_book()
    elif menu == "🔍 Find a Book":
        book_collection.find_book()
    elif menu == "✏️ Update a Book":
        book_collection.update_book()
    elif menu == "📖 Show Book List":
        book_collection.show_list_books()
    elif menu == "📊 Show Reading Progress":
        book_collection.show_reading_progress()

if __name__ == "__main__":
    main()