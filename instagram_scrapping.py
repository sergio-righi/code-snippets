import instaloader
import time
from instaloader.exceptions import TooManyRequestsException

INPUT_PATH = '\\Users\\sergi\\Documents\\source.txt'
OUTPUT_PATH = '\\Users\\sergi\\Documents\\'

def scrape_instagram_posts(L, username, output_file, max_posts):

    # Load the profile
    profile = instaloader.Profile.from_username(L.context, username)

    # Open the file to store post URLs
    with open(output_file, 'w') as f:
        post_count = 0
        # Loop through each post and print the URL
        for post in profile.get_posts():
            try:
                if post_count >= max_posts:
                    break
                f.write(post.url + '\n')
                post_count += 1
                time.sleep(1)  # Add delay to prevent getting blocked
            except TooManyRequestsException:
                time.sleep(600)  # Wait for 10 minutes before continuing


def paginate_array(data, page_size=10):
    total_items = len(data)
    
    def get_page(page_number):
        start_index = max(total_items - page_number * page_size, 0)
        end_index = total_items - (page_number - 1) * page_size
        return data[start_index:end_index][::-1]
    
    return get_page


def read_input_file():
  try:
    with open(INPUT_PATH, 'r') as file:
      # Read all lines and strip newline characters
      return [line.strip() for line in file.readlines()]
  except FileNotFoundError:
      # print(f"File not found: {INPUT_PATH}")
      return []


if __name__ == "__main__":
  
    # Replace these with your actual Instagram username and password if needed
    login_username = ''  # Optional: Your Instagram username
    login_password = ''  # Optional: Your Instagram password

    # Maximum number of posts to scrape
    max_posts = 18
    
    # Read usernames from the input file
    usernames = read_input_file()

    # Check if the list is populated
    if not usernames:
        print("No usernames found.")        
    else:
        # Create an Instaloader object
        L = instaloader.Instaloader()

        # Login if credentials are provided
        if login_username and login_password:
            L.login(login_username, login_password)
        
            # Create the pagination function
            pagination = paginate_array(usernames)
            
            # Username of the Instagram profile you want to scrape
            for username in pagination(14):
                # Output file to save the post URLs
                output_file = f'{OUTPUT_PATH}{username}.txt'

                try:
                    # Start scraping
                    scrape_instagram_posts(L, username, output_file, max_posts)
                except Exception as e:
                    print(f'{username} {str(e)}')
                
        