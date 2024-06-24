import streamlit as st
import pandas as pd
import datetime as dt
import time

# Initialize session state for user login, role, book issue, and user database
if 'users' not in st.session_state:
    st.session_state.users = {}
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False
if 'books_df' not in st.session_state:
    books_data = [
        {"title": "Book 1", "status": "Available"},
        {"title": "Book 2", "status": "Available"},
        {"title": "Book 3", "status": "Available"},
        {"title": "Book 4", "status": "Available"},
        {"title": "Book 5", "status": "Available"},
        {"title": "Book 6", "status": "Available"},
        {"title": "Book 7", "status": "Available"},
        {"title": "Book 8", "status": "Available"},
        {"title": "Book 9", "status": "Available"},
        {"title": "Book 10", "status": "Available"},
    ]
    st.session_state.books_df = pd.DataFrame(books_data)

# Function for login/signup page
def login_signup():
    st.sidebar.title("Welcome to Codeyoung Library")
    option = st.sidebar.selectbox("Choose option", ["Login", "Signup"])
    role = st.sidebar.selectbox("Select Role", ["Customer", "Admin"])
    
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if option == "Signup":
        if st.sidebar.button("Signup"):
            if username and password:
                st.session_state.users[username] = {"password": password, "role": role}
                st.sidebar.success("Signup successful! You can now log in.")
            else:
                st.sidebar.error("Please enter both username and password.")
    elif option == "Login":
        if st.sidebar.button("Login"):
            if username in st.session_state.users and st.session_state.users[username]['password'] == password:
                st.session_state.user_role = st.session_state.users[username]['role']
                st.session_state.username = username
                st.session_state.is_logged_in = True
                st.sidebar.success(f"Welcome, {username}!")
            else:
                st.sidebar.error("Invalid username or password.")
    if st.sidebar.button("Logout"):
        st.session_state.is_logged_in = False
        st.session_state.user_role = None
        st.session_state.username = None
        with st.spinner("Logging out..."):
            time.sleep(2)
            st.sidebar.success("Logged out successfully. Redirecting to home page...")
            time.sleep(2)

# Function to show available books for customers
def show_books():
    st.header("Available Books")
    available_books = st.session_state.books_df
    for index, row in available_books.iterrows():
        color = "green" if row['status'] == 'Available' else "red"
        st.markdown(f"<span style='color:{color};'>{row['title']} - {row['status']}</span>", unsafe_allow_html=True)
        st.image("https://via.placeholder.com/150", caption=row['title'], use_column_width=True)
        if row['status'] == 'Available' and st.button(f"Select {row['title']} to issue", key=f"select_{index}"):
            st.session_state.books_df.at[index, 'status'] = 'Issued'
            issue_book(row['title'])

# Function to handle book issue
def issue_book(book_title):
    st.write(f"Issuing {book_title}")
    selected_date = st.date_input("Select Issue Date", key="issue_date")
    selected_time = st.time_input("Select Issue Time", key="issue_time")
    return_date = st.date_input("Select Return Date", key="return_date")
    return_time = st.time_input("Select Return Time", key="return_time")
    if st.button("Issue Book"):
        with st.spinner("Processing..."):
            time.sleep(5)
            st.balloons()
            st.success(f"Book '{book_title}' issued successfully!")
            st.write(f"Issued Date: {selected_date}")
            st.write(f"Issued Time: {selected_time}")
            st.write(f"Return Date: {return_date}")
            st.write(f"Return Time: {return_time}")

# Function to handle book return
def return_book():
    st.write("Return Details")
    issued_books = st.session_state.books_df[st.session_state.books_df['status'] == 'Issued']
    books_to_return = st.multiselect("Select Books to Return", issued_books['title'].tolist(), key="books_to_return")
    return_date = st.date_input("Select Return Date", key="return_date_return")
    return_time = st.time_input("Select Return Time", key="return_time_return")
    if st.button("Return Book"):
        with st.spinner("Processing..."):
            time.sleep(5)
            st.balloons()
            st.success("Books returned successfully!")
            st.write(f"Return Date: {return_date}")
            st.write(f"Return Time: {return_time}")
            for book in books_to_return:
                st.session_state.books_df.loc[st.session_state.books_df['title'] == book, 'status'] = 'Available'

# Function to display admin panel
def admin_panel():
    st.header("Admin Panel")
    st.bar_chart(st.session_state.books_df['status'].value_counts())
    new_book = st.text_input("New Book Title")
    if st.button("Add Book"):
        if new_book:
            st.session_state.books_df.loc[len(st.session_state.books_df)] = [new_book, "Available"]
            st.success(f"Book '{new_book}' added to library.")
        else:
            st.error("Please enter a book title.")

# Function to display contact us page
def contact_us():
    st.header("About Us")
    st.write("""
    Welcome to Codeyoung Library! We are dedicated to providing a vast collection of books for all age groups. 
    Our library offers a comfortable and quiet environment for reading and studying. We also provide digital 
    resources and online access to our catalog. Our friendly staff is here to assist you with any queries and 
    help you find the perfect book. Join us and explore the world of knowledge at Codeyoung Library.
    """)
    st.write("Contact Number: +917906116356")
    st.write("Email: amu.aman19@gmail.com")
    st.write("Address: Pune, India")
    st.markdown("""
    <iframe 
        src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3782.9626577475274!2d73.85674311438226!3d18.520430687413616!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bc2c1a0bb97b7ef%3A0x9938e6d6bda2951b!2sPune%2C%20Maharashtra%2C%20India!5e0!3m2!1sen!2sus!4v1623148577984!5m2!1sen!2sus" 
        width="600" 
        height="450" 
        style="border:0;" 
        allowfullscreen="" 
        loading="lazy">
    </iframe>
    """, unsafe_allow_html=True)

# Main function
def main():
    login_signup()
    nav = st.sidebar.selectbox("Navigation", ["Home", "Contact Us"])
    
    if nav == 'Contact Us':
        contact_us()
    elif st.session_state.is_logged_in:
        if st.session_state.user_role == "Customer":
            show_books()
            return_book()
        elif st.session_state.user_role == "Admin":
            admin_panel()
    else:
        st.title('Welcome to Codeyoung Library!')
        st.write(" Please login or signup to continue.")
        st.image("X:\streamlit\project\Codeyoung Background x HT (1).jpg", caption="#ReadToLearn", use_column_width=True)
        total_books = len(st.session_state.books_df)
        issued_books = len(st.session_state.books_df[st.session_state.books_df['status'] == 'Issued'])
        st.slider("Books Issued", min_value=0, max_value=total_books, value=issued_books, disabled=True)

if __name__ == "__main__":
    main()
