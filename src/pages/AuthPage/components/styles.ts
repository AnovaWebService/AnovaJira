import {styled} from 'styled-components';

import logo from '../../../assets/logo.png';

export const Container = styled.div`
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  height: 100vh;
`;

export const StyledHeader = styled.header`
  position: absolute;
  top: 0;
  left: 0;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  height: 50px;
  padding: 20px 0 0 20px;
  background-color: #fff;
`;

export const Logo = styled.div`
  display: flex;
  width: 50px;
  height: 50px;
  background-image: url(${logo});
`;

export const LogoText = styled.h1`
  display: flex;
  align-items: center;
  padding: 0 25px;
  margin: 0;
  font-family: 'Open Sans';
  font-style: normal;
  font-weight: 600;
  font-size: 32px;
  line-height: 44px;
  text-align: center;
  letter-spacing: 0.05em;
  cursor: default;
`;

export const Body = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
`;

export const Card = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  width: 800px;
  height: 550px;
  background-color: #fff;
  border-radius: 15px;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.34);
`;

export const LeftCard = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 400px;
  height: 100%;
  padding: 0 25px 0 25px;
  gap: 29px;
  background-color: #a717ff;
  border-top-left-radius: 15px;
  border-bottom-left-radius: 15px;
`;

export const LeftCardText = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 17px;
`;

export const RightCard = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 400px;
  height: 100%;
  padding: 0 25px;
  background-color: #fff;
  border-top-right-radius: 15px;
  border-bottom-right-radius: 15px;
`;

export const RightCardContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 18px;
`;

export const InputForm = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 45px;
`;

export const Inputs = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 35px;
`;

export const InputEnter1 = styled.input`
  width: 320px;
  height: 50px;
  padding: 0 15px;
  background-color: #d9d9d9;
  border: none;
  border-radius: 10px;
  cursor: pointer;
`;

export const InputEnter2 = styled.input`
  width: 320px;
  height: 50px;
  padding: 0 15px;
  background-color: #d9d9d9;
  border: none;
  border-radius: 10px;
  cursor: pointer;
`;

export const AdditionalInfo = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  gap: 11px;
`;

export const CheckboxContent = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  width: 100%;
  gap: 7px;
`;

export const CheckBox = styled.input`
  display: flex;
  justify-content: center;
  align-items: center;
  width: 26px;
  height: 26px;
  margin: 0;
  /* NOT-WORK */
  background-color: #d9d9d9;
  /* NOT-WORK */
  border: 0.6 solid #bfb7b7;
  border-radius: 5px;
  cursor: pointer;
`;

export const CheckboxText = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: 5px;
`;

export const CheckboxTextP = styled.p`
  display: flex;
  margin: 0;
  align-items: center;
  font-family: 'Open Sans';
  font-style: normal;
  font-weight: 400;
  font-size: 15px;
  line-height: 20px;
  text-align: center;
  cursor: default;
`;

export const CheckboxLink = styled.a`
  display: flex;
  align-items: center;
  font-family: 'Open Sans';
  font-style: normal;
  font-weight: 400;
  font-size: 15px;
  line-height: 20px;
  color: #a717ff;
`;

export const LinkContent = styled.a`
  display: flex;
  justify-content: flex-start;
  align-items: center;
  width: 100%;
  font-family: 'Open Sans';
  font-style: normal;
  font-weight: 400;
  font-size: 15px;
  line-height: 20px;
  text-align: left;
  color: #a717ff;
`;

export const RegistrBtn = styled.button`
  display: flex;
  justify-content: center;
  align-items: center;
  width: 176px;
  height: 41px;
  margin: 0;
  font-family: 'Open Sans';
  font-style: normal;
  font-weight: 700;
  font-size: 20px;
  line-height: 27px;
  text-align: center;
  color: #fff;
  background-color: #a717ff;
  border: 2px solid #fff;
  border-radius: 20px;
  cursor: pointer;
`;

export const CardTextH2Black = styled.h2`
  display: flex;
  margin: 0;
  font-family: 'Open Sans';
  font-style: normal;
  font-weight: 700;
  font-size: 40px;
  line-height: 54px;
  align-items: center;
  text-align: center;
  color: #000;
  cursor: default;
`;

export const CardTextH2White = styled.h2`
  display: flex;
  margin: 0;
  font-family: 'Open Sans';
  font-style: normal;
  font-weight: 700;
  font-size: 40px;
  line-height: 54px;
  align-items: center;
  text-align: center;
  color: #fff;
  cursor: default;
`;

export const CardTextPWhite = styled.p`
  display: flex;
  margin: 0;
  font-family: 'Open Sans';
  font-style: normal;
  font-weight: 400;
  font-size: 15px;
  line-height: 20px;
  align-items: center;
  text-align: center;
  color: #fff;
  cursor: default;
`;
