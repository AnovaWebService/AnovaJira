import {Col, Layout, Row, Tabs} from 'antd';
import dayjs from 'dayjs';

import {StyledHeader} from '../../global-styles';
import {TaskGroupType, TTask, TUser} from '../../types/types';
import {TaskGroup} from './components/task-group';
import { useCallback, useEffect, useMemo, useState } from 'react';

const testUser: TUser = {
  id: 1,
  username: 'Sunday',
  password: '1231232',
  first_name: 'Kirill',
  last_name: 'Groshelev',
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
    comments: [],
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
  const [tasks, setTasks] = useState<TTask[]>(testTasks);
  const sortedTasks = sortTasksByType(tasks);

  const handleTaskAdd = (task: TTask, groupType: TaskGroupType) => {
    const tasksFiltered = tasks.filter(
      (_task) => _task.id !== task.id && _task.slug != task.slug,
    );
    setTasks((prev) => [...tasksFiltered, {...task, type: groupType}]);
  };

  const handleTaskDelete = (task: TTask) => {
    const tasksFiltered = tasks.filter((_task) => _task.id !== task.id);
    setTasks([...tasksFiltered]);
  };

  useEffect(() => console.log(tasks), [tasks]);

  return (
    <Layout>
      <StyledHeader>srgferger</StyledHeader>
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
              onTaskMove={handleTaskAdd}
              onTaskDelete={handleTaskDelete}
            />
          ))}
        </div>
      </Layout.Content>
    </Layout>
  );
}
