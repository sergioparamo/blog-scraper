import concurrent.futures
import requests
from bs4 import BeautifulSoup
import os
import json
import time
from weasyprint import HTML
import dateparser

# Configuration
DEFAULT_JSON_FILE = "blog_data.json"

def generate_pdf_with_weasyprint(content, year, file_name=None):
    print(f"Generating PDF for {year}...")
    """Generate a PDF from blog content for a specific year."""
    if not file_name:
        file_name = f"Blog_{year}.pdf"

    html_content = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; margin: 2cm; }
            h1 { font-size: 24px; color: #333; }
            h2 { font-size: 20px; color: #555; }
            p { font-size: 14px; color: #333; margin: 0.5em 0; }
            img { max-width: 100%; margin: 1em 0; display: block; }
        </style>
    </head>
    <body>
    """
    
    html_content += f"<h1>Blog Posts from {year}</h1>"

    for month_data in content['months']:
        month = month_data['month']
        # do not write it if there is no content
        if not month_data['posts']:
            continue
        html_content += f"<h2>{month}</h2>"

        for post in month_data['posts']:
            html_content += f"<h3>{post['date']} - {post['title']}</h3>"
            for item in post['content']:
                html_content += f"<p>{item}</p>"

    html_content += "</body></html>"
    
    print('html_content', html_content)
    final_soup = BeautifulSoup(html_content, "html.parser")
    HTML(string=str(final_soup)).write_pdf(file_name)

def format_date(date_str):
    """
    Format a human-readable date string into dd/mm/YYYY format.

    Args:
        date_str (str): The human-readable date string.
                        Examples: "3 de enero de 2004", "1st of January of 2005", "15 août 2021"

    Returns:
        str: The formatted date string in dd/mm/YYYY format or 'Invalid date' if parsing fails.
    """
    try:
        # Use dateparser to parse the date string
        parsed_date = dateparser.parse(date_str)

        if not parsed_date:
            return "Invalid date"

        # Format the parsed date into dd/mm/YYYY
        return parsed_date.strftime("%d/%m/%Y")
    except Exception as e:
        print(f"Error parsing date '{date_str}': {e}")
        return "Invalid date"
    
def extract_post_data(post_url):
    """Extract the content of a blog post."""
    try:
        response = requests.get(post_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the date
        date_element = soup.find('time')
        date = date_element.text.strip() if date_element else 'No date'
        
        print(date)

        # Extract the title
        title_element = soup.find('h1', class_='entry-title')
        
        if not title_element:
            print(f"Missing title for {post_url}")
            return None
        title = title_element.text.strip()
        print(title_element)

        # Extract the content
        article_element = soup.find('article')
        if not article_element:
            print(f"Missing article element for {post_url}")
            return None

        content_div = article_element.find('div', class_='entry-content')
        if not content_div:
            print(f"Missing entry-content for {post_url}")
            return None

        # Collect paragraphs and images
        content_elements = content_div.find_all(["p", "img"])
        content = [str(element) for element in content_elements]

        return {
            "date": format_date(date),
            "title": title,
            "content": content,
            "url": post_url
        }
    except Exception as e:
        print(f"Error extracting post data from {post_url}: {e}")
        return None

def find_last_page_from_nav(base_url):
    """Extract the last page from the navigation element."""
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Locate the navigation element
        nav = soup.find('nav', class_='navigation pagination')
        if not nav:
            print("No navigation element found, falling back to iteration.")
            return None
        
        # Find dots and page numbers
        dots = nav.find('span', class_='page-numbers dots')
        if dots:
            # Get the last `a` after the dots span
            last_page_link = dots.find_next('a', class_='page-numbers')
            if last_page_link:
                last_page_url = last_page_link['href']
                # Extract the last page number from the URL
                last_page = int(last_page_url.split('/page/')[-1].strip('/'))
                return last_page
        
        # If no dots span, find the last `a` with page-numbers class
        last_page_link = nav.find_all('a', class_='page-numbers')[-1]
        last_page_url = last_page_link['href']
        last_page = int(last_page_url.split('/page/')[-1].strip('/'))
        return last_page

    except Exception as e:
        print(f"Error extracting last page from navigation: {e}")
        return None

def find_last_page(base_url):
    """Fallback: Determine the last page by iterating."""
    print("Using fallback method to find last page.")
    current_page = 1

    while True:
        page_url = f"{base_url}/page/{current_page}/"
        response = requests.get(page_url)

        if response.status_code != 200:
            break  # Stop when no next page exists (404 or similar)

        current_page += 1

    return current_page - 1  # The last valid page number

def find_last_page_dynamic(base_url):
    """Determine the last page dynamically using navigation or fallback."""
    last_page = find_last_page_from_nav(base_url)
    if last_page:
        print(f"Last page found from navigation: {last_page}")
        return last_page
    else:
        return find_last_page(base_url)

def crawl_blog_month(blog_url, year, month):
    """Crawl a specific month and handle pagination."""
    base_url = f"{blog_url}/{year}/{str(month).zfill(2)}"
    last_page = find_last_page_dynamic(base_url)
    month_data = {"month": month, "posts": []}

    # Start from the last page and work backward
    for page in range(last_page, 0, -1):
        page_url = f"{base_url}/page/{page}/"
        print(f"Processing {page_url}...")
        response = requests.get(page_url)

        if response.status_code != 200:
            print(f"Failed to access {page_url}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        posts = soup.find_all('h2', class_='entry-title')

        for post in reversed(posts):  # Reverse to start from the last element
            post_url = post.find('a')['href']
            print(f"Found post: {post_url}")
            post_data = extract_post_data(post_url)
            if post_data:
                month_data['posts'].append(post_data)

    return month_data

def crawl_blog(blog_url, years, json_file=DEFAULT_JSON_FILE):
    """Crawl a blog for posts in specified years."""
    all_content = []

    if os.path.exists(json_file):
        with open(json_file, "r", encoding="utf-8") as file:
            all_content = json.load(file)
    else:
        for year in years:
            year_data = {"year": year, "months": []}

            for month in range(1, 12):
                print(f"Crawling {blog_url} for {year}/{month:02}...")
                month_data = crawl_blog_month(blog_url, year, month)
                year_data["months"].append(month_data)
                time.sleep(1)  # Pause to avoid overloading the server

            all_content.append(year_data)

        with open(json_file, "w", encoding="utf-8") as file:
            json.dump(all_content, file, ensure_ascii=False, indent=4)

    return all_content

def generate_pdfs_in_parallel(content):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        
        # Enviar la tarea para cada año.
        for year_data in content:
            print(year_data['year'])
            year = year_data['year']
            futures.append(executor.submit(generate_pdf_with_weasyprint, year_data, year))
        
        # Esperar que todos los hilos terminen.
        for future in futures:
            future.result()

if __name__ == "__main__":
    # Ask for input
    BLOG_URL = input("Enter the blog URL: ")
    YEARS = [int(year) for year in input("Enter years range (comma-separated): ").split(",")]

    # Crawl the blog and generate PDFs
    blog_content = crawl_blog(BLOG_URL, YEARS)
    generate_pdfs_in_parallel(blog_content)
    print("PDF generation complete!")