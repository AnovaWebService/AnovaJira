import {Card, Space} from 'antd';
import {css, styled} from 'styled-components';

const colors = {
  in_development: '#D2E3FC',
  ready_to_development: '#FEEFC3',
  testing: '#CEEAD6',
  error: '#FAD2CF',
  completed: '#34A853',
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

export type TTaskCard = {
  type:
    | 'in_development'
    | 'ready_to_development'
    | 'testing'
    | 'completed'
    | 'error';
  disabled?: boolean;
  isDragging?: boolean;
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
  color: grey;
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
  color: grey;

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
