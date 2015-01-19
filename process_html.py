__author__ = 'mike@afkconcepts.com'
"""
process_html is a django integration script for new html files
"""

import sys
import os
import log_manager
import file_io
import process_py
import logging
import re


def extend_base(contents, template='base.html'):
    """######################################################################################
    # check for {% extends "base.html" %} tag then inserts after doctype                    #
    # ###USAGE: this function can be "independently" called by process or any flow control  #
    #           will apply only to non-template files                                       #
    ######################################################################################"""
    log = logging.getLogger('main')
    EXTENDS_BASE_FRONT = '{% extends'
    EXTENDS_BASE_BACK = ' \"' + template + '\" %}'
    EXTENDS_BASE_INDEX = contents.find(EXTENDS_BASE_FRONT)
    if EXTENDS_BASE_INDEX == -1:
        DOCTYPE_LOC = find_tag(contents, '!DOCTYPE')
        BEFORE_ANY_OTHER_DJANGO_TAGS = contents.find("{%")
        if DOCTYPE_LOC[1] < BEFORE_ANY_OTHER_DJANGO_TAGS or BEFORE_ANY_OTHER_DJANGO_TAGS == -1:
            # we should always get here because doctype should be first line
            new_contents = insert_tag(contents, '\n'+EXTENDS_BASE_FRONT+EXTENDS_BASE_BACK+'\n', DOCTYPE_LOC[1])
        else:
            # just in case doctype is omitted or placed after django tags, extends will still be the first django tag
            new_contents = insert_tag(contents, '\n'+EXTENDS_BASE_FRONT+EXTENDS_BASE_BACK+'\n', BEFORE_ANY_OTHER_DJANGO_TAGS)
        log.info(EXTENDS_BASE_FRONT + EXTENDS_BASE_BACK + " inserted")
        return new_contents
    else:
        log.info("Extends tag found prior to insert. Process aborted.")
        return contents

def load_staticfiles(contents):
    """######################################################################################
    # check for {% load staticfiles %} tag                                                  #
    # then inserts after either {% extends base.html %} (if it exists) or doctype           #
    # ###USAGE: this function will be called by staticfy_resource() to ensure staticfiles   #
    #           is loaded before any linking is attempted                                   #
    ######################################################################################"""
    log = logging.getLogger('main')
    LOAD_SF_TAG = "{% load staticfiles %}"
    LOAD_SF_INDEX = contents.find(LOAD_SF_TAG)
    if LOAD_SF_INDEX != -1:
        log.info("Load staticfiles tag found prior to insert. Process aborted.")
        return contents
    else:
        EXTENDS_BASE_INDEX = contents.find("{% extends")
        if EXTENDS_BASE_INDEX > 0:
            AFTER_EXTENDS = contents.find("%}", EXTENDS_BASE_INDEX)+len("%}")
            new_contents = insert_tag(contents, "\n" + LOAD_SF_TAG + "\n", AFTER_EXTENDS)
            log.info("Load staticfiles tag inserted after {%extends ... %} tag")
        else:
            DOCTYPE_LOC = find_tag(contents, '!DOCTYPE')
            new_contents = insert_tag(contents, "\n" + LOAD_SF_TAG + "\n", DOCTYPE_LOC[1])
            log.info("Load staticfiles tag inserted after DOCTYPE tag")
        return new_contents

def staticfy_resource(contents, tags_affected=['link', 'script', 'img']):
    log = logging.getLogger('main')
    contents = load_staticfiles(contents)

    ATTRIBUTES = ['href=', 'src=']
    STATIC_TAG_FRONT = '\"{% static '
    STATIC_TAG_BACK = ' %}\"'
    for tag in tags_affected:
        index_list = find_all_tags(contents, tag)
        for each_tag in index_list:
            if each_tag[0] == -1:
                break
            else:
                for each_attr in ATTRIBUTES:
                    attr_index = contents.find(each_attr, each_tag[0], each_tag[1])
                    if attr_index != -1:
                        attr_index += len(each_attr)
                        if contents.find('{%', attr_index, each_tag[1]) == -1:
                            contents = insert_tag(contents, STATIC_TAG_FRONT, attr_index)
                            quotes = contents.find("\"", (attr_index+len(STATIC_TAG_FRONT)+1))
                            contents = insert_tag(contents, STATIC_TAG_BACK, quotes+1)
                            log.info("Static reference added to " + each_attr + " within " + tag + " tag.")
    contents = staticfy_preload(contents)
    return contents

