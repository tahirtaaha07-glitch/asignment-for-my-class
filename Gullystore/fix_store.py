import json
import os

def rebuild_database():
    products = []
    # High-quality tech images from Unsplash to make the store look pro
    tech_images = [
        "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=500",
        "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=500",
        "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=500",
        "https://images.unsplash.com/photo-1555680202-c86f0e12f086?w=500"
    ]
    
    categories = ["Gaming GPU", "Core Processor", "DDR4 RAM", "NVMe SSD", "Motherboard"]
    brands = ["ASUS", "MSI", "Nvidia", "AMD", "Intel", "Samsung", "Corsair"]

    # Generate 1,000 professional items
    for i in range(1, 1001):
        cat = categories[i % len(categories)]
        brand = brands[i % len(brands)]
        img = tech_images[i % len(tech_images)]
        
        product = {
            "id": i,
            "name": f"{brand} {cat} Series-{i}",
            "specs": f"High-end {cat} for pro gaming and rendering. Version {i}.",
            "price": 4500 + (i * 120),
            "image": img
        }
        products.append(product)

    # The structure must look exactly like this for main.py to read it
    db_data = {
        "users": {"admin": "1234"},
        "products": products
    }

    with open("data.json", "w") as f:
        json.dump(db_data, f, indent=4)
    
    # Also fix the missing orders file while we are at it
    if not os.path.exists("orders.json"):
        with open("orders.json", "w") as f:
            json.dump([], f)

    print("✅ Success! 1,000 items created. Refresh your browser now.")

if __name__ == "__main__":
    rebuild_database()