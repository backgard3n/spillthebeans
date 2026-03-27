# SpillTheBeans
COMPSCI2021 Web Application Development 2 2025-26 - Group Project 
<p align="center">
  <img src="static/images/logo.png" alt="SpillTheBeans Logo" width="140" />
</p>

A Django web application for discovering coffee shops, browsing drinks, and leaving reviews.

This project was created for **COMPSCI2021 / Web Application Development 2** and focuses on a coffee discovery platform with user accounts, shop listings, drink listings, review functionality, and a moderation-style approval flow for shop submissions.

## Features

- Browse approved coffee shops
- Search and filter shops by name, location, and minimum rating
- Browse drinks across all approved shops
- Filter drinks by shop, drink type, minimum rating, search term, and sort order
- View detailed pages for both shops and drinks
- Register, log in, and log out
- View a personal profile page showing your reviews
- Submit one shop review per shop
- Submit one drink review per drink
- Add new shops as an authenticated user
- Edit owned shops and resubmit them for approval
- Add drinks to approved shops as the shop owner
- Home page sections for top-rated shops and top-rated drinks
- Light/dark mode toggle with theme preference saved in local storage
- Seeded demo data for quick testing and marking

## Tech Stack

- **Python 3**
- **Django 4.2.11**
- **SQLite3**
- **Bootstrap 5**
- **Bootstrap Icons**
- **Pillow** for image handling

## Project Structure

```text
spillthebeans/
├── accounts/        # authentication and profile pages
├── config/          # Django project settings and root URLs
├── drinks/          # drink models, views, forms, tests
├── reviews/         # shop and drink review logic
├── shops/           # shop models, views, forms, tests
├── static/          # CSS, JS, images
├── templates/       # HTML templates
├── media/           # uploaded media
├── population_script.py
├── manage.py
└── requirements.txt
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/backgard3n/spillthebeans.git
cd spillthebeans
```

## Setup on Windows

### 1. Create a virtual environment

```powershell
py -m venv .venv
```

### 2. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Apply migrations

```powershell
python manage.py migrate
```

### 5. Populate demo data

```powershell
python population_script.py
```

### 6. Run the development server

```powershell
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Setup on macOS

### 1. Create a virtual environment

```bash
python3 -m venv .venv
```

### 2. Activate the virtual environment

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If `pip` points to Python 2 on your machine, use:

```bash
pip3 install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

If needed:

```bash
python3 manage.py migrate
```

### 5. Populate demo data

```bash
python population_script.py
```

### 6. Run the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Demo / Population Login Details

The population script creates seeded users for testing.

### Shared password for all seeded users

```text
spillthebeans123
```

### Shop owner accounts

- `owner_emma`
- `owner_jamie`
- `owner_nina`
- `owner_callum`

### Reviewer accounts

- `maya`
- `rory`
- `zara`
- `lewis`
- `aisha`
- `ben`
- `chloe`
- `hamish`

## Seeded Data Summary

Running `python population_script.py` creates:

- 12 users and profiles
- 11 shops total
- 10 approved shops visible on the site
- 1 unapproved shop to demonstrate moderation flow
- 40 drinks
- 50 shop reviews
- 120 drink reviews

## Main User Flows

### Browse shops

Visit `/shops/` to:

- search by shop name or location
- filter by minimum rating
- sort by name or rating

### Browse drinks

Visit `/drinks/` to:

- search by drink name or shop name
- filter by shop
- filter by drink type
- filter by minimum rating
- sort by name, top rated, price low-to-high, or price high-to-low

### Reviews

Authenticated users can:

- leave or update one review per shop
- leave or update one review per drink

### Shop submissions

Authenticated users can:

- submit a new shop
- edit a shop they own
- resubmit edited shops for approval

### Drink submissions

Only the owner of an approved shop, or a staff user, can add drinks to that shop.

## Running Tests

Run all tests:

```bash
python manage.py test
```

Run tests for a specific app:

```bash
python manage.py test shops
python manage.py test drinks
python manage.py test reviews
python manage.py test accounts
```

## Optional Admin Setup

To create your own Django admin account:

```bash
python manage.py createsuperuser
```

Then open:

```text
http://127.0.0.1:8000/admin/
```

## Fresh Database Setup

If you want to reset the project locally, delete the SQLite database and rerun migrations.

### Windows

```powershell
Remove-Item db.sqlite3
python manage.py migrate
python population_script.py
```

### macOS

```bash
rm db.sqlite3
python manage.py migrate
python population_script.py
```

## Common Issues

### `No module named django`

Your virtual environment is probably not activated, or dependencies were not installed.

Fix:

```bash
pip install -r requirements.txt
```

### `python` command not found on macOS

Use:

```bash
python3 manage.py runserver
```

### Images are not loading

Make sure the `media/` folder exists and that you are running the project with `DEBUG = True` locally.

### Port already in use

Run the server on a different port:

```bash
python manage.py runserver 8001
```

## External Libraries / Sources

- Django
- Pillow
- Bootstrap 5 via CDN
- Bootstrap Icons via CDN

## Repository

GitHub repository:

```text
https://github.com/backgard3n/spillthebeans
```

## Notes for Submission / Demonstration

For marking or demonstration, the fastest setup flow is:

```bash
pip install -r requirements.txt
python manage.py migrate
python population_script.py
python manage.py runserver
```

Then log in with any of the seeded usernames using the shared password:

```text
spillthebeans123
```
