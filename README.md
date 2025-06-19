# 🍽️ Restaurant Recommendation System

This is a web-based restaurant recommendation system built using **Flask** and **Pandas**. It recommends restaurants based on user preferences like country, city, cuisine, cost, and rating. The results are displayed beautifully with cuisine-specific images and locality details.

---

## 🚀 Features

- 🌍 Country and city-based filtering
- 🍜 Cuisine-specific recommendations
- 💵 Cost and ⭐ rating-based ranking
- 📸 Cuisine-themed images
- 🧾 Simple, clean interface built with HTML & CSS
- 🔁 Cascading dropdowns for dynamic filtering

---

## 🧠 How It Works

1. The user selects:
   - Country
   - City
   - Cuisine
   - Average cost for two
   - Desired rating

2. The system:
   - Filters restaurants based on inputs
   - Scores them based on similarity to cost & rating preferences
   - Displays top 10 matches as cards

---

## 🧰 Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS (inline styles)
- **Data**: Preprocessed CSV file (`Dataset .csv`)
- **Recommendation Type**: Content-based filtering (non-ML)

---

## 📁 Project Structure

restaurant-recommendation/
├── app.py           

├── Dataset .csv          # Dataset (restaurant data)

├── static/

   └── style.css         # External CSS for styling

├── templates/

   ├── index.html        # Home page (form input)

   └── results.html      # Recommendations display


## Commands

pip install flask pandas

python app.py

In web browser localhost:5000
