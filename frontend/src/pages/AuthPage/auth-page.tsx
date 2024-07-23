import {
  AdditionalInfo,
  Body,
  Card,
  CardTextH2Black,
  CardTextH2White,
  CardTextPWhite,
  CheckBox,
  CheckboxContent,
  CheckboxLink,
  CheckboxText,
  CheckboxTextP,
  Container,
  InputEnter1,
  InputEnter2,
  InputForm,
  Inputs,
  LeftCard,
  LeftCardText,
  LinkContent,
  Logo,
  LogoText,
  RegistrBtn,
  RightCard,
  RightCardContainer,
  StyledHeader,
} from './components/styles';

export function AuthPage() {
  return (
    <Container>
      <StyledHeader>
        <Logo />
        <LogoText>AnovaTask</LogoText>
      </StyledHeader>
      <Body>
        <Card>
          <LeftCard>
            <LeftCardText>
              <CardTextH2White>Регистрация</CardTextH2White>
              <CardTextPWhite>
                Если у вас ещё нет аккаунта или вы хотите зарегистрировать свою
                компания, нажмите на кнопку ниже
              </CardTextPWhite>
            </LeftCardText>
            <RegistrBtn>Регистрация</RegistrBtn>
          </LeftCard>
          <RightCard>
            <RightCardContainer>
              <InputForm>
                <CardTextH2Black>Войти</CardTextH2Black>
                <Inputs>
                  <InputEnter1 />
                  <InputEnter2 />
                </Inputs>
              </InputForm>
              <AdditionalInfo>
                <CheckboxContent>
                  <CheckBox type="checkbox" />
                  <CheckboxText>
                    <CheckboxTextP>Я ознакомлен с</CheckboxTextP>
                    <CheckboxLink href="#">Политикой компании</CheckboxLink>
                  </CheckboxText>
                </CheckboxContent>
                <LinkContent href="#">Забыли пароль?</LinkContent>
              </AdditionalInfo>
            </RightCardContainer>
          </RightCard>
        </Card>
      </Body>
    </Container>
  );
}
