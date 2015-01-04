__author__ = 'Mark'
import sys
import os
import log_manager
import file_io

ROOT_DIR = sys.path[0]
DJANGO_APP_NAME = 'home'
DJANGO_APP_DIR = os.path.join(ROOT_DIR, DJANGO_APP_NAME)  # Edit this to the django app folder
DJANGO_VIEWS = os.path.join(DJANGO_APP_DIR, "views.py")  # Path to and including views.py
DJANGO_URLS = os.path.join(DJANGO_APP_DIR, "urls.py")  # Path to and including views.py

log = log_manager.log_manager("logs/process_to_django_log.txt")


def check_view(contents, url_name):
    """
    This function checks to see if the url_name is already in django views.py
    If it is, it will return an untouched version of contents.
    Otherwise it will call append_view() and return an updated version of contents
    :param contents: This is the contents of the views.py file in readlines() format (array)
    :param url_name: This is the url name of the fixed url, no extension
    :return: Current, or appended contents. Returns to process()
    """
    url = "'%s/%s%s'" % (DJANGO_APP_NAME, url_name, SITE_EXT)
    log.log.info('Checking for %s in views...' % url)
    for line in contents:
        if line.find(url) != -1:
            log.log.info('    ...%s found, aborting append.' % url)
            return contents

    log.log.info('    ...%s not found. Appending the view...' % url)
    return append_view(contents, url_name)


def append_view(contents, url_name):
    """
    This function builds a function for the new url in views.py
    :param contents: The contents of views.py in readlines() format (Array)
    :param url_name: This is the url name of the fixed url, no extension
    :return: Returns the appended contents to check_view().
    """
    line = '\n'
    line += "def %s(request):\n" % url_name
    contents.append(line)

    url = "'%s/%s%s'" % (DJANGO_APP_NAME, url_name, SITE_EXT)
    line = "    return render(request, %s)" % url
    contents.append(line)

    log.log.info('    ...done.')
    return contents


def check_urls(contents, url_name):
    """
    This function checks to see if the url_name is already in django urls.py
    If it is, it will return an untouched version of contents.
    Otherwise it will call append_view() and return an updated version of contents
    :param contents: This is the contents of the urls.py file in readlines() format (array)
    :param url_name: This is the url name of the fixed url, no extension
    :return: Current, or appended contents. Returns to process()
    """
    url = '%s%s' % (url_name, SITE_EXT)
    log.log.info('Checking for %s in urls...' % url)
    for line in contents:
        if line.find(url) != -1:
            log.log.info('    ...%s found, aborting append.' % url)
            return contents
    log.log.info('    ...%s not found. Appending the url...' % url)
    return append_urls(contents, url_name)


def append_urls(contents, url_name):
    """
    This function builds a function for the new url in urls.py
    :param contents: The contents of urls.py in readlines() format (Array)
    :param url_name: This is the url name of the fixed url, no extension
    :return: Returns the appended contents to check_url()
    """
    temp = '\n'
    temp += 'urlpatterns.append('
    temp += "url(r'%s%s', views.%s, name='%s'))\n" % (url_name, SITE_EXT, url_name, url_name)
    contents.append(temp)
    log.log.info('    ...done.')
    return contents


def process(url):
    """
    Processes url into both views.py and urls.py
    :param url: A url name to process
    :return: Nothing.
    """
    if url:
        log.log.info("Processing views...")
        contents = file_io.get_contents(DJANGO_VIEWS, lines=True, full_dir=True)
        contents = check_view(contents, url)
        file_io.make_new_file(contents, DJANGO_VIEWS, lines=True)
        log.log.info("    ...done.")

        log.log.info("Processing urls...")
        contents = file_io.get_contents(DJANGO_URLS, lines=True, full_dir=True)
        check_urls(contents, url)
        file_io.make_new_file(contents, DJANGO_URLS, lines=True)
        log.log.info("    ...done.")


def process_py(urls, ext='.htm'):  # Externally called function, only call this function!
    """
    This is the only external function of this file.
    requires a list of urls to process
    :param urls: a list of urls to process
    :param ext: OPTIONAL default argument for site file type, sets global SITE_EXT
    :return: Nothing
    """
    log.log.info("Processing Django Files...")
    global SITE_EXT  # for site extension
    SITE_EXT = ext

    for url in urls:
        process(url)

    log.log.info("    ...done.")

if __name__ == '__main__':
    _urls = [
        'test'
    ]
    get_urls(_urls)
