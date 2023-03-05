import argparse
import csv
import urllib.request
import re
import io
import datetime

def main(url):
    """
    Takes a URL and passes it to other function calls.
    Prompts the user to press any key to exit the program.
    """
    data = download_data(url)
    image_hits, image_percent = count_image_hits(data)
    print(f'There were a total of {image_hits} hits for images today.')
    print(f'Image requests account for {image_percent:.2f}% of all requests.')
    popular_browser, browser_hits = get_popular_browser(data)
    print(f"The most popular browser today was {popular_browser} with {browser_hits} hits.")
    hourly_hits = count_hourly_hits(data)
    print_hourly_hits(hourly_hits)
    input("Press <Enter> to exit")

def download_data(url):
    """
    Takes a URL as input.
    Downloads the web log file and processes the data.
    Returns the processed data as a list of lists.
    """
    with urllib.request.urlopen(url) as response:
        response = response.read().decode('utf-8')
    data = csv.reader(io.StringIO(response))
    return list(data)

def count_image_hits(data):
    """
    Accepts data as input.
    Uses regular expression pattern matching to count total image hits by file extension.
    Returns the number of image hits and their percentage of total hits as a tuple.
    """
    pattern = r'\.(jpg|gif|png)$'
    total_hits = 0
    image_hits = 0
    for row in data:
        try:
            if re.search(pattern, row[0]):
                image_hits += 1
            total_hits += 1
        except IndexError:
            pass
    image_percent = (image_hits / total_hits) * 100
    return image_hits, image_percent

def get_popular_browser(data):
    """
    Accepts data as input.
    Uses regular expression pattern matching to search the file for browser type.
    Returns the most popular browser by usage for the day and its hits as a tuple.
    """
    firefox_hits = 0
    chrome_hits = 0
    ie_hits = 0
    safari_hits = 0
    for row in data:
        try:
            user_agent = row[2]
            if re.search('Firefox', user_agent):
                firefox_hits += 1
            elif re.search('Chrome', user_agent):
                chrome_hits += 1
            elif re.search('MSIE|Trident', user_agent):
                ie_hits += 1
            elif re.search('Safari', user_agent) and not re.search('Chrome', user_agent):
                safari_hits += 1
        except IndexError:
            pass
    hits_by_browser = {
        'Firefox': firefox_hits,
        'Chrome': chrome_hits,
        'Internet Explorer': ie_hits,
        'Safari': safari_hits
    }
    popular_browser = max(hits_by_browser, key=hits_by_browser.get)
    browser_hits = hits_by_browser[popular_browser]
    return popular_browser, browser_hits

def count_hourly_hits(data):
    """
    Accepts data as input.
    Extracts the hour from each row's timestamp and counts the hits per hour.
    Returns a list with the count of hits per hour.
    """
    hourly_hits = [0] * 24
    for row in data:
        try:
            timestamp = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
            hour = timestamp.hour
            hourly_hits[hour] += 1
