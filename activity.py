#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Richar Nunez - rnezferreira9@gmail.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
from gettext import gettext as _
from ConfigParser import SafeConfigParser

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf

from sugar3.activity.activity import Activity
from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.graphics.toolbutton import ToolButton
from sugar3.graphics.icon import Icon
from sugar3.graphics import style


class HelpButton(Gtk.ToolItem):

    def __init__(self, **kwargs):
        Gtk.ToolItem.__init__(self)

        help_button = ToolButton('toolbar-help')
        help_button.set_tooltip(_('Ayuda / ÑepYsyrõ'))
        self.add(help_button)

        self._palette = help_button.get_palette()

        sw = Gtk.ScrolledWindow()
        sw.set_size_request(int(Gdk.Screen.width() / 2.8), 100)
        sw.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self._max_text_width = int(Gdk.Screen.width() / 3) - 600
        self._vbox = Gtk.Box()
        self._vbox.set_orientation(Gtk.Orientation.VERTICAL)
        self._vbox.set_homogeneous(False)
        self._vbox.set_border_width(10)

        hbox = Gtk.Box()
        hbox.pack_start(self._vbox, False, True, 0)

        sw.add_with_viewport(hbox)

        self._palette.set_content(sw)
        sw.show_all()

        help_button.connect('clicked', self.__help_button_clicked_cb)

    def __help_button_clicked_cb(self, button):
        self._palette.popup(immediate=True, state=1)

    def add_section(self, section_text):
        hbox = Gtk.Box()
        label = Gtk.Label()
        label.set_use_markup(True)
        label.set_markup('<b>%s</b>' % section_text)
        label.set_line_wrap(True)
        hbox.pack_start(label, False, False, 0)
        hbox.show_all()
        self._vbox.pack_start(hbox, False, False, padding=5)

    def add_paragraph(self, text, icon=None):
        hbox = Gtk.Box()
        label = Gtk.Label(label=text)
        label.set_justify(Gtk.Justification.LEFT)
        label.set_line_wrap(True)
        hbox.pack_start(label, False, False, 0)
        if icon is not None:
            _icon = Icon(icon_name=icon)
            hbox.add(_icon)

        hbox.show_all()
        self._vbox.pack_start(hbox, False, False, padding=5)


class Hablando_Guarani(Activity):

    def __init__(self, handle):
        Activity.__init__(self, handle)

        self._setup_toolbarbox()

        eb = Gtk.EventBox()
        eb.modify_bg(Gtk.StateType.NORMAL, Gdk.Color.parse("white")[1])
        self.set_canvas(eb)

        vbox = Gtk.VBox()
        eb.add(vbox)

        title = Gtk.Image.new_from_pixbuf(self._scale_pixbuf("images/logo.jpg", 400, 100))
        vbox.pack_start(title, False, False, 0)

        self.entry = Gtk.Entry()
        self.entry.connect("activate", self.translate_cb)
        self.entry.connect("backspace", self.backspace_cb)
        vbox.pack_start(self.entry, False, False, 0)

        scroll = Gtk.ScrolledWindow()
        vbox.pack_start(scroll, True, True, 0)

        self.textview = Gtk.TextView()
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
        scroll.add(self.textview)

        buttonbox = Gtk.HButtonBox()
        buttonbox.set_layout(Gtk.ButtonBoxStyle.CENTER)
        vbox.pack_start(buttonbox, False, False, 0)

        parser = SafeConfigParser()
        parser.read("config.ini")

        for data in [("dic", "A"), ("dic", "E"), ("dic", "I"), ("dic", "O"), ("dic", "U"), ("dic", "Y"), ("dic", "G")]:
            button = Gtk.Button(parser.get(*data))
            button.modify_bg(Gtk.StateType.NORMAL, Gdk.Color.parse('#FCB947')[1])
            button.connect("clicked", self.__add, data[1])
            buttonbox.add(button)

        achegety = Gtk.Image.new_from_pixbuf(self._scale_pixbuf("images/achegety.jpg", 600, 200))
        vbox.pack_start(achegety, False, False, 0)

        scroll = Gtk.ScrolledWindow()
        scroll.set_border_width(10)
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        vbox.pack_start(scroll, True, True, 0)

        textview = Gtk.TextView()
        textview.set_wrap_mode(Gtk.WrapMode.WORD)
        textview.set_editable(False)
        scroll.add(textview)

        self.buffer = textview.get_buffer()

        parser = SafeConfigParser()
        parser.read('config.ini')

        #Cargando archivo .txt
        path = "lang/guarani/dic.txt"
        if os.path.exists(path):
            infile = open("lang/guarani/dic.txt", "r")
            string = infile.read()
            infile.close()

            self.buffer.set_text(string)

        self.show_all()

    def _setup_toolbarbox(self):
        toolbarbox = ToolbarBox()
        self.set_toolbar_box(toolbarbox)

        toolbarbox.toolbar.insert(ActivityToolbarButton(self), -1)
        toolbarbox.toolbar.insert(Gtk.SeparatorToolItem(), -1)
        toolbarbox.toolbar.insert(StopButton(self), -1)

        names = ""
        parser = SafeConfigParser()
        parser.read("config.ini")
        for data in [("dic", "A"), ("dic", "E"), ("dic", "I"), ("dic", "O"), ("dic", "U"), ("dic", "Y"), ("dic", "G")]:
            names += parser.get(*data) + " "
        
        names = names[:-1]

        help_button = HelpButton()
        help_button.add_paragraph(_("Para traducir algo, debes escribirlo en la entrada de abajo y luego presionar enter."))
        help_button.add_paragraph(_("También puedes ver las traducciones abajo."))
        help_button.add_paragraph(_("Al precionar uno de los botones (%s), su texto se insertará en la entrada de escritura" % names))
        toolbarbox.toolbar.insert(help_button, 2)

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbarbox.toolbar.insert(separator, 3)

        toolbarbox.show_all()
        toolbarbox.toolbar.show_all()

    def _scale_pixbuf(self, path, width, height):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file('images/logo.jpg')
        return pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)

    def __add(self, button, data):
        parser = SafeConfigParser()
        parser.read('config.ini')
        self.entry.set_text(self.entry.get_text() + parser.get('dic', data))

    def translate_cb(self, entry):
        text = entry.get_text() + ' = '
        buffer = self.textview.get_buffer()
        infile = "lang/guarani/dic.txt"

        found = False

        with open(infile, 'r') as f:
            for line in f:
                if line.lstrip().startswith(text.capitalize()):
                    line = line.rstrip()
                    buffer.set_text(line)

                    found = True
                    break

        if not found:
            buffer.set_text('No se ha encontrado coincidencia')

    def backspace_cb(self, entry):
        buffer = self.textview.get_buffer()
        buffer.set_text('')

