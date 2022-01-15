'''
Selenium based script to retrieve first 100 reviews from 5 specified
Airbnb hosts.
Reviews are saved in CSV format
'''

import re
import csv
import time
from selenium import webdriver

def airbnb_reviews(websites):
    for website in websites:
        print ('\nRetrieving:', website)
        path = '/Users/sambrown/documents/python/webscraping/chromedriver'
        driver = webdriver.Chrome(path)
        driver.get(website)

        #Extract Airbnb host name and format it for later use
        get_title = driver.title
        host_name = get_title[:re.search("\'s Profile", get_title).start()].replace(" ", "-")

        #Create empty list to populate with reviews
        review_text = []

        #Need to click Show More Reviews several times to load enough reviews
        for _ in range(13):
            more_reviews = driver.find_element_by_class_name('_rto2zje')
            driver.execute_script("arguments[0].click();", more_reviews)
            #Pause to allow page to reload
            time.sleep(2)

        #Find reviews section
        reviews = driver.find_elements_by_xpath("//div[@id='user-profile-review-tabs']/div/div/div/div/div/span")
        for review in reviews:
            #Skip any auto generated reviews
            if str(review.text).startswith("The host canceled this reservation"):
                continue
            #Skip blank reviews
            elif str(review.text) == "":
                continue
            #If we have a suitable review, add it to the list
            review_text.append(review.text)

        #Close Selenium driver
        driver.quit()

        #Remove any read mores that slipped through the net
        review_text = [x for x in review_text if x != "read more"]

        #Save results as CSV
        headings = ['URL', 'Review Text']
        #Generate filename based on host name
        filename = host_name + '-reviews.csv'
        print('Writing data to', filename)
        with open(filename, 'w') as f:
            write = csv.writer(f)
            write.writerow(headings)
            #Just write first 100 reviews if we captured more
            for row in review_text[:100]:
                #According to the specification,
                #each row should contain the URL and the review
                row_inc_url = (website, row)
                write.writerow(row_inc_url)
        print ('Finished', host_name)
    print ('Finished all')

if __name__ == "__main__":
    #List of specified host pages to trawl
    websites = [
    'https://www.airbnb.com.au/users/show/11914644',
    'https://www.airbnb.com.au/users/show/7409213',
    'https://www.airbnb.com.au/users/show/3046924',
    'https://www.airbnb.com.au/users/show/1649158',
    'https://www.airbnb.com.au/users/show/23274365'
    ]
    airbnb_reviews(websites)
