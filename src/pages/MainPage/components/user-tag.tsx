import {Avatar, Space, Tooltip} from 'antd';
import { UserTagContainer, UserTagName } from './styles';

type UserTagProps = {
  readonly firstName: string;
  readonly lastName: string;
  readonly avatar?: string;
  readonly username: string;
  readonly unfocusable?: boolean;
  readonly onClick?: (username: string) => void;
};

export function UserTag({
  firstName,
  lastName,
  username,
  unfocusable,
  onClick,
}: UserTagProps) {
  return (
    <UserTagContainer
      size="small"
      unfocusable={unfocusable}
      onClick={() => onClick(username)}
    >
      <Avatar src={"https://variety.com/wp-content/uploads/2021/04/Avatar.jpg?w=800"} size={20}>
        {username.at(0)}
      </Avatar>
      <UserTagName>
        {firstName} {lastName}
      </UserTagName>
    </UserTagContainer>
  );
}
