import {CommentOutlined, SnippetsOutlined} from '@ant-design/icons';
import {Tooltip} from 'antd';
import {useDrag} from 'react-dnd';

import {TransparentTag} from '../../../global-styles';
import {TTask} from '../../../types/types';
import {
  CommentButtonSmallWrapper,
  Hoverable,
  TaskCard,
  TaskCardContentWrapper,
  TaskCode,
  TaskTagsContainer,
  TaskTitle,
  TaskTitleWrapper,
  ToolbarContainer,
} from './styles';
import {UserTag} from './user-tag';

interface TaskProps extends TTask {
  readonly onClick?: (task: TTask) => void;
  readonly onDragComplete?: (task: TTask) => void;
}

function CommentButton({count}) {
  return (
    <Tooltip title="Комментарии" placement="left">
      <CommentButtonSmallWrapper>
        <CommentOutlined />
        <code>{count}</code>
      </CommentButtonSmallWrapper>
    </Tooltip>
  );
}

export function Task({
  id,
  title,
  type,
  assigners,
  slug,
  comments,
  creator,
  onClick,
}: TaskProps) {
  const [{isDragStart}, dragRef] = useDrag({
    type: 'task',
    item: () => ({id, title, type, assigners, slug, comments, creator}),
    collect: (monitor) => ({
      isDragStart: monitor.isDragging(),
    }),
  });

  return (
    <TaskCard
      type={type}
      onClick={() =>
        onClick?.({title, type, assigners, slug, comments, id, creator})
      }
      ref={dragRef}
      isDragging={isDragStart}
    >
      <TaskCardContentWrapper>
        <TaskTitleWrapper size={5}>
          <SnippetsOutlined />
          <TaskTitle>{title}</TaskTitle>
        </TaskTitleWrapper>

        <Tooltip title="ID задачи" placement="left">
          <TaskCode>{slug}</TaskCode>
        </Tooltip>

        <Tooltip title="Исполнитель" placement="left">
          {assigners.map((assigner) => (
            <UserTag
              key={assigner.id}
              firstName={assigner.first_name}
              lastName={assigner.last_name}
              username={assigner.username}
            />
          ))}
        </Tooltip>

        <TaskTagsContainer>
          <Hoverable>
            <TransparentTag color="#f50">Ошибка</TransparentTag>
          </Hoverable>

          <Hoverable>
            <TransparentTag color="#0088ff">Проект</TransparentTag>
          </Hoverable>
        </TaskTagsContainer>
      </TaskCardContentWrapper>

      <ToolbarContainer>
        {!!comments && comments.length > 0 && (
          <CommentButton count={comments.length} />
        )}
      </ToolbarContainer>
    </TaskCard>
  );
}
