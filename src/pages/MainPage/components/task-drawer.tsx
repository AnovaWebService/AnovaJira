import {
  BranchesOutlined,
  BulbOutlined,
  CommentOutlined,
  DownOutlined,
  EllipsisOutlined,
  HistoryOutlined,
  InfoCircleOutlined,
  ScheduleOutlined,
  SnippetsOutlined,
  StarOutlined,
  TeamOutlined,
  UpOutlined,
  UserOutlined,
} from '@ant-design/icons';
import {useForm} from '@tanstack/react-form';
import {zodValidator} from '@tanstack/zod-form-adapter';
import {
  Avatar,
  Col,
  DatePicker,
  Divider,
  Drawer,
  Empty,
  Flex,
  Row,
  Select,
  Space,
  Tooltip,
  Typography,
} from 'antd';
import dayjs from 'dayjs';
import {ReactNode, useEffect, useState} from 'react';
import {z} from 'zod';

import {EditableTag} from '../../../components/editable-tag';
import {Hoverable, NoMarginDivider, PaddingContainer, TextColorContainer} from '../../../global-styles';
import {TTask} from '../../../types/types';
import {dayjsSchema} from '../../../types/zod-types';
import {
  AssignersSelect,
  AssignersSelectGroup,
  colors,
  DrawerDescriptionsItemContainer,
  DrawerTaskDescription,
  DrawerTaskTitle,
  DrawerTypeSelect,
  GroupTypeTag,
  GroupTypeTagContainer,
  typeNames,
} from './styles';
import {UserTag} from './user-tag';
import { CommentList } from './comment-list';

type TaskDrawerProps = {
  readonly task?: TTask;
  readonly open?: boolean;
  readonly onUpdate?: (task: Partial<TTask>) => void;
  readonly onCreate?: (task: TTask) => void;
  readonly onClose?: (changed: boolean) => void;
};

interface TTaskForm
  extends Omit<TTask, 'id' | 'slug' | 'comments' | 'type' | 'assigners'> {
  id?: number;
  taskType: string;
  deadline: dayjs.Dayjs;
  assigners: number[];
}

interface DesctiptionElement {
  name?: string;
  label: ReactNode;
  icon: ReactNode;
  contentSpan?: number;
  align?: string;
  validators?: {onBlur?: z.Schema; onChange?: z.Schema};
  children: ({state, handleChange, handleBlur}: any) => ReactNode;
}

const initialValues = {
  id: null,
  type: 'ready_to_development',
  title: '',
  description: '',
  assigners: null,
  deadline: null,
};

function IconText({icon, children, onClick = null}) {
  return (
    <Space size="small" onClick={() => onClick?.()}>
      {icon}
      {children}
    </Space>
  );
}

const DESCRIPTIONS_COLLAPSED_LENGTH = 4;

