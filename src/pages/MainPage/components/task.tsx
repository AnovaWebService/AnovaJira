import {CommentOutlined, SnippetsOutlined} from '@ant-design/icons';
import {Tooltip} from 'antd';
import {useDrag} from 'react-dnd';

import {TransparentTag} from '../../../global-styles';
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
  TTaskCard,
} from './styles';
import {UserTag} from './user-tag';

type TaskProps = {
  readonly title: string;
  readonly type: TTaskCard['type'];
  readonly assigners: any[];
  readonly slug: string;
  readonly tags?: any[];
  readonly comments?: any[];
  readonly onClick?: (slug: string) => void;
  readonly onDrag?: (slug: string) => void;
};

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
  title,
  type,
  assigners,
  slug,
  comments,
  onClick,
}: TaskProps) {
  const [{isDragStart}, dragRef] = useDrag({
    type: 'task',
    item: {slug},
    collect: (monitor) => ({
      isDragStart: monitor.isDragging(),
    }),
  });

  return (
    <TaskCard
      type={type}
      onClick={() => onClick?.(slug)}
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
              key={assigner}
              firstName="Kirill"
              lastName="Groshelev"
              username="Sunday"
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
        {!!comments && <CommentButton count={comments.length} />}
      </ToolbarContainer>
    </TaskCard>
  );
}
