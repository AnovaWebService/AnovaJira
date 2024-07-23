import {SendOutlined} from '@ant-design/icons';
import {Avatar, Button, Flex, Input, Space, Typography} from 'antd';
import {useState} from 'react';

import {TComment, TUser} from '../../../types/types';
import {CommentListComponent} from './styles';

type CommentListProps = {
  readonly comments: TComment[];
  readonly user?: TUser;
  readonly allowWrite?: boolean;
  readonly onCommentRemove?: (comment: TComment) => void;
  readonly onCommentAdd?: (commentText: string) => void;
};

export function CommentList({
  comments,
  user,
  allowWrite,
  onCommentRemove,
  onCommentAdd,
}: CommentListProps) {
  const [loading, setLoading] = useState<boolean>(false);
  const [commentText, setCommentText] = useState<string>('');

  const handleCommentSubmit = () => {
    if (!commentText) {
      return;
    }

    if (commentText.length <= 3) {
      return;
    }

    setLoading(true);

    setTimeout(() => {
      onCommentAdd?.(commentText);
      setCommentText('');
      setLoading(false);
    }, 2000);
  };

  const handleCommentInputChange = ({target}) => {
    setCommentText(target?.value);
  };

  return (
    <Space size="large" direction="vertical">
      {comments.length > 0 && (
        <CommentListComponent
          current={comments?.length}
          status="wait"
          direction="vertical"
          items={comments.map((comment) => ({
            disabled: false,
            description: <Typography.Text>{comment.text}</Typography.Text>,
            icon: (
              <Avatar src={comment.creator.avatar}>
                {comment.creator.first_name.at(0)}
              </Avatar>
            ),
            title: (
              <Space size={7} align="center">
                <Typography.Text>{comment.creator.first_name}</Typography.Text>

                <Typography.Text type="secondary">
                  {comment.date_created.locale('ru').fromNow()}
                </Typography.Text>

                {!!comment.date_modified && (
                  <Typography.Text type="secondary">(изменено)</Typography.Text>
                )}
              </Space>
            ),
          }))}
        />
      )}

      {!!user && !!allowWrite && (
        <Flex gap={0} align="end">
          <Avatar src={user?.avatar!}>{user.first_name.at(0)}</Avatar>
          <Input.TextArea
            value={commentText}
            style={{
              width: '80%',
            }}
            variant="borderless"
            placeholder="Ваш комментарий..."
            autoSize
            onChange={handleCommentInputChange}
          />
          {!!commentText && (
            <Button
              type="text"
              icon={<SendOutlined />}
              disabled={commentText.length <= 3}
              loading={loading}
              onClick={handleCommentSubmit}
            />
          )}
        </Flex>
      )}
    </Space>
  );
}
