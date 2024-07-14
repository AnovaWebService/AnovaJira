import {Layout} from 'antd';
import {StyledHeader} from '../../global-styles';
import {Task} from './components/task';
import { useDrag, useDrop } from 'react-dnd';

export function MainPage() {
  const [{isDropping}, dragRef] = useDrop({
    accept: 'task',
    drop(data) {
      console.log(data);
    },
    collect: (monitor) => ({
      isDropping: monitor.isOver(),
    }),
  });

  return (
    <Layout>
      <StyledHeader>srgferger</StyledHeader>
      <Layout.Content>
        <div style={{display: 'flex', flexDirection: 'row', gap: '1rem'}}>
          <Task
            type="ready_to_development"
            title="Сделать авторизацию и регистрацию на стороне бэкенда."
            slug="TASK-5"
            assigners={['Kirill Groshelev']}
          />

          <Task
            type="testing"
            title="Реализовать аутентификацию на фронтенде."
            slug="TASK-6"
            assigners={['Kirill Groshelev']}
          />

          <Task
            type="error"
            title="Ошибка: какого хуя меня нет в списке бэкендеров."
            slug="TASK-7"
            assigners={['Kirill Groshelev']}
            comments={['frfr']}
          />

          <Task
            type="in_development"
            title="Сделать эти ебаные карточки нормально, а то хуйня получается пока что."
            slug="TASK-8"
            assigners={['Kirill Groshelev']}
          />

          <div
            style={{
              background: isDropping ? 'green' : 'yellow',
              width: '200px',
              height: '200px',
            }}
            ref={dragRef}
          />
        </div>
      </Layout.Content>
    </Layout>
  );
}
