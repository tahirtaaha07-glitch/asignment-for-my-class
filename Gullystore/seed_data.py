import json

products = []
categories = ["Graphic Card (GPU)", "Processor (CPU)", "Gaming RAM", "NVMe SSD", "Motherboard"]
brands = ["ASUS", "MSI", "Gigabyte", "Intel", "AMD", "Corsair", "Samsung"]

# This loop creates 1000 items automatically
for i in range(1, 1001):
    cat = categories[i % len(categories)]
    brand = brands[i % len(brands)]
    
    product = {
        "id": i,
        "name": f"{brand} Pro-Series {cat} v{i}",
        "specs": f"High-performance {cat} for gaming and development. Gen {i//100 + 1}",
        "price": 5000 + (i * 150),  # Generates different prices
        "image": f"https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?q=80&w=400&auto=format&fit=crop" # High quality tech image
    }
    products.append(product)

db = {
    "users": {"admin": "1234"},
    "products": products
}

with open("data.json", "w") as f:
    json.dump(db, f, indent=4)

print("✅ Success! data.json now has 1,000 computer parts.")