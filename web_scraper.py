""" --Simple Web Scraper--
returns URLS, Emails and phone numbers
found on a given website."""

__author__ = '''Jordan Kubista, with help from stackoverflow
                in setting up pattern and multiline regex,
                provided links for regex were also used'''

import sys
import argparse
import re
import requests
import subprocess


def get_html(site):
    """Send request to get the website and creates a html
        file for the following functions to read"""
# ----WEBSITE REQUEST----
    get_website = requests.get(site)

    request_response = get_website.status_code

    if request_response != 200:
        print('----Jordan\'s Web Scraper----')
        print(f'Error: {request_response} \nCannot reach this site')
        sys.exit(1)
    else:
        with open('site_text.html', 'w') as site_text:
            site_text.write(get_website.text)


def scrape_for_url(site):
    """Takes site html page and searches for URLs"""
# ----opens html file to search for URLs----
    with open('site_text.html', 'r') as site_file:
        get_website = site_file.read()
# ---URL SEARCH----
    url_pattern = r'''(https?:\/\/[-a-zA-Z0-9@:%._\+~#=]
        {1,2048}\.[a-zA-Z0-9()]{1,6}\b)([-a-zA-Z0-9()@:
        %_\+.~#?&\/\/=,;]*)'''
    url_regex = re.compile(url_pattern, re.VERBOSE)

    url_search = re.findall(url_regex, get_website)

    print('----Jordan\'s Web Scraper----')
    print(f'RESULTS FOR: {site}')
    print('----URL----')
    print(f'Found {len(url_search)}')
    counter = 1
    for link in url_search:
        jlink = ''.join(link)
        print(f'{counter}) {jlink}')
        counter += 1


def scrape_for_email(site):
    """Takes site html page and searches for Emails"""
# ----opens html file to search for emails----
    with open('site_text.html', 'r') as site_file:
        get_website = site_file.read()

# ----EMAIL SEARCH----
    email_pattern = r'''(?:[a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.
        [a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f
        \x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@
        (?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])
        ?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4]
        [0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f
        \x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''
    email_regex = re.compile(email_pattern, re.VERBOSE)

    email_search = re.findall(email_regex, get_website)

    counter2 = 1
    if len(email_search) > 0:
        print('----EMAIL----')
        print(f'Found {len(email_search)}')
        for email in email_search:
            jemail = ''.join(email)
            print(f'{counter2}) {jemail}')
            counter2 += 1
    else:
        print('[----No Emails were found!----]')


def scrape_for_phone(site):
    """Takes site html page and searches for Phone Numbers"""
# ----opens html file to search for Phone Numbers----
    with open('site_text.html', 'r') as site_file:
        get_website = site_file.read()

# ----PHONE SEARCH----
    phone_pattern = r'''>(1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})
        (\se?x?t?(\d*))?)<'''
    phone_regex = re.compile(phone_pattern, re.VERBOSE)

    phone_search = re.findall(phone_regex, get_website)
    counter3 = 1
    if len(phone_search) > 0:
        print('----PHONE NUMBER----')
        print(f'Found {len(phone_search)}')
        for phone in phone_search:
            print(f'{counter3}) {phone[0]}')
            counter3 += 1
    else:
        print('[----No phone numbers were found!----]')


def create_parser():
    "Returns an instance of argparse.ArgumentParser"
    parser = argparse.ArgumentParser(description='''Requires a website URL to search
                                     the site for URLs, Emails and Phone
                                     Numbers.''')
    parser.add_argument('-u', '--url', help='Use to just recieve URLs.',
                        action='store_true')
    parser.add_argument('-e', '--email', help='Use to just recieve Emails.',
                        action='store_true')
    parser.add_argument('-p', '--phone', help='Use to just recieve Phone\
                        Numbers.', action='store_true')
    parser.add_argument('website', help='Enter a website to search')
    return parser


def main(args):
    "takes command line arguments and runs the web_scraper program"

    parser = create_parser()
    ns = parser.parse_args(args)

    url = ns.url
    email = ns.email
    phone = ns.phone
    website = ns.website

    get_html(website)

    if not ns:
        parser.print_usage()
        print(ns)
        sys.exit(1)

    if not url and not email and not phone:
        scrape_for_url(website)
        scrape_for_email(website)
        scrape_for_phone(website)
    elif url:
        scrape_for_url(website)
    elif email:
        print('----Jordan\'s Web Scraper----')
        print(f'RESULTS FOR: {website}')
        scrape_for_email(website)
    elif phone:
        print('----Jordan\'s Web Scraper----')
        print(f'RESULTS FOR: {website}')
        scrape_for_phone(website)

    subprocess.run('rm -rf site_text.html', shell=True)


if __name__ == "__main__":
    main(sys.argv[1:])
