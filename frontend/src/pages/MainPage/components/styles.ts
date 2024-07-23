import {Badge, Button, Input, Select, Space, Steps} from 'antd';
import {CSSProperties} from 'react';
import {styled} from 'styled-components';

import {
  colorTransition,
  fontFamily,
  hoverEffectMask,
} from '../../../global-styles';
import {TaskGroupType} from '../../../types/types';

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

export type TTaskCard = {
  type: TaskGroupType;
  disabled?: boolean;
  isDragging?: boolean;
};

export type TTaskGroup = {
  type: TaskGroupType;
  isTaskDropping?: boolean;
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
  touch-action: none;

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

export const UserTagContainer = styled(Space)<{unfocusable?: boolean}>`
  border-radius: 0.5rem;
  padding: 0.3rem;

  ${(props) => !props.unfocusable && hoverEffectMask}
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

export const TaskGroupContainer = styled.div<TTaskGroup>`
  scale: 1;
  display: flex;
  flex-direction: column;
  background-color: ${(props) =>
    `color-mix(in srgb, ${colors[props.type]} 60%, black 30%)`};
  border-radius: 0.5rem;
  padding: 0.5rem 0.3rem 0.5rem 0.3rem;
  gap: 0.5rem;
  color: white;
  height: auto;
  min-width: 20rem;
  transition: scale 300ms;
  ${(props) => !!props.isTaskDropping && 'scale: 1.05;'};
`;

export const GroupTypeTag = styled(Badge)`
  background-color: ${(props) => props.theme.taskTypeTagBg};
  padding: 0.2rem 0.5rem 0.2rem 0.5rem;
  border-radius: 1rem;
  color: white;

  span {
    color: white;
  }

  ${colorTransition}
`;

export const GroupTypeTagContainer = styled.div<{type: TaskGroupType}>`
  ${hoverEffectMask};
  filter: brightness(95%);
  border-radius: 1rem;
  padding: 0.2rem;
  align-items: center;
`;

export const GroupTaskCreateButton = styled(Button)`
  text-align: start;
  justify-content: start;
`;

export const DrawerTaskTitle = styled(Input.TextArea)<{error?: boolean}>`
  border: none;
  background: transparent;
  background-color: transparent;
  box-shadow: none;
  box-sizing: none;
  font-size: 1.7rem;
  font-weight: bold;
  transition: color 300ms;
  color: ${(props) => (!!props.error ? 'red' : 'inherit')};

  &::placeholder {
    transition: color 300ms;
    ${(props) => !!props.error && 'color: #F97681;'};
  }

  &:focus-within {
    box-shadow: none;
    border-color: transparent;
  }
`;

export const DrawerTaskDescription = styled(Input.TextArea)`
  border: none;
  background: transparent;
  background-color: transparent;
  box-shadow: none;
  box-sizing: none;
  font-size: 1.1rem;

  &:focus-within {
    box-shadow: none;
    border-color: transparent;
  }
`;

export const DrawerTypeSelect = styled(Select)`
  &,
  .ant-select-selector {
    padding: 0 !important;
    border: none !important;
    border-color: transparent !important;
    background-color: transparent !important;
    box-shadow: none !important;
    box-sizing: none !important;
  }

  .ant-select-arrow {
    display: none;
  }

  option {
    width: 100%;
  }
`;

export const DrawerDescriptionsItemContainer = styled.div`
  padding: 0.2rem;
`;

export const CommentListComponent = styled(Steps)`
  margin-inline-end: 0;

  .ant-steps-item,
  .ant-steps-item-icon {
    margin-inline-end: 0.5rem !important;
  }

  .ant-steps-item-tail::after {
    background-color: rgba(5, 5, 5, 0.3) !important;
  }
`;

export const AssignersSelect = styled(Select)`
  .ant-select-selector {
    padding-inline: 0 !important;
    padding-block: 0 !important;
    width: 10rem !important;
  }
`;

export const AssignersSelectGroup = styled(Select.OptGroup)`
  .ant-select-dropdown.ant-select-item-option-grouped {
    padding-inline-start: 0.5rem !important;
  }
`;
