### Macros

Макросы на вкладку MDI интерфейса Gmoccapy<br />

Создать папку macros в папке станка, <br />
в неё поместить ваши макросы. <br />

Добавить в Ваш станок.ini <br />

[MACROS] <br />
MACRO = probe_z <br />
MACRO = go_to_zero <br />
MACRO = go_to_home <br />

[RS274NGC] <br />
SUBROUTINE_PATH = macros <br />
если уже есть папка, например ngcgui <br />
то папки пишем через : без пробелов. <br />
SUBROUTINE_PATH = ngcgui:macros <br />
