from pathlib import Path

# Function to delete a list of images
def delete_images(image_list):
    for image_name in image_list:
        image_path = Path(image_name)
        if image_path.exists():
            image_path.unlink()
            #print(f"{image_name} has been deleted.")
        else:
            print(f"{image_name} does not exist.")