def staticfy_preload(contents):
    """######################################################################################
    #  designed to staticfy preloaded resources in format :                                 #
    #  <script ...> $(["file.ext","file2.ext"]).preloadImg(); </script>                     #
    # ###USAGE: this will be called from staticfy_resource() to ensure staticfiles are      #
    #           already in use in given file                                                #
    ######################################################################################"""
    log = logging.getLogger('main')
    STATIC_TAG_FRONT = '\"{% static '
    STATIC_TAG_BACK = ' %}\"'
    FRONT_INDICATOR = '$(['
    BACK_INDICATOR = '])'
    front_index = 0
    back_index = 0
    while front_index != -1:
        front_index = contents.find(FRONT_INDICATOR, back_index)
        if front_index == -1:
            break
        back_index = contents.find(BACK_INDICATOR, front_index)
        file_list = contents[(front_index+len(FRONT_INDICATOR)):back_index]
        thing = file_list.split(',')
        file_list = ""
        for item in thing:
            file_list += STATIC_TAG_FRONT + item + STATIC_TAG_BACK + ","
        file_list = file_list[:-1]
        new_contents = contents[:(front_index+len(FRONT_INDICATOR))] + file_list + contents[back_index:]
        contents = new_contents
        log.info("A script preload list has been STATICFIED!")
    return contents

def url_conf(contents, appname=""):
    """######################################################################################
    # designed to match all hyperlinks to their django url configuration                    #
    # ###USAGE: this function can be "independently" called by process() or any flow control#
    ######################################################################################"""
    log = logging.getLogger('main')
    url_reg_ex = re.compile(r"((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)", re.MULTILINE|re.UNICODE)

    URL_FRONT = '{% url \"'
    URL_BACK = ' %}\"'
    index_list = find_all_tags(contents, 'a')
    for each_tag in index_list:
        if each_tag[0] != -1:
            if contents.find(URL_BACK, each_tag[0], each_tag[1]) == -1:
                attr_index = contents.find('href=', each_tag[0], each_tag[1])
                if attr_index != -1:
                    attr_index += len('href="')
                    print url_reg_ex.findall(contents)
                    if appname == "":
                        contents = insert_tag(contents, URL_FRONT, attr_index)
                    else:
                        contents = insert_tag(contents, (URL_FRONT+appname+":"), attr_index)
                    attr_index += len(URL_FRONT) + 1
                    quotes = contents.find('\"', attr_index)
                    contents = insert_tag(contents, URL_BACK, quotes+1)
                    dot_index = contents.find('.', attr_index, quotes)
                    contents = contents[:dot_index] + contents[quotes:]
                    log.info("Url reference added to href= attribute within <a> tag.")
    return contents

def default_blocks(contents):  # TODO segment into del_tag, mod_tag, insert_tag
    """######################################################################################
    #  designed to insert the default inherited blocks (head_block and body_content)        #
    #  declarations are verbose to avoid naming errors                                      #
    #  could probably generalize to make less redundant, but must remain scalable           #
    # ###USAGE: called during process() when in child page mode                             #
    ######################################################################################"""
    log = logging.getLogger('main')
    HEAD_BLOCK_OPEN = '{% block head_block %}'
    BODY_BLOCK_OPEN = '{% block body_content %}'
    BLOCK_CLOSE = '{% endblock %}'

    HEAD_TAG = '<head'
    HEAD_FRONT = contents.find(HEAD_TAG)
    if HEAD_FRONT > -1:
        HEAD_BACK = contents.find(">", HEAD_FRONT) + 1  # move past > char
        new_contents = contents[:HEAD_FRONT] + HEAD_BLOCK_OPEN + contents[HEAD_BACK:]
        contents = new_contents
        log.info("Head block inserted")

    HEAD_CLOSE_TAG = '</head>'
    HEAD_CLOSE_FRONT = contents.find(HEAD_CLOSE_TAG)
    if HEAD_CLOSE_FRONT > -1:
        HEAD_CLOSE_BACK = HEAD_CLOSE_FRONT + len(HEAD_CLOSE_TAG)
        new_contents = contents[:HEAD_CLOSE_FRONT] + BLOCK_CLOSE + contents[HEAD_CLOSE_BACK:]
        contents = new_contents
        log.info("Head block close inserted")

    BODY_TAG = '<body'
    BODY_FRONT = contents.find(BODY_TAG)
    if BODY_FRONT > -1:
        BODY_BACK = contents.find(">", BODY_FRONT) + 1  # move past > char
        new_contents = contents[:BODY_FRONT] + BODY_BLOCK_OPEN + contents[BODY_BACK:]
        contents = new_contents
        log.info("Body block inserted")

    BODY_CLOSE_TAG = '</body>'
    BODY_CLOSE_FRONT = contents.find(BODY_CLOSE_TAG)
    if BODY_CLOSE_FRONT > -1:
        BODY_CLOSE_BACK = BODY_CLOSE_FRONT + len(BODY_CLOSE_TAG)
        new_contents = contents[:BODY_CLOSE_FRONT] + BLOCK_CLOSE + contents[BODY_CLOSE_BACK:]
        contents = new_contents
        log.info("Body block close inserted")

    return contents

