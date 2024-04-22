import requests

def generate_profile_image(name, size=200):
    # Split the name into first and last names
    names = name.split()
    first_name = names[0]
    last_name = names[-1] if len(names) > 1 else ""

    # Construct the API endpoint URL
    api_url = f"https://avatars.io/api/initials.png?name={first_name}+{last_name}&size={size}&background=random"

    # Send a GET request to the API
    response = requests.get(api_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the image data from the response
        image_bytes = response.content
        return image_bytes
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

name = "Glen James"
profile_image = generate_profile_image(name)

# Save the image to a file
if profile_image:
    with open("profile_image.png", "wb") as f:
        f.write(profile_image)