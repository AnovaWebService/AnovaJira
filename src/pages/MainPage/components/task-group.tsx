import {PlusOutlined} from '@ant-design/icons';
import {Badge, Button} from 'antd';

import {
  colors,
  GroupTaskCreateButton,
  GroupTypeTag,
  GroupTypeTagContainer,
  TaskGroupContainer,
  TaskGroupType,
  typeNames,
} from './styles';
import {Task} from './task';

type TaskGroupProps = {
  readonly type: TaskGroupType;
};

export function TaskGroup({type}: TaskGroupProps) {
  return (
    <TaskGroupContainer type={type}>
      <GroupTypeTagContainer type={type}>
        <GroupTypeTag color={colors[type]} text={typeNames[type]} />
      </GroupTypeTagContainer>

      <Task
        type={type}
        title="Сделать авторизацию и регистрацию на стороне бэкенда."
        slug="TASK-5"
        assigners={['Kirill Groshelev']}
      />

      <Task
        type={type}
        title="Реализовать аутентификацию на фронтенде."
        slug="TASK-6"
        assigners={['Kirill Groshelev']}
      />

      <Task
        type={type}
        title="Ошибка: какого хуя меня нет в списке бэкендеров."
        slug="TASK-7"
        assigners={['Kirill Groshelev']}
        comments={['frfr']}
      />

      <GroupTaskCreateButton icon={<PlusOutlined />} type="text">
        Добавить
      </GroupTaskCreateButton>
    </TaskGroupContainer>
  );
}
