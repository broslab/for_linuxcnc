### Comp_Map

Компенсация карты высот при фрезеровке печатных плат.

### Keyboard

Немного изменённая тема для виртуальной клавиатуры matchbox-keyboard.

### Macros

Макросы для встройки в Gmoccapy на вкладку MDI.

### NativeCAM

NativeCAM, в прошлом LinuxCNC Features, <br />
это набор шаблонных программ для создания Gкода обработки прямо на стойке. <br />
Доступны "мастера" для фрезерной, токарной обработки и плазменной резки. <br />

### Programs

Папка с разными программами обработки для LinuxCNC.

### PyNGCGUI

Создание простых программ обработки для токарного и фрезерного станка.
 
## Начинающему для LinuxCNC

Автоматический Вход <br />
в терминале ввести <br />
sudo geany /etc/lightdm/lightdm.conf <br />
раскомментировать <br />
autologin-user=ваше имя пользователя <br />

Изолирование Ядра <br />
в терминале ввести <br />
sudo geany /etc/default/grub <br />
добавить isolcpus=3 для 4х ядерного cpu <br />
GRUB_CMDLINE_LINUX_DEFAULT="quiet isolcpus=3" <br />
Обновить загрузчик <br />
в терминале ввести <br />
sudo update-grub <br />

Добавление архивных репозиториев <br />
в терминале ввести <br />
sudo geany /etc/apt/sources.list <br />
Для Debian 10 buster <br />
deb ht<span>tp​://archive.debian.org/debian buster main contrib non-free <br />
deb ht<span>tp://archive.debian.org/debian buster-updates main contrib non-free <br />
deb ht<span>tp​://archive.debian.org/debian-security buster/updates main contrib non-free <br />
не обезательно <br />
deb ht<span>tp://archive.debian.org/debian buster-backports main contrib non-free <br />
deb ht<span>tp://archive.debian.org/debian buster-proposed-updates main contrib non-free <br />
