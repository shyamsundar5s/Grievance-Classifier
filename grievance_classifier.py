def classify_grievance(text):
    categories = {
        'Infrastructure': ['broken', 'wifi', 'electricity', 'water', 'toilet'],
        'Academic': ['marks', 'exam', 'result', 'assignment'],
        'Administrative': ['id card', 'fee', 'registration', 'admission'],
        'Other': []
    }

    text = text.lower()
    for category, keywords in categories.items():
        if any(keyword in text for keyword in keywords):
            return category
    return 'Other'
