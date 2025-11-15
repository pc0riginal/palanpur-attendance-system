import dropbox
import os
from django.conf import settings

# Dropbox configuration
DROPBOX_ACCESS_TOKEN = "sl.u.AGEk-3K-q84rJOdkh9Npm-MLBgQM3leAquB_2w4l6aVLX6Hi_aAz2tyVhbKEt1EBbuFoUQrt0w1rHI_10CvfhsHYAfzjnBKDFP8Ai3nFlgn8OgxY-HxLG0ulFspF6-t87FuCkv1rB3YSnI3C8xQ1Od4Qf2QmWl_9hgiNWTZsmFq6hs5S5h4BOpQGCNWRT4laJN-0qgpWicRifYnocxYmG7QfRWmphdXSaAlB3GX8VFXVSBtTqkJ-bu6K2gyq2-c83C6TV3Bl0Nz9O8xK6HhUjGh6tjVAQuTppLvHAxIK3ckR9e4Z3CfbRPbREzqIg1KzOH_G9ojL4RamnPCcUrEQ-Kva4Wc5lNYrB3vBJFY7JYuHbyCAdlMmZNIDkRCtgvfdBJpOEUJ0ibWvbrmcildb38hCngKf1agmjfYNcCd4U6lWlLivcV2TuTkGJSDOQgGL_0qraHEuKvpARb2M2W1VoOcL0d0hQ6Gz6Iv5YzIq2zmFmAxv37irrjGWkaeIzA_kiGzAi5ftBhetGy7_Nr0wty273byMIIyYhxbkzrD_KKvAZ2AS9EN0LMWd5yX-5HN-nkYz5rfN_4wdTc274fqdi4fgzURHFBosgOOBgBK2EhlXPeeNYyvhAU0QoMN_s5XT7sj7cbD79nvO4ApdbH0nFmZM08LIqrZKspvFgNKO_KgFhXAEtMW5gjAHHWu5I2kF_u55szfHZZRVJ3pti2FLEEMKipzEypvPyW4gFyxrmW4bgqEgHhLozpUBAK9qmYMNBz6VsVVTEcWBOGeoe0GydEiHoJAawTQIFZnqXZwJRST-kf1JTXbqJwLdKd9XbZr7SDu3U86zXJeVYppKDgEhot7a-T0a-NpK6w4reWqhuJWyJ4NqUOMaB16YF3zocgjBOutGz9c0cATzGOm-uqycBhdvglA3SWlUOYixojOw1EHkrT9zSG7uR1rJuzocxuRj0OTl4DOJaGEcLT-rVdV9R56pqI_5wsYILYzVlz59qXLL3lM1Z5lxAfGS6l3Pr0CLCYp6G7gg7mUJ6l85eqRBhcfXcBNroRLaZv1OeVJcXn2Wa8kmrPdzZ9dkkXEolUO_ursKHqXjhJ1wk8xnGrjZFNtTZ4LSHpjdYJ-M6K9vqooXF1TnF1K_YQkj-eYvXK3e8CstHo-MNGa6G1-JmEaRVjiFQvmV2mwJOLhdoE1tAS-DJSBkrBJJnJ3bWKOReTMVikdf16jp0SbHfL0csclS_GwyEA4UyYrEtIt6FychNVOYAbuDkQftTkrjY29UCuz_xBqCsAVHNKDh9arMk3zrX3Zjc1sAfldBXBJVZEN1tND3us8MNstbFYICe67YfN0XRr1me2S-hBBXZftS3CWwLNtKcx0ba6mzlt-kL-g5w8cXxJRBiYuhg3ml7ncJJKQ3ahCaJ4xqqqZEihapavNxzehCwhg3qpoI3pcyY1cOBDgUKWWolsCzkO0MHQNquHGmSh0o7yNm5RY8Pq6huL-BIgxa"
def get_direct_dropbox_link(shared_url):
    """Convert Dropbox shared link to direct link."""
    if "dropbox.com" in shared_url:
        shared_url = shared_url.replace("?dl=0", "?raw=1")
        shared_url = shared_url.replace("?dl=1", "?raw=1")
        shared_url = shared_url.replace("www.dropbox.com", "dl.dropboxusercontent.com")
    return shared_url

def upload_devotee_photo(photo_file, devotee_data):
    """Upload devotee photo to Dropbox and return direct URL."""
    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
        
        # Create filename from devotee data: first_last_number
        name_parts = devotee_data['name'].strip().split()
        first_name = name_parts[0].lower() if name_parts else 'unknown'
        last_name = name_parts[-1].lower() if len(name_parts) > 1 else ''
        contact_number = devotee_data.get('contact_number', '0000000000')
        
        file_extension = os.path.splitext(photo_file.name)[1] or '.jpg'
        filename = f"{first_name}_{last_name}_{contact_number}{file_extension}" if last_name else f"{first_name}_{contact_number}{file_extension}"
        dropbox_path = f"/devotee_photos/{filename}"
        
        # print(f"Uploading photo as: {filename}")
        
        # Reset file pointer to beginning
        photo_file.seek(0)
        file_content = photo_file.read()
        
        # Upload file
        upload_result = dbx.files_upload(file_content, dropbox_path, mode=dropbox.files.WriteMode.overwrite)
        # print(f"Upload successful: {upload_result.name}")
        
        # Create shared link
        try:
            link = dbx.sharing_create_shared_link_with_settings(dropbox_path)
        except dropbox.exceptions.ApiError:
            # Link already exists
            links = dbx.sharing_list_shared_links(path=dropbox_path).links
            link = links[0] if links else None
        
        if link:
            direct_url = get_direct_dropbox_link(link.url)
            # print(f"Direct URL: {direct_url}")
            return direct_url
        
        return None
        
    except Exception as e:
        print(f"Dropbox upload error: {e}")
        return None