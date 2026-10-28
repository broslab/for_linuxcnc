NGCGUI Gmoccapy
Скопировать pyngcgui.ui в папку станка.

В ваш станок.ini добавить:

[DISPLAY]
EMBED_TAB_NAME = NGCGUI
EMBED_TAB_LOCATION = ntb_user_tabs
EMBED_TAB_COMMAND = gladevcp -x {XID} pyngcgui.ui
NGCGUI_SUBFILE = проточка.ngc
NGCGUI_SUBFILE = расточка.ngc
NGCGUI_SUBFILE = сверление.ngc

[RS274NGC]
SUBROUTINE_PATH = ngcgui
если уже есть папка, например macros
то папки пишем через : без пробелов.
SUBROUTINE_PATH = macros:ngcgui