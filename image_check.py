from google.cloud import vision

def detect_object_in_image(image_path, target_object):
    # Initialize the Vision API client
    client = vision.ImageAnnotatorClient()

    # Load the image file
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    # Create an Image object
    image = vision.Image(content=content)

    # Perform label detection on the image
    response = client.label_detection(image=image)
    labels = response.label_annotations

    #for label in labels:
    #    print(label.description.lower())

    # Check if the target object is in the detected labels
    for label in labels:
        if target_object.lower() in label.description.lower():
            #print(f"The image contains a {target_object}.")
            return True

    #print(f"The image does not contain a {target_object}.")
    return False
