__author__ = 'mike@afkconcepts.com'
"""
process_html is a django integration script for new html files
"""

import sys
import os
import log_manager
import file_io
import process_py

log = log_manager.log_manager("logs/staticfy_log.txt")

def extend_base(contents, template='base.html'):
    """######################################################################################
    # check for {% extends "base.html" %} tag then inserts after doctype                    #
    # ###USAGE: this function can be "independently" called by process or any flow control  #
    #           will apply only to non-template files                                       #
    ######################################################################################"""
    EXTENDS_BASE_TAG = '{% extends \"' + template + '\" %}'
    EXTENDS_BASE_INDEX = contents.find(EXTENDS_BASE_TAG)
    if EXTENDS_BASE_INDEX == -1:
        log.log.info("Extends base.html tag was inserted")
        AFTER_DOCTYPE = contents.find(">")+1  # safe enchant to +3   o.0
        new_contents = contents[:AFTER_DOCTYPE] + "\n" + EXTENDS_BASE_TAG + "\n" + contents[AFTER_DOCTYPE:]
        return new_contents
    else:
        log.log.info("Extends tag found prior to insert. Process aborted.")
        return contents

def load_staticfiles(contents):
    """######################################################################################
    # check for {% load staticfiles %} tag                                                  #
    # then inserts after either {% extends base.html %} (if it exists) or doctype           #
    # ###USAGE: this function will be called by staticfy_resource() to ensure staticfiles   #
    #           is loaded before any linking is attempted                                   #
    ######################################################################################"""
    LOAD_SF_TAG = "{% load staticfiles %}"
    LOAD_SF_INDEX = contents.find(LOAD_SF_TAG)
    if LOAD_SF_INDEX != -1:
        return contents
    else:
        EXTENDS_BASE_TAG = "{% extends \"base.html\" %}"
        EXTENDS_BASE_INDEX = contents.find(EXTENDS_BASE_TAG)
        if EXTENDS_BASE_INDEX > 0:
            log.log.info("Load staticfiles tag inserted after extends base.html tag")
            EXTENDS_BASE_INDEX += len(EXTENDS_BASE_TAG)+1
            new_contents = contents[:EXTENDS_BASE_INDEX] + "\n" + LOAD_SF_TAG + "\n" + contents[EXTENDS_BASE_INDEX:]
        else:
            log.log.info("Load staticfiles tag inserted after DOCTYPE tag")
            AFTER_DOCTYPE = contents.find(">")+1
            new_contents = contents[:AFTER_DOCTYPE] + "\n" + LOAD_SF_TAG + "\n" + contents[AFTER_DOCTYPE:]
        return new_contents

def staticfy_resource(contents, res_type):  # TODO ignore <a>
    """######################################################################################
    #  designed to link all resources to the staticfiles dir                                #
    #  calls load_staticfiles() to ensure the files are loaded before trying to link        #
    #  generalized to require you pass the resource type (ie. src=, href= (REMEMBER = !))   #
    # ###USAGE: Don't forget the = or it won't work right!                                  #
    #           Safe to call on template and non-template files                             #
    ######################################################################################"""
    contents = load_staticfiles(contents)

    RES_INDEX = 0
    STATIC_TAG_FRONT = '\"{% static '
    STATIC_TAG_BACK = ' %}\"'
    STATIC_FRONT_LEN = len(STATIC_TAG_FRONT)+1
    STATIC_BACK_LEN = len(STATIC_TAG_BACK)+1
    OFFSET = len(res_type)
    while RES_INDEX != -1:
        RES_INDEX = contents.find(res_type, RES_INDEX)
        if RES_INDEX != -1:
            RES_INDEX += OFFSET
        else:
            break
        ALREADY_LINKED = contents.find(STATIC_TAG_FRONT, RES_INDEX, (RES_INDEX+STATIC_FRONT_LEN))
        if ALREADY_LINKED == -1:
            log.log.info("Resource of type: " + res_type + " FOUND! STATICFYING!")
            new_contents = contents[:RES_INDEX] + STATIC_TAG_FRONT + contents[RES_INDEX:]
            contents = new_contents
            quotes = contents.find("\"", (RES_INDEX+STATIC_FRONT_LEN))
            quotes += 1
            new_contents = contents[:quotes] + STATIC_TAG_BACK + contents[quotes:]
            contents = new_contents
        else:
            break
    contents = staticfy_preload(contents)
    log.log.info("ALL RESOURCES ARE STATICFIED!")
    return contents

