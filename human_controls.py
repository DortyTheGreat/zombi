'''

Закинем сюда куча глобальных переменных, чтобы удобнее контролировать

Основные идеи:

1. Стратегии.
Мы играем и можем вручную поменять стратегию AI:
1.1 Расширение Амёбы (уже реализовано, двигаемся во все стороны, тратим деньги на все деньги)
1.2 Сохранение формы - не тратим много денег, чтобы расширять границы
1.3 ЧЕРЕПАХА - агрессивно строимся лишь около центра

'''

player_mode = 'expand' # 'expand' 'save' 'turtle'

player_move_x = None
player_move_y = None
clicked_squares = set()