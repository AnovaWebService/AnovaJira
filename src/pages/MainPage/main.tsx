import {Layout, Switch, Tabs} from 'antd';
import dayjs from 'dayjs';
import {useMemo, useState} from 'react';

import {StyledHeader} from '../../global-styles';
import {TaskGroupType, TTask, TUser} from '../../types/types';
import {TaskDrawer} from './components/task-drawer';
import {TaskGroup} from './components/task-group';
import { useThemeContext } from '../../hooks/use-theme-context';

const testUser: TUser = {
  id: 1,
  username: 'Sunday',
  password: '1231232',
  first_name: 'Kirill',
  last_name: 'Groshelev',
  avatar: 'https://variety.com/wp-content/uploads/2021/04/Avatar.jpg?w=800',
  date_joined: dayjs(),
};

const testTasks: TTask[] = [
  {
    id: 1,
    type: 'completed',
    title: 'Настроить CI/CD для проекта.',
    slug: 'TASK-1',
    assigners: [testUser],
    creator: testUser,
    comments: [],
  },
  {
    id: 2,
    type: 'in_development',
    title: 'Оптимизировать запросы к базе данных.',
    slug: 'TASK-2',
    assigners: [testUser],
    creator: testUser,
    comments: [],
  },
  {
    id: 3,
    type: 'ready_to_development',
    title: 'Реализовать страницу профиля пользователя.',
    slug: 'TASK-3',
    assigners: [testUser],
    creator: testUser,
    comments: [],
  },
  {
    id: 4,
    type: 'error',
    title: 'Исправить баг в модуле аутентификации.',
    slug: 'TASK-4',
    assigners: [testUser],
    creator: testUser,
    comments: [],
  },
  {
    id: 5,
    type: 'testing',
    title: 'Сделать авторизацию и регистрацию на стороне бэкенда.',
    slug: 'TASK-5',
    assigners: [testUser],
    creator: testUser,
    comments: [],
  },
  {
    id: 6,
    type: 'in_development',
    title: 'Написать unit-тесты для нового функционала.',
    slug: 'TASK-6',
    assigners: [testUser],
    creator: testUser,
    comments: [],
  },
  {
    id: 7,
    type: 'completed',
    title: 'Обновить документацию по API.',
    slug: 'TASK-7',
    assigners: [testUser],
    creator: testUser,
    comments: [],
  },
  {
    id: 8,
    type: 'error',
    title: 'Реализовать кэширование для уменьшения нагрузки на сервер.',
    slug: 'TASK-8',
    assigners: [testUser],
    creator: testUser,
    comments: [],
  },
  {
    id: 9,
    type: 'testing',
    title: 'Настроить логирование ошибок.',
    slug: 'TASK-9',
    assigners: [testUser],
    creator: testUser,
    comments: [],
  },
  {
    id: 10,
    type: 'ready_to_development',
    title: 'Провести рефакторинг кода фронтенда.',
    slug: 'TASK-10',
    assigners: [testUser],
    creator: testUser,
    comments: [
      {
        id: 1,
        text: 'Текст очооооочень длинного комментария для просмотра каким будет уроливым данный компонент. Ну короче надо прям что-то длинное воткнуть. https://git.chilli-web.tech/',
        creator: testUser,
        task: null,
        date_created: dayjs(),
      },
      {
        id: 2,
        text: 'Тестовый комментарий 2',
        creator: testUser,
        task: null,
        date_created: dayjs(),
      },
    ],
  },
];

function sortTasksByType(tasks) {
  const sortedTasks = {
    ready_to_development: tasks.filter(
      (task) => task.type === 'ready_to_development',
    ),
    in_development: tasks.filter((task) => task.type === 'in_development'),
    error: tasks.filter((task) => task.type === 'error'),
    completed: tasks.filter((task) => task.type === 'completed'),
    testing: tasks.filter((task) => task.type === 'testing'),
  };

  return sortedTasks;
}

export function MainPage() {
  const [drawerOpened, setDrawerOpened] = useState(false);
  const [taskToEdit, setTaskToEdit] = useState(null);
  const [tasks, setTasks] = useState<TTask[]>(testTasks);

  const sortedTasks = useMemo(() => sortTasksByType(tasks), [tasks]);
  const setTheme = useThemeContext();

  const handleTaskAdd = (task: TTask, groupType: TaskGroupType) => {
    const tasksFiltered = tasks.filter(
      (_task) => _task.id !== task.id && _task.slug != task.slug,
    );
    setTasks([...tasksFiltered, {...task, type: groupType}]);
  };

  const handleTaskDelete = (task: TTask) => {
    const tasksFiltered = tasks.filter((_task) => _task.id !== task.id);
    setTasks([...tasksFiltered]);
  };

  const handleTaskCreateMode = () => {
    setTaskToEdit(null);
    setDrawerOpened(true);
  };

  const handleTaskEditMode = (task: TTask) => {
    setTaskToEdit(task);
    setDrawerOpened(true);
  };

  const handleThemeSwitch = (checked: boolean) => {
    setTheme(!!checked ? 'dark' : 'light');
  };

  return (
    <Layout>
      <StyledHeader>
        <Switch onChange={handleThemeSwitch} />
      </StyledHeader>
      <Layout.Content>
        <Tabs size="middle">
          <Tabs.TabPane tab="Фамилия" key={0} />
          <Tabs.TabPane tab="Имя" key={1} />
        </Tabs>
        <div
          style={{
            display: 'flex',
            flexDirection: 'row',
            gap: '1rem',
            alignItems: 'baseline',
          }}
        >
          {Object.entries<TTask[]>(sortedTasks).map(([type, tasks]) => (
            <TaskGroup
              key={type}
              type={type as any}
              tasks={tasks}
              onTaskClick={(task) => handleTaskEditMode(task)}
              onTaskMove={handleTaskAdd}
              onTaskDelete={handleTaskDelete}
              onTaskCreate={handleTaskCreateMode}
            />
          ))}
        </div>
      </Layout.Content>
      <TaskDrawer
        task={taskToEdit}
        open={drawerOpened}
        onClose={() => setDrawerOpened(false)}
      />
    </Layout>
  );
}
