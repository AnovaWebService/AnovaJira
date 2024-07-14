import {Badge, Button, Card, Space} from 'antd';
import {css, styled} from 'styled-components';

export const colors = {
  in_development: '#D68FD6',
  ready_to_development: '#E28413',
  testing: '#E0B700',
  error: '#FF7070',
  completed: '#4DD179',
};

export const typeNames = {
  in_development: 'В разработке',
  ready_to_development: 'Готово к разработке',
  testing: 'Тестирование',
  error: 'Ошибка',
  completed: 'Завершено',
};

const hoverEffectMask = css`
  background-color: transparent;

  &:hover {
    background-color: rgba(0, 0, 0, 0.07);
  }
`;

const fontFamily = css`
  font-family:
    ui-sans-serif,
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI Variable Display',
    'Segoe UI',
    Helvetica,
    'Apple Color Emoji',
    Arial,
    sans-serif,
    'Segoe UI Emoji',
    'Segoe UI Symbol';
`;

export type TaskGroupType =
  | 'in_development'
  | 'ready_to_development'
  | 'testing'
  | 'completed'
  | 'error';

export type TTaskCard = {
  type: TaskGroupType;
  disabled?: boolean;
  isDragging?: boolean;
};

export type TTaskGroup = {
  type: TaskGroupType;
};

export const TaskCard = styled.div<TTaskCard>`
  padding: 0;
  display: flex;
  flex-direction: column;
  border-radius: 0.5rem;
  transition: filter 300ms;
  background-color: ${(props) => colors[props.type]};
  min-height: 10rem;
  max-width: 20rem;
  transition: opacity 300ms;
  opacity: ${(props) => (!!props.isDragging ? '0.5' : '1')};

  &:hover {
    filter: brightness(93%);
  }
`;

export const TaskCardContentWrapper = styled.div`
  padding: 0.6rem 0.6rem 0 0.6rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

export const TaskTitle = styled.p`
  font-size: 0.9rem;
  text-overflow: ellipsis;
  word-wrap: break-word;
  margin: 0;
  ${fontFamily};
`;

export const TaskTitleWrapper = styled(Space)`
  align-items: baseline;
  font-size: 1rem;
`;

export const TaskCode = styled.p`
  color: inherit;
  font-size: 0.8rem;
  margin: 0;
  ${fontFamily};
`;

export const UserTagContainer = styled(Space)`
  border-radius: 0.5rem;
  padding: 0.3rem;

  ${hoverEffectMask}
`;

export const UserTagName = styled.p`
  font-size: 0.8rem;
  padding: 0;
  margin: 0;
  ${fontFamily};
`;

export const ToolbarContainer = styled.div`
  display: flex;
  flex-direction: row;
  margin: 1rem 0.4rem 0.4rem 0.4rem;
  gap: 1rem;
`;

export const TaskTagsContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

export const CommentButtonSmallWrapper = styled.div`
  display: flex;
  flex-direction: row;
  padding: 0.2rem;
  border-radius: 10%;
  font-size: 1.02rem;
  gap: 0.2rem;
  color: inherit;

  ${hoverEffectMask};
  ${fontFamily};

  code {
    font-size: 0.9rem;
  }
`;

export const Hoverable = styled.div`
  width: auto;
  ${hoverEffectMask};
`;

export const TaskGroupContainer = styled.div<TTaskGroup>`
  display: flex;
  flex-direction: column;
  background-color: ${(props) =>
    `color-mix(in srgb, ${colors[props.type]} 60%, black 30%)`};
  border-radius: 0.5rem;
  padding: 0.5rem 0.3rem 0.5rem 0.3rem;
  gap: 0.5rem;
  color: white;
`;

export const GroupTypeTag = styled(Badge)`
  background-color: rgba(255, 255, 255, 0.605);
  padding: 0.2rem 0.5rem 0.2rem 0.5rem;
  border-radius: 1rem;
  color: white;

  span {
    color: white;
  }
`;

export const GroupTypeTagContainer = styled.div<{type: TaskGroupType}>`
  ${hoverEffectMask};
  filter: brightness(95%);
  border-radius: 1rem;
  padding: 0.5rem;
  align-items: center;
`;

export const GroupTaskCreateButton = styled(Button)`
  text-align: start;
  justify-content: start;
`;