def staticfy_preload(contents):
    """######################################################################################
    #  designed to staticfy preloaded resources in format :                                 #
    #  <script ...> $(["file.ext","file2.ext"]).preloadImg(); </script>                     #
    # ###USAGE: this will be called from staticfy_resource() to ensure staticfiles are      #
    #           already in use in given file                                                #
    ######################################################################################"""
    STATIC_TAG_FRONT = '\"{% static '
    STATIC_TAG_BACK = ' %}\"'
    FRONT_INDICATOR = '$(['
    BACK_INDICATOR = '])'
    front_index = 0
    back_index = 0
    while front_index != -1:
        front_index = contents.find(FRONT_INDICATOR, back_index)
        back_index = contents.find(BACK_INDICATOR, front_index)
        file_list = contents[(front_index+len(FRONT_INDICATOR)):back_index]
        thing = file_list.split(',')
        file_list = ""
        for item in thing:
            file_list += STATIC_TAG_FRONT + item + STATIC_TAG_BACK + ","
        file_list = file_list[:-1]
        new_contents = contents[:(front_index+len(FRONT_INDICATOR))] + file_list + contents[back_index:]
        contents = new_contents
        log.log.info("A script preload list has been STATICFIED!")
    return contents

def url_conf(contents):  # TODO make this independent from staticfy
    """######################################################################################
    # designed to match all hyperlinks to their django url configuration                    #
    # ###USAGE: this function can be "independently" called by process() or any flow control#
    ######################################################################################"""
    link_index = 0
    bracket_index = 0
    ANCHOR_TAG = '<a'
    ATTRIBUTE = 'href='
    OFFSET_1 = len('href="{% ')             # pos to add 'url'
    OFFSET_2 = len('href="{% static "')     # pos to put trimmed url
    url_list = []
    while link_index != -1:
        link_index = contents.find(ANCHOR_TAG, bracket_index)
        if link_index == -1:
            break
        else:
            ATTRIBUTE_INDEX = contents.find(ATTRIBUTE, link_index)
            DOT_INDEX = contents.find('.', (ATTRIBUTE_INDEX + OFFSET_2))
            bracket_index = contents.find('}', DOT_INDEX)
            URL_FRONT = ATTRIBUTE_INDEX + OFFSET_2
            URL = contents[URL_FRONT: DOT_INDEX]
            url_list.append(URL)
            log.log.info("Url revised : " + URL)
            NEW_LINK = 'url \"' + URL + '\" %'
            new_contents = contents[:(ATTRIBUTE_INDEX+OFFSET_1)] + NEW_LINK + contents[bracket_index:]
            contents = new_contents
    process_py.process_py(url_list)
    return contents

