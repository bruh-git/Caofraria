with open(encoded_image, "wb") as encoded_image:
        encoded_image.write(image_data)
    return encoded_image