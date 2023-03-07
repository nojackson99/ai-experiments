from pathlib import Path

import scrapy
import pandas as pd

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://quotes.toscrape.com/page/1/',
            #'https://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #* To scape the sites into json with key being text type
        # for quote in response.css('div.quote'):
        #     yield {
        #         'text': quote.css('span.text::text').get(),
        #         'author': quote.css('small.author::text').get(),
        #         'tags': quote.css('div.tags a.tag::text').getall(),
        #     }
        
        #* To scrape the site into raw text including any whitespace and empty lines 
        # Extract all the text from the response
        # text = response.xpath('string()').extract_first()
       
        # with open('quotesRawText.txt', 'w') as file:
        #     file.write(text)

        #* To take lines of text from get_lines() yield function and write to a txt file
        # # Open a file in write mode
        # with open('quotesRawTextNoWhitespace.txt', 'w') as file:
        #     # Iterate over each line of text and write it to the file
        #     for line in get_lines():
        #         file.write(line + '\n')

        #* To scrape the site and text in a csv with each word in a new line
        # # Extract all the text from the response
        # text = response.xpath('string()').extract_first()

        # # Split the text into words after removing any leading or trailing white space
        # words = [word.strip() for word in text.split() if word.strip()]

        # # Create a Pandas data frame with a single column
        # df = pd.DataFrame({'words': words})

        # # Write the data frame to a CSV file
        # df.to_csv('quotes.csv', index=False)
        
        #* To scrape the site and remove all whitespace and empty lines
        def get_lines():
            # Extract all the text from the response
            text = response.xpath('string()').extract_first()

            # Split the text into lines and iterate over each line
            for line in text.splitlines():
                # Strip the line of any leading or trailing white space
                line = line.strip()

                # Skip any empty lines
                if line:
                    yield line

        # writes data passed in to a new csv file
        def write_to_csv(sentences, file_name):
            # Create a Pandas data frame with a single column
            df = pd.DataFrame({'sentences': sentences})

            # Write the data frame to a CSV file
            df.to_csv((file_name + '.csv'), index=False)

        lines_array = []

        for line in get_lines():
            lines_array.append(line)

        write_to_csv(lines_array, 'quotesLines')

        
        
        