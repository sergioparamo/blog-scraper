# Blog Scraper and PDF Generator script

## Overview

This Python script allows you to scrape blog posts from a specified blog URL for specific years and generate PDFs compiling the posts for each year. It utilizes `BeautifulSoup` for web scraping and `WeasyPrint` for generating high-quality PDFs.

---

## Features

- **Dynamic Blog Crawling**: Crawl any blog by providing its base URL and the years to scrape.
- **Content Parsing**: Extracts post titles, dates, and content (including images).
- **PDF Generation**: Creates beautifully formatted PDFs for each year's posts.
- **Content Archival**: Saves scraped data in a JSON file for reuse.
- **Parallel Processing**: Utilizes multithreading to speed up PDF generation.

---

## Requirements

### Python Version

The script is tested in Python 3.12

### Python Dependencies

I recommend using a virtual environment to manage your dependencies.

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required packages using the command below:

```bash
pip install requests beautifulsoup4 weasyprint dateparser pydyf
```

or you can just install the dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Additional Requirements

- An internet connection for accessing blog pages.
- Ensure the `weasyprint` package is installed and configured correctly. You may need additional libraries like `cairo` for rendering PDFs.

---

## Blog format

### URL Format sample:

The blog posts follow a consistent URL format across all years. Each URL is structured hierarchically to organize posts by year, month, pagination (if applicable), and individual post titles. Here's the breakdown:

- **Base URL**: The base URL of the blog, e.g., `https://www.test.com/`.
- **Year**: The year of the blog post, e.g., `2024`.
- **Month**: The month of the blog post, e.g., `12`.
- **Pagination**: Optional pagination for multiple posts in a single month, e.g., `page/2/`.
- **Title**: The title of the blog post, e.g., `post-title`.

For example, the URL for a blog post on March 20, 2003, is `https://www.test.com/2024/12/post-title`.

Or in the case of pagination, `https://www.test.com/2024/12/page/2/post-title`.

### HTML Format sample:

The format of the blog posts is expected to be the same. The script will scrape the blog page for each year and month and extract the necessary information for each post (title, date, and content).

```html
<article class="post">
  <header class="entry-header">
    <h1 class="entry-title">Blog Post Title</h1>
    <div class="entry-meta">
      <span class="screen-reader-text">Posted on</span>
      <a href="https://www.test.com/2003/03/post-title" rel="bookmark"
        ><time
          class="entry-date published updated"
          datetime="2003-03-20T12:44:12+09:00"
          >March 20, 2003</time
        ></a
      >
    </div>
  </header>
  <div class="entry-content">
    <p>This is the content of the blog post...</p>
  </div>
</article>
```

Format breakdown:

- `<article class="post">`: The main container for the blog post.
- `<header class="entry-header">`: The header section containing the post title and date.
- `<div class="entry-content">`: The content of the blog post.

---

## How to Use

1. **Clone the Repository**

   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. **Run the Script**
   Execute the script and provide the blog URL and years when prompted:

   ```bash
   python blog_scraper.py
   ```

   Example Inputs:

   - **Blog URL**: `https://www.test.com`
   - **Years range (Optional)**: `2009, 2010`

3. **Generated Output**
   - PDFs for each year will be created in the current directory.
   - Scraped data will be saved in a JSON file (`blog_data.json`), allowing you to reuse it without scraping again.

---

## Example Output

For the blog URL `https://www.test.com` and years `2009, 2011`:

- PDFs: `Blog_2009.pdf`, `Blog_2011.pdf`
- JSON: `blog_data.json` (contains structured data of all scraped posts)

---

## File Structure

```
.
├── blog_scraper.py    # Main script
├── blog_data.json     # (Generated) Scraped content as JSON
```

---

## Configuration

### Default JSON File

You can change the default JSON filename by modifying the `DEFAULT_JSON_FILE` variable in the script.

---

## Troubleshooting

- **Missing Content in PDFs**:
  - Ensure the blog's structure matches the selectors used in the script (e.g., `h1.entry-title`, `div.entry-content`).
  - Update the script if the blog's HTML structure changes.
- **WeasyPrint Issues**:

  - Verify that `WeasyPrint` is correctly installed with all dependencies (`pip install weasyprint`).
  - On Linux, ensure `libcairo2` and `pango` are installed.

- **Connection Errors**:
  - Ensure the provided blog URL is correct and accessible.
  - Avoid excessive crawling to prevent being blocked by the server.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for web scraping.
- [WeasyPrint](https://weasyprint.org/) for generating PDFs.
- [dateparser](https://dateparser.readthedocs.io/en/latest/) for parsing dates.
- [pydyf](https://github.com/CourtBouillon/pydyf) for creating PDFs with custom styles.

---

## Collaboration

Feel free to contribute to this project. You can fork the repository, make changes, and submit pull requests.

## Contact

If you have any questions or feedback, please reach out to the project maintainer:

- **GitHub**: [sergioparamo](https://github.com/sergioparamo)
- **Email**: sergio.paramo1997@gmail.com
