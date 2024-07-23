import dayjs from 'dayjs';

export type TaskGroupType =
  | 'in_development'
  | 'ready_to_development'
  | 'testing'
  | 'completed'
  | 'error';

export interface TUser {
  id: number;
  username: string;
  password: string;
  first_name: string;
  last_name?: string;
  avatar?: string;
  role?: 'admin' | 'user' | 'moderator';
  date_joined: dayjs.Dayjs;
}

export interface TBoard {
  id: number;
  title: string;
  participants: TUser[];
}

export interface TComment {
  id: number;
  creator: TUser;
  task: TTask;
  text: string;
  date_created: dayjs.Dayjs;
  date_modified?: dayjs.Dayjs;
}

export interface TTask {
  id: number;
  slug: string;
  assigners: TUser[];
  title: string;
  type: TaskGroupType;
  creator: TUser;
  description?: string;
  comments: TComment[];
}
