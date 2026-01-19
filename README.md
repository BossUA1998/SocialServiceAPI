# Social Media API

A powerful RESTful API service for a social network, built with **Django REST Framework**. The project provides a full range of features for user interaction: from profile creation and content publishing to a subscription system, likes, and comments.

## 🚀 Key Features

### 👤 Users & Authentication
* **Registration & Login:** Full support for **JWT authentication** (access & refresh tokens).
* **Profile Management:** Ability to update biography, avatar, and personal data.
* **Logout:** Implemented token blacklisting for secure logout.
* **Search:** Search users by username.

### 📱 Social Interaction
* **Subscriptions:** Followers/Following system. Ability to follow and unfollow other authors.
* **Feed:** View posts from authors you follow.

### 📝 Posts & Content
* **CRUD for Posts:** Create, read, update, and delete posts.
* **Media:** Image upload and processing for posts and avatars (using UUIDs for unique filenames).
* **Hashtags:** Automatic recognition, creation, and filtering of hashtags.
* **Likes:** Ability to add and remove likes.
* **Comments:** Add comments to publications.

### 🛠 Technical Highlights
* **Permissions:** Custom permissions (e.g., `IsAuthorOrReadOnly`) ensuring data security (only the author can edit their post).
* **Documentation:** Automatic generation of interactive documentation via **Swagger UI** and **Redoc** (drf-spectacular).
* **Optimization:** usage of `select_related` and `prefetch_related` to avoid N+1 query problems.

## 🛠 Tech Stack

* **Python 3.10+**
* **Django 5+**
* **Django REST Framework**
* **Simple JWT** (Authentication)
* **PostgreSQL** (Recommended DB)
* **Docker** (Optional)

## ⚙️ Installation & Setup

Follow these steps to run the project locally:
1. **Clone the repository:**
   ```bash
   git clone https://github.com/BossUA1998/SocialMediaAPI.git
   ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

5. **Run the development server:**
    ```bash
   python manage.py runserver
   ```
