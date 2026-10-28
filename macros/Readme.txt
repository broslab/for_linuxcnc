Macros

Макросы добавляются во вкладку MDI

Создать папку macros в папке станка,
в неё поместити ваши макросы.

Добавить в Ваш станок.ini

[MACROS]
MACRO = probe_z
MACRO = go_to_zero
MACRO = go_to_home

[RS274NGC]
SUBROUTINE_PATH = macros
если уже есть папка, например ngcgui
то папки пишем через : без пробелов.
SUBROUTINE_PATH = ngcgui:macros