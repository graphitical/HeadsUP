import urllib.parse
import requests
import os, argparse
import csv
import time
import random

BASE_URL = "https://dl.acm.org/exportformats_search.cfm?"
ACMDL_RESULTS_DIR = "ACMDL_Results"


def download_csv(field, keyword, venue, year, force_rerun_query=False):
    save_dir = os.path.join(ACMDL_RESULTS_DIR, keyword, venue)
    tmp_results_filename = os.path.join(save_dir, get_filename(field, keyword, venue, year, True))

    # Check to see if we've run this query before and saved the results
    if os.path.exists(tmp_results_filename) is True and force_rerun_query is False:
        error_str = "Query results already exist for query (stored in '{}' but force_rerun_query=False. " \
                    "To rerun a query, set force_rerun_query=True. Warning: this will overwrite the query " \
                    "results".format(tmp_results_filename)

        print(error_str)
        return {
            'success': False,
            'error': error_str,
            'ran_query': False,
            'save_filename_with_dir': tmp_results_filename
        }

    print("Downloading CSV for field= {} keyword={} venue={} year={}".format(field, keyword, venue, year))

    # Example CSV export urls
    # https://dl.acm.org/exportformats_search.cfm?query=disability&filtered=series%2EseriesAbbr%3DASSETS&expformat=csv
    # with year
    # https://dl.acm.org/exportformats_search.cfm?query=%28disability%29&filtered=series%2EseriesAbbr%3DASSETS&dte=2014&bfr=2014&expformat=csv
    
    # add fields to query
    query_url = ''
    if(field == 'title'):
        query_url = 'query=acmdlTitle' 
    elif(field == 'abstract'):
        query_url = 'query=recordAbstract'
    elif(field == 'author'):
        query_url = 'query=persons%2Eauthors%2EpersonName'
    elif(field == 'affiliation'):
        query_url = 'query=persons%2Eauthors%2Eaffiliation'
    elif(field == 'full-text'):
        query_url = 'query=content%2Eftsec'
    elif(field == 'funding-agency'):
        query_url = 'query=fundingAgencies%2EfundingAgencyNames'
    elif(field == 'author-keywords'):
        query_url = 'query=keywords%2Eauthor%2Ekeyword'
    
    # add keyword
    query_url = query_url + '%3A%28%252B' + "\"" + keyword + "\""

    # add venue (journals (TOCHI, TACCESS) are parsed differently than conferences)
    if(venue == 'TACCESS'):
        query_url = query_url + '&' + 'filtered=acmPubGroups%2EacmPubGroup%3DJournal%7EacmdlPublicationTitle%2Eraw%3D' + 'ACM%20Transactions%20on%20Accessible%20Computing%20%28TACCESS%29'
    elif(venue == 'TOCHI'):
        query_url = query_url + '&' + 'filtered=acmPubGroups%2EacmPubGroup%3DJournal%7EacmdlPublicationTitle%2Eraw%3D' + 'ACM%20Transactions%20on%20Computer%2DHuman%20Interaction%20%28TOCHI%29'
    else:
        query_url = query_url + '&' + 'filtered=series%2EseriesAbbr%3D' + venue
   
    # add year
    query_url = query_url + '&' + 'dte=' + str(year) + '&bfr=' + str(year)
    
    # export as csv
    query_url = query_url + '&expformat=csv'
    print("Raw query_url=" + query_url)
    
    # Strangely, ACM does not appear to fully escape/encode their urls, so this won't work
    encoded_query_url = urllib.parse.quote(query_url)
    print("Encoded query_url=" + encoded_query_url)
    encoded_query_url = BASE_URL + encoded_query_url

    print("Full encoded url: " + encoded_query_url)

    custom_encoded_query_url = BASE_URL + query_url
    print("Custom encoded url: " + custom_encoded_query_url)

    # looks like requests has ability to pass params
    # https://2.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    http_headers = {'User-Agent': user_agent}
    r = requests.get(custom_encoded_query_url, headers=http_headers)

    success = True
    if r.status_code == 403 or \
            r.url == 'https://dl.acm.org/errorpgs/403.html' or \
            "<title>403 - Forbidden Access to The Digital Library</title>" in r.text:
        print("Uh oh, received 403 Access Forbidden Error")
        success = False

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    save_filename_with_dir = os.path.join(save_dir, get_filename(field, keyword, venue, year, success))

    error_str = ""
    if success is False:
        with open(save_filename_with_dir, 'wb') as f:
            f.write(r.content)
            error_str = "403 forbidden result saved to '{}'".format(save_filename_with_dir)
            print(error_str)
    elif os.path.exists(save_filename_with_dir) is False or \
            (os.path.exists(save_filename_with_dir) is True and force_rerun_query is True):
        with open(save_filename_with_dir, 'wb') as f:
            f.write(r.content)
            print("field={} keyword={} venue={} year={} saved to '{}'".format(field, keyword, venue, year, save_filename_with_dir))

    return {
        'success': success,
        'ran_query': True,
        'error': error_str,
        'save_filename_with_dir': save_filename_with_dir
    }


def get_filename(field, keyword, venue, year, success):
    filename = str(year) + '_' + venue + '_' + 'field=' + field + '_' + 'keyword=' + keyword
    if success:
        return filename + ".csv"
    else:
        return filename + ".html"


