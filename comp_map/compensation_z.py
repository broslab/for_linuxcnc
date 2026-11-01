#!/usr/bin/env python
# -*- coding:UTF-8 -*-
"""
    This file will control Compensation Z addition to Gmoccapy interface
    for LinuxCNC machines

    Copyright (C) 2014 Serguei Glavatski, gsngla@gmail.com

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

"""

import hal                  # base hal class to react to hal signals
import hal_glib             # needed to make our own hal pins
import gtk                  # base for pygtk widgets and constants
import linuxcnc             # to get our own error sytsem
import gobject              # needed to add the timer for periodic


work_thread = 50            # work_thread means how often pins will be updated (ms)
filename    = "filename.txt"# file for scan results dump

from gmoccapy import preferences
from gmoccapy import getiniinfo

class CompensationzClass:

    def __init__(self, halcomp, builder, useropts):
        self.builder = builder
        get_ini_info = getiniinfo.GetIniInfo()
        prefs = preferences.preferences(get_ini_info.get_preference_file_path())
        theme_name = prefs.getpref("gtk_theme", "Follow System Theme", str)
        if theme_name == "Follow System Theme":
            theme_name = gtk.settings_get_default().get_property("gtk-theme-name")
        gtk.settings_get_default().set_string_property("gtk-theme-name", theme_name, "")
        self.stat = linuxcnc.stat()
        # get all widgets and connect them
        # получить все виджеты и подключите их
        self.deltaZ = self.builder.get_object("deltaZ")
        self.realZ = self.builder.get_object("realZ")
        self.adj_comp_scale = self.builder.get_object("adj_comp_scale")
        self.adj_comp_scale.set_sensitive(False)
        self.enable_comp = self.builder.get_object("enable_comp")
        self.enable_comp.connect("toggled", self.enable_comp_toggled)
        self.reset_comp = self.builder.get_object("reset_comp")
        self.reset_comp.connect("clicked", self.comp_reset_click)
        self.enable_comp.modify_bg(gtk.STATE_ACTIVE, gtk.gdk.color_parse("#FFFF00"))
        self.reset_comp.modify_bg(gtk.STATE_ACTIVE, gtk.gdk.color_parse("#FFFF00"))
        # prepare height map
        # подготовить карту высот
        self.h=hal.component("compensation_z_math")
        self.h.newpin("out", hal.HAL_FLOAT, hal.HAL_OUT)
        self.h.newpin("enable",hal.HAL_BIT, hal.HAL_IN)
        self.h.newpin("x_map", hal.HAL_FLOAT, hal.HAL_IN)
        self.h.newpin("y_map", hal.HAL_FLOAT, hal.HAL_IN)
        self.h.newpin("reset", hal.HAL_BIT, hal.HAL_IN)
        self.h.newpin("error", hal.HAL_BIT, hal.HAL_OUT)
        self.h["error"] = True
        self.comp = {}
        self.x_coords = []
        self.y_coords = []
        self.range_x,self.range_y, self.len_x,self.len_y = [],[], 0,0
        self.last_reset = False
        self.timeout_id = 0
        self.map_ok = False     # True only when a complete rectangular map is loaded

    # timer tracking function
    # функция отслеживания по таймеру
    def _update_realz( self ):
        self.stat.poll()
        compensation_change = float( self.deltaZ.hal_pin.get() )
        self.realZ.set_text( "%.3f" % float( compensation_change + self.stat.actual_position[2] ) )
        self.deltaZ.set_text( "%.3f" % float( compensation_change ) )
        # map create iteration
        # итерация создания карты
        h=self.h
        try:
            # reset (reopen) on rising edge of the signal
            # перезагрузка карты по фронту сигнала reset
            if h["reset"] and not self.last_reset:
                self.reopen()
            self.last_reset = h["reset"]
            if h["enable"] and self.map_ok:
                h["out"]=self.get_comp(h['x_map'],h['y_map']) # result of iteration  Результат итерации
            else :
                h["out"]=0
            # error mirrors the real state of the map, it is NOT cleared just because the loop ran without exceptions
            h["error"] = not self.map_ok
        except Exception:
            h["out"]=0
            h["error"]=True
        return True

    # drop the current map completely
    # полностью сбросить текущую карту
    def _clear_map(self):
        self.comp = {}
        self.x_coords = []
        self.y_coords = []
        self.len_x = self.len_y = 0
        self.range_x = self.range_y = []
        self.map_ok = False

    # read scanned data from filename
    # считывание отсканированных данных из filename
    def reopen(self) :
        # the old map is always dropped first: if the new file is bad, no old map must stay active
        # старая карта всегда сбрасывается: если новый файл испорчен, старая не должна остаться
        self._clear_map()
        self.h["error"] = True
        comp = {}
        xs, ys = set(), set()
        try:
            with open(filename, "r") as f:
                for line in f:
                    if not line.strip():
                        continue
                    x,y,z = [float(i) for i in line.split()[0:3]]
                    x,y = round(x,4), round(y,4)
                    comp.setdefault(x, {})[y] = z
                    xs.add(x)
                    ys.add(y)
        except (IOError, OSError, ValueError) as e:
            print("ERROR! Can not read map file %s: %s" % (filename, e))
            return False
        if not comp:
            print("ERROR! Map file %s is empty" % filename)
            return False
        # check map integrity, map should be rectangular!
        # проверьте целостность карты, карта должна быть прямоугольной!
        for x in xs :
            for y in ys :
                if y not in comp.get(x, {}) :
                    print("ERROR! Map should be rectangular!\nCan not find point X %s Y %s"%(x,y))
                    return False
        # everything is fine - only now publish the new map
        # всё хорошо - только теперь применяем новую карту
        self.comp = comp
        self.x_coords = sorted(xs)
        self.y_coords = sorted(ys)
        self.len_x = len(self.x_coords)
        self.range_x = range(self.len_x)
        self.len_y = len(self.y_coords)
        self.range_y = range(self.len_y)
        self.map_ok = True
        self.h["error"] = False
        return True

    # math approximation - calculated on a weighted average of four points
    # математическая аппроксимация - рассчитывается на основе средневзвешенного значения из четырех пунктов
    def get_comp(self,x,y) :
        x = max(self.x_coords[0],min(self.x_coords[-1],x))
        y = max(self.y_coords[0],min(self.y_coords[-1],y))
        i = 0
        while i<self.len_x :
            if self.x_coords[i]>x : break
            i+=1
        j = 0
        while j<self.len_y :
            if self.y_coords[j]>y : break
            j+=1
        if i==self.len_x : i -= 1
        if j==self.len_y : j -= 1
        x2=self.x_coords[i]
        y2=self.y_coords[j]
        if i<self.len_x:
            x1 = self.x_coords[max(0,i-1)]
        else:
            x1 = x2
        if j<self.len_y:
            y1 = self.y_coords[max(0,j-1)]
        else:
            y1 = y2
        # now make bilinear interpolation of the points
        # теперь выполните билинейную интерполяцию точек
        if x1 != x2 :
            z1 = ((x2-x)*self.comp[x1][y1] + (x-x1)*self.comp[x2][y1])/(x2-x1)
            z2 = ((x2-x)*self.comp[x1][y2] + (x-x1)*self.comp[x2][y2])/(x2-x1)
        else:
            z1 = self.comp[x1][y1]
            z2 = self.comp[x1][y2]
        if y1 != y2 :
            z1 = ((y2-y)*z1 + (y-y1)*z2)/(y2-y1)
        return z1

    # this function performed by pressing button "Open"
    # эта функция выполняется нажатием кнопки "Открыть"
    def comp_reset_click(self, widget, data = None):
        self.reopen()
        self.last_reset = self.h["reset"]

    # toggle "Play" button
    # переключить кнопку "Воспроизведение"
    def enable_comp_toggled(self, widget, data = None):
        if widget.get_active(): # "Play" button is active, run timer  Кнопка "Play" активна, запускается таймер
            self.timeout_id = gobject.timeout_add(work_thread, self._update_realz) # time between calls to the function, in milliseconds  Время между вызовами функции в миллисекундах
            self.adj_comp_scale.set_sensitive(True)
        else:
            if self.timeout_id :
                gobject.source_remove(self.timeout_id) # stop timer  Остоновить таймер
                self.h["out"]=0
                self.adj_comp_scale.set_sensitive(False)
                self.deltaZ.set_text( "%.3f" % float( float( self.deltaZ.hal_pin.get() )) )
                self.stat.poll()
                self.realZ.set_text( "%.3f" % float( self.stat.actual_position[2] ) )


def get_handlers(halcomp,builder,useropts):
    return(CompensationzClass(halcomp,builder,useropts))