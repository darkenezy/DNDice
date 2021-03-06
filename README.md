# DNDice
### Веб-приложение для любителей побросать кубики.
Развернуто тут: http://18.219.240.23:8080/game
- Если ссылка вдруг недоступна, просьба пингануть @Darkenezy в дискорде
- Что-то, а AWS нынче работает как попало!

### В приложении можно:
- Добавить кости D4/D6/D8/D10/D12/D20/D50 на игровое поле!
- Убрать кость с игрового поля (кликом)!
- Очистить игровое поле!
- Бросить все кости на игровом столе!
- Увидеть сумму выпавших очков!
- Выиграть! (нет)

### Стек:
- Python3 (flask)
- MongoDB

### Как все это поднять?
```
git clone https://github.com/darkenezy/DNDice.git
cd DNDice
docker-compose up --build -d
```
## Ответы на вопросы
### Полагаю что пользователи приложения могли бы захотеть:
- Возможность создания своих кубиков с заданными гранями
- Возможность создания сессий, в которых ГеймМастер (ГМ, Ведущий) сможет разрешать игрокам бросить кубик.
- Возможность получить историю бросков, чтобы проверить действительно ли кубик в среднем выбрасывает свое матожидание.
Говорят, что у одного ГМа в нашей таверне бросок двух D6 в опасной ситуации всегда заканчивается как snake eyes.

### В качестве продвижения, данную разработку можно использовать двумя способами: 
- В качестве приложения, которое будут использовать игроки во время оффлайн партий вместо физическиих
кубиков. (Тут следует напомнить игрокам, сколько раз они роняли кости на пол/под диван/холодильник или возможно даже пытались отнять их у собаки).
- В качестве части цифровой версии ролевой игры.
В обоих случаях главное убедить игроков, что с этой разработкой удача всегда будет на их стороне!