def remove_html_tags(contents):  # TODO will be replaced by del_tag
    """######################################################################################
    # this function simply seeks and eliminates html tags from inheriting pages             #
    # ###USAGE: this function is called in process() when in child page mode                #
    ######################################################################################"""
    log = logging.getLogger('main')
    HTML_TAG = '<html'
    END_OF_HTML_TAG = '>'
    HTML_CLOSE_TAG = '</html>'
    tag_index = contents.find(HTML_TAG)
    end_index = contents.find(END_OF_HTML_TAG, tag_index) + 1  # move past >
    if tag_index > -1:
        new_contents = contents[:tag_index] + contents[end_index:]
        contents = new_contents
        log.info(HTML_TAG + END_OF_HTML_TAG + " removed")
    tag_index = contents.find(HTML_CLOSE_TAG)
    if tag_index > -1:
        new_contents = contents[:tag_index]
        contents = new_contents
        log.info(HTML_CLOSE_TAG + " removed")
    return contents

def remove_relative_path(contents):
    """######################################################################################
    # this function simply seeks and eliminates relative path indicators ( ../ )            #
    # ###USAGE: this function is called in process() for child or template mode             #
    ######################################################################################"""
    log = logging.getLogger('main')
    REL_PATH = '../'
    rel_path_loc = 0
    while rel_path_loc != -1:
        rel_path_loc = contents.find(REL_PATH, rel_path_loc)
        if rel_path_loc != -1:
            rel_path_end = rel_path_loc + len(REL_PATH)
            new_contents = contents[:rel_path_loc] + contents[rel_path_end:]
            contents = new_contents
    return contents

def find_tag(content, tag, start_index=0):
    index = content.find('<'+tag, start_index)
    end = content.find('>', index) + 1
    location = (index, end)
    return location

def find_all_tags(contents, tag):
    index = 0
    index_list = []
    while index != -1:
        LOC = find_tag(contents, tag, index+1)
        index_list.append(LOC)
        index = LOC[0]
    return index_list

def del_tag(content, tag):
    loc = find_tag(content, tag)
    new_content = content[:loc[0]] + content[loc[1]:]
    return new_content

def mod_tag(content, tag, new_tag):
    loc = find_tag(content, tag)
    new_content = content[:loc[0]] + new_tag + content[loc[1]:]
    return new_content

def insert_tag(content, tag, index):
    new_content = content[:index] + tag + content[index:]
    return new_content

def process(funct_dic):
    ''' funct_dic key
    #  'path': 0,                 # file path to modify or 0(None) - expect: u'c:\\dir\file'  getting: C
    #  'extends': 0,              # name of base template          - expect: u'base.html'
    #  'static': 0,               # t/f
    #  'remove_html_tags': 0,     # t/f
    #  'url_conf': 0,             # t/f
    #  'disable_rel_path': 0,     # t/f
    #  'default_blocks': 0        # t/f
    '''
    log = logging.getLogger('main')
    fileslist = file_io.file_or_dir(funct_dic['path'])
    for a_file in fileslist:
        contents = file_io.get_contents(a_file)
        log.info("processing an html file: " + a_file)
        if funct_dic['extends']:
            contents = extend_base(contents, funct_dic['extends'])
        if funct_dic['default_blocks']:
            contents = default_blocks(contents)
        if funct_dic['remove_html_tags']:
            contents = remove_html_tags(contents)
        if funct_dic['disable_rel_path']:
            contents = remove_relative_path(contents)
        if funct_dic['static']:
            contents = staticfy_resource(contents, "src=")
            contents = staticfy_resource(contents, "href=")
        if funct_dic['url_conf']:
            contents = url_conf(contents)
        file_io.make_new_file(contents, a_file)
    return fileslist

if __name__ == "__main__":
    global log
    log = log_manager.log_manager("logs/staticfy_log.txt")
    if len(sys.argv) < 1:               # check for command line args first
        files = [                       # Or Add files to manage here
            # "example.html", "another.htm"
        ]
        mode = 1
    else:
        files = sys.argv
        mode = 1

    for each_file in files:
        process(each_file, mode)