export function TaskDrawer({
  task,
  open,
  onUpdate,
  onCreate,
  onClose,
}: TaskDrawerProps) {
  const [showAdditionalOptions, setShowAdditionalOptions] =
    useState<boolean>(false);

  const form = useForm({
    defaultValues: initialValues,
    validators: !!task && {
      onBlur({}) {
        form.handleSubmit();
      },
    },
    onSubmit({value}) {
      if (!!task) {
        return onUpdate?.(value as any);
      }

      onCreate?.(value as any);
    },
    validatorAdapter: zodValidator() as any,
  });

  const updateFormValues = (values: Partial<TTaskForm>) => {
    form.store.setState((prev) => ({
      ...prev,
      values: {
        ...prev.values,
        ...values,
      },
    }));
  };

  useEffect(() => {
    form.reset();
    setShowAdditionalOptions(false);

    updateFormValues({
      ...task,
      taskType: task?.type,
      assigners: [],
      creator: null,
    });
  }, [task]);

  const descriptionsElements: DesctiptionElement[] = [
    {
      name: 'type',
      label: 'Статус',
      icon: <InfoCircleOutlined />,
      contentSpan: 10,
      validators: {
        onBlur: z
          .string()
          .refine(
            (value) =>
              [
                'ready_to_development',
                'in_development',
                'testing',
                'completed',
                'error',
              ].includes(value),
            'Неверно выбрана позиция',
          ),
      },
      children: ({state, handleChange, handleBlur}) => (
        <Tooltip title={state.meta.errors[0]}>
          <DrawerTypeSelect
            maxTagCount={1}
            labelRender={(props) => (
              <div>
                <GroupTypeTagContainer type={props.value as any}>
                  <GroupTypeTag
                    color={colors[props.value]}
                    text={typeNames[props.value]}
                  />
                </GroupTypeTagContainer>
              </div>
            )}
            optionRender={(props) => (
              <GroupTypeTag
                color={colors[props.value]}
                text={typeNames[props.value]}
              />
            )}
            options={[
              {
                key: 0,
                value: 'ready_to_development',
              },
              {
                key: 1,
                value: 'in_development',
              },
              {
                key: 2,
                value: 'testing',
              },
              {
                key: 3,
                value: 'completed',
              },
              {
                key: 4,
                value: 'error',
              },
            ]}
            value={state.value}
            onChange={(value: string) => handleChange(value)}
            onBlur={handleBlur}
          />
        </Tooltip>
      ),
    },
    {
      label: 'ID',
      icon: <SnippetsOutlined />,
      children: ({}) => (
        <DrawerDescriptionsItemContainer>
          <Typography.Text
            copyable={!!task}
            type={!task ? 'secondary' : undefined}
          >
            {task?.slug || '...'}
          </Typography.Text>
        </DrawerDescriptionsItemContainer>
      ),
    },
    {
      label: 'Создатель',
      icon: <UserOutlined />,
      children: ({}) =>
        !!task ? (
          <UserTag
            key={task.creator.id}
            firstName={task.creator.first_name}
            lastName={task.creator.last_name}
            username={task.creator.username}
          />
        ) : (
          <DrawerDescriptionsItemContainer>
            <Typography.Text type="secondary">...</Typography.Text>
          </DrawerDescriptionsItemContainer>
        ),
    },
    {
      name: 'assigners',
      label: 'Исполнители',
      icon: <TeamOutlined />,
      contentSpan: 9,
      children: ({state, handleChange, handleBlur}) => (
        <Hoverable>
          <AssignersSelect
            notFoundContent={<Empty description="Пользователи не найдены." />}
            placeholder="Выберите..."
            variant="borderless"
            mode="multiple"
            value={state.value}
            onChange={(value) => handleChange(value)}
            onBlur={handleBlur}
            tagRender={(props) => props.label as any}
            suffixIcon={null}
          >
            <AssignersSelectGroup label="BACKEND">
              <AssignersSelect.Option value={1}>
                <UserTag
                  unfocusable
                  firstName="Kirill"
                  lastName="Andreev"
                  username="andreev_01"
                />
              </AssignersSelect.Option>
            </AssignersSelectGroup>

            <AssignersSelectGroup label="FRONTEND">
              <AssignersSelect.Option value={2}>
                <UserTag
                  unfocusable
                  firstName="Kirill"
                  lastName="Matveev"
                  username="matveev_01"
                />
              </AssignersSelect.Option>
            </AssignersSelectGroup>
          </AssignersSelect>
        </Hoverable>
      ),
    },
    {
      name: 'from_branch',
      label: 'Ветка',
      validators: {
        onBlur: z
          .string()
          .regex(
            /^(?!.*\-\-)((main|next|staging|dev(elop)?|test(ing)?)$|^((feat(ure)?|(bug|hot)?fix|docs|wip|test(ing)?)\/(?!\-)([a-z0-9\-]{1,50}(?<!-)\/(?!\-))?[a-z0-9\-]{1,100}(?<!-))$|^release\/v?(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?)$/,
            'Название ветки должно быть написано на латинских сомволах без пробелов.',
          )
          .nullish(),
      },
      icon: <BranchesOutlined />,
      children: ({state, handleChange, handleBlur}) => (
        <Tooltip title={state.meta.errors[0]}>
          <DrawerDescriptionsItemContainer>
            <EditableTag
              value={state.value}
              color={state.meta.errors.length > 0 ? 'red' : 'blue'}
              placeholder="+ Создать"
              onChange={(value) => handleChange(value)}
              onBlur={handleBlur}
            />
          </DrawerDescriptionsItemContainer>
        </Tooltip>
      ),
    },
    {
      name: 'deadline',
      label: 'Дата окончания',
      icon: <ScheduleOutlined />,
      validators: {
        onChange: dayjsSchema.nullish().superRefine((value, ctx) => {
          if (!value) return;
          if (value.diff(dayjs(), 'seconds') <= 0) {
            return ctx.addIssue({
              message: 'Дата не может быть раньше текущего времени.',
              code: 'custom',
            });
          }
        }),
      },
      children: ({state, handleChange, handleBlur}) => (
        <Tooltip title={state.meta.errors[0]}>
          <Hoverable>
            <DatePicker
              format="DD.MM.YYYY"
              placeholder="Выберите дату"
              value={state.value}
              onChange={(value) => handleChange(value)}
              onBlur={handleBlur}
              status={!!state.meta.errors[0] && 'error'}
              minDate={dayjs().add(1, 'day')}
            />
          </Hoverable>
        </Tooltip>
      ),
    },
    !!task && {
      label: 'Дата создания',
      icon: <HistoryOutlined />,
      children: ({}) =>
        !!task ? (
          <DrawerDescriptionsItemContainer>
            <Typography.Text type="secondary">
              {dayjs().format('DD.MM.YYYY HH:MM')}
            </Typography.Text>
          </DrawerDescriptionsItemContainer>
        ) : (
          <DrawerDescriptionsItemContainer>
            <Typography.Text type="secondary">...</Typography.Text>
          </DrawerDescriptionsItemContainer>
        ),
    },
  ];

  return (
    <Drawer
      open={open}
      destroyOnClose
      onClose={() => onClose?.(false)}
      title={
        <Flex gap="small" justify="end">
          {!!task && (
            <Hoverable style={{fontSize: '1.15rem'}}>
              <CommentOutlined size={60} />
            </Hoverable>
          )}

          {!!task && (
            <Hoverable style={{fontSize: '1.15rem'}}>
              <StarOutlined size={60} />
            </Hoverable>
          )}

          <Hoverable style={{fontSize: '1.15rem'}}>
            <EllipsisOutlined size={60} />
          </Hoverable>
        </Flex>
      }
    >
      <Flex vertical gap="middle">
        <form.Field
          name="title"
          validators={{
            onChange: z
              .string({required_error: 'Обязательное поле.'})
              .min(1, 'Обязательное поле.')
              .min(3, 'Минимальная длина - 3 символа.')
              .max(75, 'Максимальная длина - 75 символов.'),
          }}
        >
          {({state, handleChange, handleBlur}) => (
            <Tooltip title={state.meta.errors[0]}>
              <DrawerTaskTitle
                error={state.meta.errors.length > 0}
                size="large"
                placeholder="Заголовок задачи"
                autoSize
                value={state.value}
                onChange={({target}) => handleChange(target?.value)}
                onBlur={handleBlur}
                maxLength={75}
              />
            </Tooltip>
          )}
        </form.Field>

        {descriptionsElements
          .slice(
            0,
            !showAdditionalOptions
              ? DESCRIPTIONS_COLLAPSED_LENGTH
              : descriptionsElements.length,
          )
          .map((element) => (
            <Row
              align={(element.align! as any) || 'middle'}
              key={element.label as string}
            >
              <Tooltip title={element.label} placement="left">
                <Col span={8} offset={1}>
                  <IconText icon={element.icon}>{element.label}</IconText>
                </Col>
              </Tooltip>

              <Col offset={2} span={element.contentSpan!}>
                {!!element.name ? (
                  <form.Field
                    name={element.name as any}
                    validators={element.validators!}
                  >
                    {element.children}
                  </form.Field>
                ) : (
                  element.children({})
                )}
              </Col>
            </Row>
          ))}

        <PaddingContainer top="0.5rem">
          <Row align="middle">
            <Col offset={1} span={32}>
              <TextColorContainer color="grey">
                <IconText
                  icon={
                    !!showAdditionalOptions ? <UpOutlined /> : <DownOutlined />
                  }
                  onClick={() =>
                    setShowAdditionalOptions(!showAdditionalOptions)
                  }
                >
                  <Typography.Text type="secondary">
                    {!showAdditionalOptions
                      ? `${descriptionsElements.length - DESCRIPTIONS_COLLAPSED_LENGTH} других опций`
                      : `Скрыть ${descriptionsElements.length - DESCRIPTIONS_COLLAPSED_LENGTH} опции`}
                  </Typography.Text>
                </IconText>
              </TextColorContainer>
            </Col>
          </Row>
        </PaddingContainer>

        <NoMarginDivider />

        {!!task && (
          <>
            <CommentList
              comments={task?.comments || []}
              allowWrite
              user={task?.creator}
            />

            <NoMarginDivider />
          </>
        )}

        <form.Field
          name="description"
          validators={{
            onBlur: z
              .string()
              .max(500, 'Максимальная длина описания - 255 символов.')
              .nullish(),
          }}
        >
          {({state, handleChange, handleBlur}) => (
            <>
              <DrawerTaskDescription
                placeholder="Укажите описание задачи"
                value={state.value}
                onChange={({target}) => handleChange(target?.value)}
                onBlur={handleBlur}
                autoSize
              />
              <code>{state.meta.errors[0]}</code>
            </>
          )}
        </form.Field>
      </Flex>
    </Drawer>
  );
}
