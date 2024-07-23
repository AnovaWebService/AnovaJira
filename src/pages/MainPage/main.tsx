import {Layout} from 'antd';
import {useDrop} from 'react-dnd';

import {StyledHeader} from '../../global-styles';
import {TaskGroup} from './components/task-group';

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
          <TaskGroup type="in_development" />

          <TaskGroup type="error" />

          <TaskGroup type="testing" />

          <TaskGroup type="completed" />

          <TaskGroup type="ready_to_development" />

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
