import {Button, Divider, Layout, Tabs, Tag} from 'antd';
import {CSSProperties} from 'react';
import {createGlobalStyle, css, styled} from 'styled-components';

import PoppinsBlack from './fonts/Poppins/Poppins-Regular.ttf';

type StyledThemeType = {
  taskTypeTagBg: CSSProperties['color'];
  taskTypeTagFg: CSSProperties['color'];
};

export const styledLightTheme: StyledThemeType = {
  taskTypeTagBg: 'rgba(255, 255, 255, 0.605)',
  taskTypeTagFg: 'black',
};

export const styledDarkTheme: StyledThemeType = {
  taskTypeTagBg: 'rgba(71, 73, 84, 0.605)',
  taskTypeTagFg: 'white',
};

export const hoverEffectMask = css`
  background-color: transparent;

  &:hover {
    background-color: rgba(0, 0, 0, 0.07);
  }
`;

export const fontFamily = css`
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

export const PoppinsFont = createGlobalStyle`
  @font-face {
    font-family: 'poppins';
    src: url(${PoppinsBlack}) format('truetype');
    font-weight: 300;
    font-style: normal;
    font-display: auto;
  }

  .ant-select-dropdown .ant-select-item-option-grouped {
    padding-inline-start: 0.5rem !important;
  }
`;

export const SubmitButton = styled(Button)`
  background-color: yellow;
`;

export const RemoveButton = styled(Button)`
  background-color: red;
`;

export const ActionButton = styled(Button)`
  background-color: grey;
`;

export const StyledHeader = styled(Layout.Header)`
  background-color: transparent;
`;

export const TransparentTag = styled(Tag)`
  background: transparent;
`;

export const Hoverable = styled.div`
  width: auto;
  padding: 0.2rem;
  border-radius: 0.5rem;
  ${hoverEffectMask};
`;

export const NoMarginDivider = styled(Divider)`
  margin: 0;
`;

export const colorTransition = css`
  transition:
    color 300ms,
    background-color 300ms;
`;

export const PaddingContainer = styled.div<{
  top?: CSSProperties['paddingTop'];
  bottom?: CSSProperties['paddingBottom'];
  left?: CSSProperties['paddingLeft'];
  right?: CSSProperties['paddingRight'];
}>`
  ${(props) => !!props.top && `padding-top: ${props.top}`}
  ${(props) => !!props.bottom && `padding-bottom: ${props.bottom}`}
  ${(props) => !!props.left && `padding-left: ${props.left}`}
  ${(props) => !!props.right && `padding-right: ${props.right}`}
`;

export const TextColorContainer = styled.div<{color: CSSProperties['color']}>`
  color: ${(props) => props.color} !important;
`;