def parse_filename(filename):
    # Example filename: year_pubvenue_keywords.csv
    # 2009_ASSETS_keyword='assistive technology'.csv
    filename_no_ext = os.path.splitext(filename)[0]
    filename_parts = filename_no_ext.split("_")
    year = int(filename_parts[0])
    pub_venue = filename_parts[1]
    field = filename_parts[2].split('=')[1]
    keyword = filename_parts[3].split('=')[1]

    return {
        "year": year,
        "pub_venue": pub_venue,
        "field": field,
        "keyword": keyword
    }


def main(args):
    # Field 'title' Keyword 'disability', year='2015', venue='ASSETS'
    # https://dl.acm.org/exportformats_search.cfm?query=acmdlTitle%3A%28%252Bdisability%29&filtered=series%2EseriesAbbr%3DASSETS&dte=2015&bfr=2015&expformat=csv
    # Lots of escape characters, see: https://www.w3schools.com/tags/ref_urlencode.asp
    # %28 = (
    # %29 = )
    # %2E = .
    # %3D = =
    # You can use a tool like the following to decode these url strings: https://meyerweb.com/eric/tools/dencoder/
    # 
    # Keyword: 'disability' venue='ASSETS'. 
    # https://dl.acm.org/exportformats_search.cfm?query=disability&filtered=series%2EseriesAbbr%3DASSETS&within=owners%2Eowner%3DHOSTED&dte=&bfr=&srt=%5Fscore&expformat=csv
    # Which can be simplified to the following. Strangely, notice how they don't fully escape/encode their urls
    # https://dl.acm.org/exportformats_search.cfm?query=disability&filtered=series%2EseriesAbbr%3DASSETS&expformat=csv
    # This is the url fully encoded (but this won't work)
    # https://dl.acm.org/exportformats_search.cfm?query%3Ddisability%26filtered%3Dseries.seriesAbbr%3DASSETS%26expformat%3Dcsv

    parser = argparse.ArgumentParser(description="Downloads CSV Exports from the ACM DL")

    # add expected arguments
    parser.add_argument('--keywords', dest='keywords', required=True, default='disability',
                        help='A single keyword or a comma separated list of keywords.')
    parser.add_argument('--fields', dest='fields', required=True, default='full-text',
                        help='A single field or a comma separated list of fields to query. Can be title, abstract, author, affiliation, full-text, funding-agency, author-keywords. Defaults to full-text.')                  
    parser.add_argument('--venues', dest='venues', required=True, default='ASSETS',
                        help='A single venue or a comma separated list of venues. For example, ASSETS, TACCESS, CHI, TOCHI, UbiComp, and/or CSCW')
    parser.add_argument('--start', dest='start_year', required=False, default=1999, type=int,
                        help='The first year to download (inclusive). Defaults to 1999')
    parser.add_argument('--end', dest='end_year', required=False, default=2019, type=int,
                        help='The last year to download (inclusive). Defaults to 2019')

    # parse args
    args = parser.parse_args()
    print("**Running queries for:**")
    print("\tvenues={}".format(args.venues))
    print("\tfields={}".format(args.fields))
    print("\tkeywords={}".format(args.keywords))
    print("\tstart_year={} end_year={} (inclusive)".format(args.start_year, args.end_year))

    csv_reader_venues = csv.reader([args.venues])
    results_tracker = {'total_queries_cnt': 0,
                       'ran_query_cnt': 0,
                       'successful_download_cnt': 0,
                       'failed_download_cnt': 0
                       }

    for venues in csv_reader_venues:
        for venue in venues:
            venue = venue.strip()
            csv_reader_fields = csv.reader([args.fields])
            for fields in csv_reader_fields: 
                for field in fields:
                    field = field.strip()
                    csv_reader_keywords = csv.reader([args.keywords])
                    for keywords in csv_reader_keywords:
                        for keyword in keywords:
                            keyword = keyword.strip()
                            for year in range(args.start_year, args.end_year + 1):
                                ret_values = download_csv(field, keyword, venue, year)
                                results_tracker['total_queries_cnt'] += 1

                                if ret_values['success']:
                                    results_tracker['successful_download_cnt'] += 1
                                else:
                                    results_tracker['failed_download_cnt'] += 1

                                if ret_values['ran_query'] == True:
                                    # We don't want to bombard the server, so we will sleep a random amount
                                    # I've been experimenting with these values and have been getting blocked
                                    # with low vals (so I keep increasing them. YMMV).
                                    min_sleep_secs = 120
                                    max_sleep_additional_secs = 190
                                    sleep_time_in_secs = min_sleep_secs + random.random() * max_sleep_additional_secs
                                    print("Sleeping for {} secs".format(sleep_time_in_secs))
                                    time.sleep(sleep_time_in_secs)
                                    results_tracker['ran_query_cnt'] += 1

    print("**Finished!**")
    print('\tTotal possible queries: {}'.format(results_tracker['total_queries_cnt']))
    print('\tActually ran {} queries'.format(results_tracker['ran_query_cnt']))
    print('\tSuccessfully downloaded: {} query results'.format(results_tracker['successful_download_cnt']))

    # TODO: differentiate between failed 403 and failed because we already have data
    # print('\tFailed to download: {} query results'.format(results_tracker['failed_download_cnt']))

# call main
if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
