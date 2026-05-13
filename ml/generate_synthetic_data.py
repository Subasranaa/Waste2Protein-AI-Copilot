import numpy as np
import pandas as pd
from pathlib import Path


np.random.seed(42)

N = 1200

waste_types = [
    "fruit_waste",
    "vegetable_waste",
    "brewery_waste",
    "dairy_waste",
    "mixed_agri_waste",
]

locations = ["Leeds", "Manchester", "Birmingham", "London", "Glasgow"]

data = []

for _ in range(N):
    waste_type = np.random.choice(waste_types)
    location = np.random.choice(locations)

    sugar_content = np.random.uniform(5, 35)
    nitrogen_content = np.random.uniform(0.5, 5.0)
    moisture = np.random.uniform(45, 90)
    ph = np.random.uniform(4.0, 8.5)
    temperature = np.random.uniform(20, 42)
    fermentation_time = np.random.uniform(12, 96)
    waste_volume_kg = np.random.uniform(10, 1000)

    waste_factor = {
        "fruit_waste": 1.15,
        "vegetable_waste": 0.95,
        "brewery_waste": 1.25,
        "dairy_waste": 1.10,
        "mixed_agri_waste": 1.00,
    }[waste_type]

    ph_score = max(0, 1 - abs(ph - 6.2) / 3)
    temp_score = max(0, 1 - abs(temperature - 32) / 15)
    moisture_score = max(0, 1 - abs(moisture - 70) / 40)
    time_score = min(fermentation_time / 72, 1.2)

    protein_yield = (
        8
        + sugar_content * 0.55
        + nitrogen_content * 4.5
        + ph_score * 10
        + temp_score * 8
        + moisture_score * 5
        + time_score * 7
    ) * waste_factor

    protein_yield += np.random.normal(0, 3)

    protein_yield = max(5, min(protein_yield, 85))

    data.append(
        {
            "waste_type": waste_type,
            "sugar_content": round(sugar_content, 2),
            "nitrogen_content": round(nitrogen_content, 2),
            "moisture": round(moisture, 2),
            "ph": round(ph, 2),
            "temperature": round(temperature, 2),
            "fermentation_time": round(fermentation_time, 2),
            "waste_volume_kg": round(waste_volume_kg, 2),
            "location": location,
            "protein_yield": round(protein_yield, 2),
        }
    )

df = pd.DataFrame(data)

output_path = Path("ml/sample_protein_data.csv")
df.to_csv(output_path, index=False)

print(f"Saved synthetic dataset to {output_path}")
print(df.head())
