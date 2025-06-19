from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Load and preprocess the data
df = pd.read_csv("Dataset .csv")
df = df.dropna(subset=['Cuisines', 'City', 'Average Cost for two', 'Aggregate rating'])
df['Cuisines'] = df['Cuisines'].str.strip().str.lower()
df['City'] = df['City'].str.strip()
df['Country Code'] = df['Country Code'].astype(int)

# Cuisine images
CUISINE_IMAGES = {
    "italian": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRLVSY1AP83B_HFSbhBn7v6hto6W-gGVzQ3jA&s",
    "southindian": "https://restaurantindia.s3.ap-south-1.amazonaws.com/s3fs-public/content6054.jpg",
    "northindian": "https://res.cloudinary.com/hz3gmuqw6/image/upload/c_fill,q_auto,w_750/f_auto/North-Indian-food-phpUPkVj5",
    "chinese": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRi9DiVo-DH1TH9Ck9Ui8ZIU11E2PO3ZuaoZg&s",
    "japanese": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTdOlAbVW2gV9WmuwI6pmmjJUZ5XoNxvEkL2g&s",
    "mexican": "https://cloudfront-us-east-1.images.arcpublishing.com/ajc/5ULFVCWWNFHD3NYXDEPGUZWL2Q.jpg",
    "bakery": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS6gtJ3URQ1HLfL5PcZq3KsWXEyAT7Bo1u4bA&s",
    "fast food": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR75oqEsVn2OYLvdjAOnHbdhZcc_j3F9YSUcg&s",
    "thai": "https://cdn.shopify.com/s/files/1/0976/3044/files/thai-food-ingredients-v2.png?v=1643515319",
    "korean": "https://c.ndtvimg.com/2022-05/7efvlvl_korean-rice-cakes_625x300_13_May_22.jpg?im=FaceCrop,algorithm=dnn,width=1200,height=675",
    "seafood": "https://www.licious.in/blog/wp-content/uploads/2022/02/shutterstock_1773695441-min-750x750.jpg",
    "bevarages": "https://eu-images.contentstack.com/v3/assets/blt7a82e963f79cc4ec/blt60803213ffe6589c/66ec2f2d00900379f7caf243/beverages.png",
    "default": "https://img.freepik.com/free-photo/flat-lay-table-full-delicious-food-arrangement_23-2149141378.jpg?semt=ais_hybrid&w=740"
}

# Recommendation logic
def recommend_restaurants(country_code, city, cuisine, preferred_cost, preferred_rating, top_n=10):
    cuisine = cuisine.lower()
    filtered = df[
        (df['Country Code'] == int(country_code)) &
        (df['City'].str.lower() == city.lower()) &
        (df['Cuisines'].str.contains(cuisine, na=False))
    ].copy()

    if filtered.empty:
        return []

    cost_diff = (filtered['Average Cost for two'] - preferred_cost).abs()
    rating_diff = (filtered['Aggregate rating'] - preferred_rating).abs()

    cost_norm = (cost_diff - cost_diff.min()) / (cost_diff.max() - cost_diff.min() + 1e-5)
    rating_norm = (rating_diff - rating_diff.min()) / (rating_diff.max() - rating_diff.min() + 1e-5)

    filtered['score'] = cost_norm + rating_norm
    filtered_sorted = filtered.sort_values('score').head(top_n)

    return [
        {
            "name": row['Restaurant Name'],
            "locality": row['Locality']
        }
        for _, row in filtered_sorted.iterrows()
    ]

@app.route('/')
def index():
    df_clean = df[['Country Code', 'City', 'Cuisines']].dropna()
    countries = sorted(df_clean['Country Code'].unique().tolist())

    cities_by_country = (
        df_clean.groupby('Country Code')['City']
        .unique().apply(list).to_dict()
    )

    cuisines_by_city = (
        df_clean.groupby('City')['Cuisines']
        .apply(lambda x: list(set(c.strip() for s in x.dropna() for c in s.split(','))))
        .to_dict()
    )

    return render_template(
        'index.html',
        countries=countries,
        cities_by_country=cities_by_country,
        cuisines_by_city=cuisines_by_city
    )

@app.route('/results', methods=['POST'])
def show_results():
    country = request.form['country']
    city = request.form['city']
    cuisine = request.form['cuisine']
    cost = float(request.form['cost'])
    rating = float(request.form['rating'])

    recommendations = recommend_restaurants(country, city, cuisine, cost, rating)

    image_url = CUISINE_IMAGES.get(cuisine.strip().lower(), CUISINE_IMAGES["default"])

    return render_template(
        'results.html',
        recommendations=recommendations,
        cuisine=cuisine,
        image_url=image_url
    )

if __name__ == '__main__':
    app.run(debug=True)  