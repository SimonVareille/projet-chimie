# -*- coding: utf-8 -*-

import kivy.utils as utils
from kivy.uix.settings import SettingItem
from kivy.properties import ObjectProperty
from kivy.lang import Builder

from kivymd.pickers import MDThemePicker


Builder.load_string(
'''
<SettingThemePicker>:
    Label:
        text: root.value or 'default'
''')
        
class SettingThemePicker(SettingItem):
    '''Implementation of a MDThemePicker setting on top of a :class:`SettingItem`.
    It is visualized with a :class:`~kivy.uix.label.Label` widget that, when
    clicked, will open a :class:`~kivymd.pickers.MDThemePicker` so the user can
    select customs colors.
    '''
    
    md_theme_picker = ObjectProperty(None)
    '''(internal) Used to store the current MDThemePicker and
    to listen for changes.
    :attr:`md_theme_picker` is an :class:`~kivy.properties.ObjectProperty` and defaults
    to None.
    '''

    def on_panel(self, instance, value):
        if value is None:
            return
        self.bind(on_release=self._theme_picker_open)
        
    def _theme_picker_open(self, instance):
        if not self.md_theme_picker:
            self.md_theme_picker = MDThemePicker()
            self.md_theme_picker.bind(on_dismiss=self._validate)
        self.md_theme_picker.open()

    def _validate(self, instance):
        #value = self.textinput.text.strip()
        value = self.md_theme_picker.theme_cls.theme_style\
                + ", " + self.md_theme_picker.theme_cls.primary_palette\
                +", " + self.md_theme_picker.theme_cls.accent_palette
        self.value = value
        
