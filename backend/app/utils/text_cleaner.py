def extract_ingredients_from_predictions(predictions):
    detected = []

    for p in predictions:
        label = p.class_name.lower()
        detected.append(label)

    # remove duplicates
    return list(set(detected))
