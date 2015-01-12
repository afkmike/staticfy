__author__ = 'mike@afkconcepts.com'
"""
    gui.py classes extend facade classes
    to provide functionality in the ui
"""
import wx
import facade
import process_html
import process_py


class MyFrame(facade.main_window):
    def __init__(self, parent):
        super(MyFrame, self).__init__(parent)
        self.show_actions(self)
        self.show_picker_type(self)

    def show_picker_type(self, event=None):
        ########### Clear the process_type_panel #############
        current_picker = self.process_type_panel.GetChildren()
        while current_picker:
            self.process_type_panel.Hide(0)
            self.process_type_panel.Remove(0)

        ########## Figure out which picker to show ##############
        # clause definitions by combo list index:
        single = 0
        multi = 1
        type_selected = self.processing_type_combo.GetCurrentSelection()
        if type_selected == single:
            self.Label11 = wx.StaticText(self, wx.ID_ANY, u"Select a File", wx.DefaultPosition, wx.DefaultSize, 0)
            self.Label11.Wrap(-1)
            self.Label11.SetFont(wx.Font(11, 70, 90, 90, False, wx.EmptyString))

            self.process_type_panel.Add(self.Label11, 0, wx.ALL, 5)

            self.m_filePicker1 = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*",
                                                   wx.DefaultPosition, wx.Size(400, -1),
                                                   wx.FLP_DEFAULT_STYLE | wx.FLP_FILE_MUST_EXIST | wx.FLP_USE_TEXTCTRL)
            self.process_type_panel.Add(self.m_filePicker1, 0, wx.ALL, 5)
        elif type_selected == multi:
            self.Label1 = wx.StaticText(self, wx.ID_ANY, u"Select a Folder", wx.DefaultPosition, wx.DefaultSize, 0)
            self.Label1.Wrap(-1)
            self.Label1.SetFont(wx.Font(11, 70, 90, 90, False, wx.EmptyString))

            self.process_type_panel.Add(self.Label1, 0, wx.ALL, 5)

            self.m_dirPicker1 = wx.DirPickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"Select a folder",
                                                 wx.DefaultPosition, wx.Size(400, -1),
                                                 wx.DIRP_DEFAULT_STYLE | wx.DIRP_DIR_MUST_EXIST | wx.DIRP_USE_TEXTCTRL)
            self.process_type_panel.Add(self.m_dirPicker1, 0, wx.ALL, 5)

            self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"Note: Entering a directory will modify all files.",
                                               wx.DefaultPosition, wx.DefaultSize, 0)
            self.m_staticText2.Wrap(-1)
            self.process_type_panel.Add(self.m_staticText2, 0, wx.ALL, 5)
        else:
            # something went wrong, fuck, lol
            pass
        self.Layout()
        self.Fit()

    def show_actions(self, event=None):
        # ########### Clear the actions_panel ############
        action_items = self.actions_panel.GetChildren()
        while action_items:
            self.actions_panel.Hide(0)
            self.actions_panel.Remove(0)

            ############ Determine new actions to display #############
        # clause definitions by combo list index:
        html = 0
        python = 1
        file_type_selected = self.file_type_selector.GetCurrentSelection()
        if file_type_selected == html:
            # show some html file functions
            sbSizer3 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"HTML Actions"), wx.VERTICAL)
            bSizer18 = wx.BoxSizer(wx.VERTICAL)
            bSizer19 = wx.BoxSizer(wx.HORIZONTAL)

            self.extends = wx.CheckBox(self, wx.ID_ANY, u"Extends :", wx.DefaultPosition, wx.DefaultSize, 0)
            bSizer19.Add(self.extends, 0, wx.ALL, 5)

            self.base_file = wx.TextCtrl(self, wx.ID_ANY, u"base.html", wx.DefaultPosition, wx.DefaultSize, 0)
            bSizer19.Add(self.base_file, 0, wx.ALL, 5)
            bSizer18.Add(bSizer19, 0, wx.EXPAND, 5)

            self.static_res = wx.CheckBox(self, wx.ID_ANY, u"Link Static Resources", wx.DefaultPosition, wx.DefaultSize, 0)
            bSizer18.Add(self.static_res, 0, wx.ALL, 5)

            self.rem_html_tags = wx.CheckBox(self, wx.ID_ANY, u"Remove <html> and </html> tags", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
            bSizer18.Add(self.rem_html_tags, 0, wx.ALL, 5)

            self.url_conf = wx.CheckBox(self, wx.ID_ANY, u"Configure URLs", wx.DefaultPosition, wx.DefaultSize, 0)
            bSizer18.Add(self.url_conf, 0, wx.ALL, 5)

            self.dis_rel_path = wx.CheckBox(self, wx.ID_ANY, u"Disable Relative Paths\n(delete all instances of ../)",
                                            wx.DefaultPosition, wx.DefaultSize, 0)
            bSizer18.Add(self.dis_rel_path, 0, wx.ALL, 5)

            self.def_blocks = wx.CheckBox(self, wx.ID_ANY,
                                          u"Default Inheritance Blocks\n{% block head_block %}\n        and\n{% block body_content %}",
                                          wx.DefaultPosition, wx.DefaultSize, 0)
            bSizer18.Add(self.def_blocks, 0, wx.ALL, 5)
            sbSizer3.Add(bSizer18, 1, wx.EXPAND, 5)
            self.url_conf.Bind( wx.EVT_CHECKBOX, self.sync_rel_path )

        elif file_type_selected == python:
            # TODO show some python file functions
            sbSizer3 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Python Actions"), wx.VERTICAL)
            temp_label = wx.StaticText(self, wx.ID_ANY, u"TODO: Add some on demand Python Functions! ",
                                       wx.DefaultPosition, wx.DefaultSize, 0)
            sbSizer3.Add(temp_label, 0, wx.ALL, 5)
        else:
            # something fucked up, deal with it
            sbSizer3 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Unrecognized Actions"), wx.VERTICAL)
            temp_label = wx.StaticText(self, wx.ID_ANY, u"Unrecognized Selection! Please try again. ",
                                       wx.DefaultPosition, wx.DefaultSize, 0)
            sbSizer3.Add(temp_label, 0, wx.ALL, 5)

        self.actions_panel.Add(sbSizer3)
        confirm_actions_button = wx.Button(self, wx.ID_ANY, u"Confirm Actions and Process File(s)", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.actions_panel.Add(confirm_actions_button)
        confirm_actions_button.Bind(wx.EVT_BUTTON,
                                    self.process)  # self.process() is an idiomatic representation of the actual process
                                                   # and decision function in each process_ file
        self.Layout()
        self.Fit()

    def sync_rel_path(self, event):
        checked = self.url_conf.GetValue()
        self.dis_rel_path.SetValue(checked)
        if checked:
            self.dis_rel_path.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW))
            self.dis_rel_path.Enable(False)
        else:
            self.dis_rel_path.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))
            self.dis_rel_path.Enable(True)

    def process(self, event):
        # TODO gather variables, pass to actual process and then show in diff_view
        '''
            self.processing_type_combo.GetCurrentSelection() will tell what processing type to expect (0=file,1=dir)
                based on this get the correct picker:
                    self.m_filePicker1 or self.m_dirPicker1
                    .GetPath() and .GetTextCtrlValue() both obtain path as a String
            self.file_type_selector.GetCurrentSelection() will tell what file type to expect (0=html,1=python)
        '''
        # indexes :
        html = 0
        python = 1
        file = 0
        dir = 1
        # dictionary by process :
        function_dict_html = {'path': "path",            # file path to modify     - expect: u'c:\\dir\file'
                              'extends': 0,              # name of base template   - expect: u'base.html'
                              'static': 0,               # t/f
                              'remove_html_tags': 0,     # t/f
                              'url_conf': 0,             # t/f
                              'disable_rel_path': 0,     # t/f
                              'default_blocks': 0        # t/f
                              }
        function_dict_python = {'path': 0                # file path to modify or 0(None) - expect: u'c:\\dir\file'
                                # TODO make some functions and add to dictionary
                                }
        file_type = self.file_type_selector.GetCurrentSelection()
        this_dic = [function_dict_html, function_dict_python]   # now you can access the correct dictionary with - this_dic[file_type]

        processing_type = self.processing_type_combo.GetCurrentSelection()
        if processing_type == file:
            path_to_mod = self.m_filePicker1.GetTextCtrlValue()
        if processing_type == dir:
            path_to_mod = self.m_dirPicker1.GetTextCtrlValue()
        if path_to_mod == "":
            # TODO show 'you didn't enter a file to modify, moron' dialog
            pass
        else:
            this_dic[file_type]['path'] = path_to_mod
            print "in gui we retrieve path as: " + path_to_mod + " and dict stored: " + this_dic[file_type]['path']

        if file_type == html:
            if self.extends.IsChecked():
                this_dic[file_type]['extends'] = self.base_file.GetValue()
            this_dic[file_type]['static'] = self.static_res.IsChecked()
            this_dic[file_type]['remove_html_tags'] = self.rem_html_tags.IsChecked()
            this_dic[file_type]['url_conf'] = self.url_conf.IsChecked()
            this_dic[file_type]['disable_rel_path'] = self.dis_rel_path.IsChecked()
            this_dic[file_type]['default_blocks'] = self.def_blocks.IsChecked()
            filenames = process_html.process(this_dic[file_type])
        if file_type == python:
            # TODO add some input to the dict items you make
            pass

        diff = facade.diff_view(None)
        diff.files_combo.Append(filenames)
        diff.Show()

    def clear_log_contents(self, event):
        self.console.Clear()

    def submit_log_contents(self, event):
        # TODO consider/reconsider
        pass

######################################## Menu item stuff goes in here ##################################################
    def show_about_dialog(self, parent):            # Help Menu : About button
        about = facade.about_dialog(None)
        about.Show()

    def close_program(self, event):               # File Menu : Exit button
        self.Close()
########################################################################################################################

app = wx.App()
frame = MyFrame(None)
frame.Show()
app.MainLoop()