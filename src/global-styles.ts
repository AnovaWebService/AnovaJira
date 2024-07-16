import {Button, Layout, Tabs, Tag} from 'antd';
import {createGlobalStyle, styled} from 'styled-components';

import PoppinsBlack from './fonts/Poppins/Poppins-Regular.ttf';

export const PoppinsFont = createGlobalStyle`
  @font-face {
    font-family: 'poppins';
    src: url(${PoppinsBlack}) format('truetype');
    font-weight: 300;
    font-style: normal;
    font-display: auto;
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
