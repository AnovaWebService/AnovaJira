import {PlusOutlined} from '@ant-design/icons';
import {Badge, Button, Empty} from 'antd';
import {useState} from 'react';
import {useDrop} from 'react-dnd';

import {TaskGroupType, TTask} from '../../../types/types';
import {
  colors,
  GroupTaskCreateButton,
  GroupTypeTag,
  GroupTypeTagContainer,
  TaskGroupContainer,
  typeNames,
} from './styles';
import {Task} from './task';

type TaskGroupProps = {
  readonly type: TaskGroupType;
  readonly tasks: TTask[];
  readonly onTaskDelete?: (task: TTask) => void;
  readonly onTaskMove?: (task: TTask, groupType: TaskGroupType) => void;
};

export function TaskGroup({type, tasks, onTaskMove}: TaskGroupProps) {
  const [{isDropping}, dropRef] = useDrop({
    accept: 'task',
    collect: (monitor) => ({
      isDropping: monitor.isOver() && monitor.canDrop(),
    }),
    drop(item: TTask) {
      onTaskMove?.(item, type);
    },
    canDrop: (item: any) => item.type !== type,
  });

  return (
    <TaskGroupContainer type={type} ref={dropRef} isTaskDropping={isDropping}>
      <GroupTypeTagContainer type={type}>
        <GroupTypeTag color={colors[type]} text={typeNames[type]} />
      </GroupTypeTagContainer>

      {tasks.map((task) => (
        <Task key={task.id} {...task} />
      ))}

      {!isDropping ? (
        <GroupTaskCreateButton icon={<PlusOutlined />} type="text">
          Добавить
        </GroupTaskCreateButton>
      ) : (
        <Empty description="Перетащить сюда" />
      )}
    </TaskGroupContainer>
  );
}