def default_blocks(contents):
    """######################################################################################
    #  designed to insert the default inherited blocks (head_block and body_content)        #
    #  declarations are verbose to avoid naming errors                                      #
    #  could probably generalize to make less redundant, but must remain scalable           #
    # ###USAGE: called during process() when in child page mode                             #
    ######################################################################################"""
    HEAD_BLOCK_OPEN = '{% block head_block %}'
    BODY_BLOCK_OPEN = '{% block body_content %}'
    BLOCK_CLOSE = '{% endblock %}'

    HEAD_TAG = '<head'
    HEAD_FRONT = contents.find(HEAD_TAG)
    if HEAD_FRONT > -1:
        HEAD_BACK = contents.find(">", HEAD_FRONT) + 1  # move past > char
        new_contents = contents[:HEAD_FRONT] + HEAD_BLOCK_OPEN + contents[HEAD_BACK:]
        contents = new_contents
        log.log.info("Head block inserted")

    HEAD_CLOSE_TAG = '</head>'
    HEAD_CLOSE_FRONT = contents.find(HEAD_CLOSE_TAG)
    if HEAD_CLOSE_FRONT > -1:
        HEAD_CLOSE_BACK = HEAD_CLOSE_FRONT + len(HEAD_CLOSE_TAG)
        new_contents = contents[:HEAD_CLOSE_FRONT] + BLOCK_CLOSE + contents[HEAD_CLOSE_BACK:]
        contents = new_contents
        log.log.info("Head block close inserted")

    BODY_TAG = '<body'
    BODY_FRONT = contents.find(BODY_TAG)
    if BODY_FRONT > -1:
        BODY_BACK = contents.find(">", BODY_FRONT) + 1  # move past > char
        new_contents = contents[:BODY_FRONT] + BODY_BLOCK_OPEN + contents[BODY_BACK:]
        contents = new_contents
        log.log.info("Body block inserted")

    BODY_CLOSE_TAG = '</body>'
    BODY_CLOSE_FRONT = contents.find(BODY_CLOSE_TAG)
    if BODY_CLOSE_FRONT > -1:
        BODY_CLOSE_BACK = BODY_CLOSE_FRONT + len(BODY_CLOSE_TAG)
        new_contents = contents[:BODY_CLOSE_FRONT] + BLOCK_CLOSE + contents[BODY_CLOSE_BACK:]
        contents = new_contents
        log.log.info("Body block close inserted")

    return contents

def remove_html_tags(contents):
    """######################################################################################
    # this function simply seeks and eliminates html tags from inheriting pages             #
    # ###USAGE: this function is called in process() when in child page mode                #
    ######################################################################################"""
    HTML_TAG = '<html'
    END_OF_HTML_TAG = '>'
    HTML_CLOSE_TAG = '</html>'
    tag_index = contents.find(HTML_TAG)
    end_index = contents.find(END_OF_HTML_TAG, tag_index) + 1  # move past >
    if tag_index > -1:
        new_contents = contents[:tag_index] + contents[end_index:]
        contents = new_contents
        log.log.info(HTML_TAG + END_OF_HTML_TAG + " removed")
    tag_index = contents.find(HTML_CLOSE_TAG)
    if tag_index > -1:
        new_contents = contents[:tag_index]
        contents = new_contents
        log.log.info(HTML_CLOSE_TAG + " removed")
    return contents

def remove_relative_path(contents):
    """######################################################################################
    # this function simply seeks and eliminates relative path indicators ( ../ )            #
    # ###USAGE: this function is called in process() for child or template mode             #
    ######################################################################################"""
    REL_PATH = '../'
    rel_path_loc = 0
    while rel_path_loc != -1:
        rel_path_loc = contents.find(REL_PATH, rel_path_loc)
        if rel_path_loc != -1:
            rel_path_end = rel_path_loc + len(REL_PATH)
            new_contents = contents[:rel_path_loc] + contents[rel_path_end:]
            contents = new_contents
    return contents

''' original version
def process(a_file, mode):
    """######################################################################################
    # single call helper function encapsulates flow control by file type                    #
    # ###USAGE: this function is called from __main__ to automate typical processing        #
    ######################################################################################"""
    # TODO implement base template configurations!!
    # (MODE == PAGE_TYPE)
    # if mode = base

    # if mode = content
    # Standard Child template process:
    if mode == 1:
        contents = file_io.get_contents(a_file)
        contents = default_blocks(contents)
        contents = remove_html_tags(contents)
        contents = remove_relative_path(contents)
        contents = staticfy_resource(contents, "src=")
        contents = staticfy_resource(contents, "href=")
        contents = url_conf(contents)
        file_io.make_new_file(contents, a_file)
    return
'''
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
    fileslist = file_io.file_or_dir(funct_dic['path'])
    for a_file in fileslist:
        contents = file_io.get_contents(a_file)
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