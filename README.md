# FreshCart 🛒

A shared family grocery and recipe management app. Create lists, track bought items, manage inventory, and plan meals with recipes — all in real time. Built with Django and HTMX.

---

## Features

- **Shared grocery lists** — create and manage lists together as a family
- **Buy tracking** — mark items as bought, sorted automatically to the bottom
- **Inventory** — bought items appear in your inventory with quantity tracking
- **Mark as used** — track how much of an item has been used
- **Recipes** — create recipes with ingredients and quantities
- **Recipe shopping lists** — each recipe gets its own automatic shopping list
- **Reusable products** — products are stored once and reused across lists
- **Filter & sort** — filter by bought/unbought status or by store
- **Inline editing** — edit items without leaving the page
- **Real time updates** — powered by HTMX, no full page reloads
- **User authentication** — register, login, logout

---

## Tech Stack

- **Backend** — Django 4.2
- **Frontend** — HTMX 1.9, vanilla CSS
- **Database** — SQLite (development)
- **Auth** — Django built-in authentication

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/freshcart.git
cd freshcart
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv

# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run migrations**
```bash
cd groceryproject
python manage.py migrate
```

**5. Create a superuser**
```bash
python manage.py createsuperuser
```

**6. Run the development server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---

## Project Structure

```
groceryproject/
├── grocery/
│   ├── models.py        # Product, GroceryList, GroceryItem, Recipe, RecipeIngredients
│   ├── views.py         # All view logic
│   ├── forms.py         # Django forms
│   ├── urls.py          # URL routing
│   ├── admin.py         # Admin registration
│   └── templates/
│       ├── grocery/     # App templates
│       └── registration/ # Auth templates
├── groceryproject/
│   ├── settings.py
│   └── urls.py
└── manage.py
```

---

## Usage

1. Register an account or log in
2. Create a grocery list from the homepage
3. Add items to your list with quantity and unit
4. Mark items as bought while shopping
5. Bought items appear in your inventory
6. Create recipes and add ingredients
7. Each recipe gets its own shopping list automatically
