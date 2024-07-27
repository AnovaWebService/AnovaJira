
NOT_AUTHORIZED = Exception("Вы не авторизованы!")

WORKSPACE_NOT_FOUND = Exception("Рабочее пространство не было найдено.")
WORKSPACE_ALREADY_EXISTS = Exception("Рабочее пространство с таким именем уже существует.")
WORKSPACE_UPDATE_NOT_PERMITTED = Exception("У Вас нет прав на редактирование данного рабочего пространства.")
WORKSPACE_NOT_A_PARTICIPANT = Exception("Вы не являетесь участником данного рабочего пространства.")
WORKSPACE_BOARD_CREATE_NOT_PERMITTED = Exception("У Вас нет прав на создание доски задач в данном рабочем пространстве.")
WORKSPACE_ROLE_MANAGE_NOT_PERMITTED = Exception("Вы не можете редактировать роли данного рабочего пространства.")

BOARD_NOT_FOUND = Exception("Запрашиваемая Вами доска задач не была найдена.")
BOARD_ALREADY_EXISTS = Exception("Доска задач с таким именем уже существует.")
BOARD_UPDATE_NOT_PERMITTED = Exception("У Вас нет прав на редактирование данных данной доски задач.")
BOARD_DELETE_NOT_PERMITTED = Exception("У Вас нет прав на удаление данной доски задач.")
