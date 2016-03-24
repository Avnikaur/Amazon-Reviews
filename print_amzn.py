# This code flattens Amazon product reviews into csv file
import json
import os
import sys
import pandas
import flatten_json

sys.path.append("etl_lib")
import etl_lib
amazon_reviews ="/Volumes/My Passport/BU - Data warehousing/datasets/AmazonReviews"
top_level_keys =[u'Reviews', u'ProductInfo']
review_keys =[u'Author', u'ReviewID', u'Overall', u'Content', u'Title', u'Date']
product_keys =[u'Price', u'ProductID', u'Features', u'ImgURL', u'Name']

# For each product there are many reviews ie. 1 to many relationship

#Print columns first
category_list=[dir.strip() for dir in os.listdir(amazon_reviews) if dir != '.DS_Store']
log_file = open("print_amzn.log","w")
exception_log = open("print_amzn_except.log","w")

for category in category_list:
 full_dir_path = amazon_reviews + "/" + category
 file_list = [fl for fl in os.listdir(full_dir_path) if fl != '.DS_Store']
 for fl in file_list:
    try:
     
     with open(full_dir_path + "/" + fl) as f:
      data = f.read()
      jsondata = json.loads(data)


      for row in jsondata:
          # Pull the product info first
          #Notice the use of string to deal with None return values in case lookup of column fails
          product_info="@".join([jsondata['ProductInfo'][key] or '' for key in product_keys])
     
          number_reviews = len(jsondata['Reviews'])
          for i in range(number_reviews):
              review = jsondata['Reviews'][i]
              review_info="@".join([review[key] or '' for key in review_keys])
      #use * as record terminator
              sys.stdout.write(category + "@" + product_info + "@" + review_info + "*")
    except:
        exception_log.write(str(sys.exc_info()[0]) + "\n")
        log_file.write(full_dir_path + "/" + fl + "\n")

log_file.close()
exception_log.close()

