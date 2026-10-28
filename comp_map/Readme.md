### Gmoccapy

Дополнение Compensation Z к интерфейсу Gmoccapy используется для отслеживания <br />
с высокой точностью перепада высот обрабатываемой детали по Z в таких операциях, <br />
как поверхностная гравировка, фрезеровка дорожек печатных плат и других случаях, <br />
когда необходимо ‘повторять’ неровную поверхность детали и нельзя срезать лишнее. <br />

Процесс состоит из двух частей:
1. Сканирование поверхности с помощью щупа (probe). <br />
Позже добавлю программы в папку programs и pyngcgui. <br />

2. Фрезеровка с включенной функцией Compensation Z. <br />
Нажимаем «Open», затем «Enable» <br />
Автоматическая компенсация включена. <br />
Запускаем свою программу обработки поверхности .ngc <br />
Для выключения компенсации ещё раз нажимаем «Enable» <br />

### Установка

Скопировать в папку станка: <br />
compensation_z.glade <br />
compensation_z.hal <br />
compensation_z.py <br />
filename.txt <br />

Добавить в .ini файл: <br />
[DISPLAY] <br />
EMBED_TAB_NAME = my_new_panel <br />
EMBED_TAB_LOCATION = box_spindle <br />
EMBED_TAB_COMMAND = gladevcp -x {XID} -u compensation_z.py -H compensation_z.hal compensation_z.glade <br />

